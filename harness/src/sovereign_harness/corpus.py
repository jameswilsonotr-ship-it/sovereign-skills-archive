"""Offline BURN HARD corpus loading and connector call-log ingestion.

The manifest points at optional local blobs. Missing blobs are expected in a
clean checkout, so the loader creates deterministic synthetic data instead of
contacting a service or silently producing an empty corpus.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


class ManifestError(ValueError):
    """Raised when a corpus manifest or corpus record is invalid."""


@dataclass(frozen=True)
class CorpusSpec:
    """One corpus artifact declared by a manifest."""

    name: str
    kind: str
    path: str
    format: str
    output: str
    sha256: str | None
    synthetic: Any


@dataclass(frozen=True)
class ArtifactReceipt:
    """Receipt for one copied or generated artifact."""

    name: str
    kind: str
    source: str
    input_path: str
    output_path: str
    sha256: str
    record_count: int


@dataclass(frozen=True)
class IngestReport:
    """Summary returned after a manifest has been ingested."""

    manifest: str
    output_dir: str
    artifacts: tuple[ArtifactReceipt, ...]

    @property
    def record_count(self) -> int:
        return sum(artifact.record_count for artifact in self.artifacts)

    def as_dict(self) -> dict[str, Any]:
        return {
            "manifest": self.manifest,
            "output_dir": self.output_dir,
            "record_count": self.record_count,
            "artifacts": [asdict(artifact) for artifact in self.artifacts],
        }


def _manifest_path(path: Path) -> Path:
    if path.is_dir():
        for candidate in ("MANIFEST.json", "MANIFEST.md"):
            candidate_path = path / candidate
            if candidate_path.is_file():
                return _manifest_path(candidate_path)
        raise ManifestError(f"no MANIFEST.json or MANIFEST.md found in {path}")

    if path.suffix.lower() == ".md":
        sibling = path.with_suffix(".json")
        if sibling.is_file():
            return sibling
        raise ManifestError(f"markdown manifest has no machine-readable sibling: {path}")
    return path


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read manifest {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ManifestError("manifest root must be an object")
    return value


def load_manifest(path: Path | str) -> tuple[Path, tuple[CorpusSpec, ...]]:
    """Load a JSON manifest, accepting its human-readable ``MANIFEST.md`` twin."""

    manifest_path = _manifest_path(Path(path))
    payload = _read_json(manifest_path)
    entries = payload.get("corpora", payload.get("entries"))
    if not isinstance(entries, list) or not entries:
        raise ManifestError("manifest must contain a non-empty 'corpora' list")

    specs: list[CorpusSpec] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ManifestError("every corpus entry must be an object")
        try:
            name = str(entry["name"])
            kind = str(entry["kind"])
            relative_path = str(entry["path"])
        except KeyError as exc:
            raise ManifestError(f"corpus entry is missing {exc.args[0]!r}") from exc
        output = str(entry.get("output", Path(relative_path).name))
        file_format = str(entry.get("format", "json"))
        expected_sha = entry.get("sha256")
        if expected_sha is not None and (
            not isinstance(expected_sha, str) or len(expected_sha) != 64
        ):
            raise ManifestError(f"{name}: sha256 must be a 64-character hex string")
        specs.append(
            CorpusSpec(
                name=name,
                kind=kind,
                path=relative_path,
                format=file_format,
                output=output,
                sha256=expected_sha,
                synthetic=entry.get("synthetic"),
            )
        )
    return manifest_path, tuple(specs)


def _safe_relative_path(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ManifestError(f"corpus path escapes manifest directory: {relative_path}") from exc
    return candidate


def _default_synthetic(spec: CorpusSpec) -> Any:
    if spec.kind == "phone_health":
        return {
            "status": "ok",
            "service": "phone-bridge",
            "version": "0.1.0",
            "capabilities": ["health", "offline-fixtures"],
        }
    if spec.kind == "connector_call_log":
        return [
            {
                "connector": "phone_bridge",
                "operation": "health",
                "account_id": None,
                "request": {},
            }
        ]
    raise ManifestError(f"{spec.name}: missing synthetic fallback for kind {spec.kind!r}")


def _synthetic_bytes(spec: CorpusSpec) -> bytes:
    value = spec.synthetic if spec.synthetic is not None else _default_synthetic(spec)
    if spec.kind == "connector_call_log":
        records = value.get("records") if isinstance(value, dict) else value
        if not isinstance(records, list):
            raise ManifestError(f"{spec.name}: synthetic call log must be a list")
        return b"".join(
            (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
            for record in records
        )
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _validate_call_record(record: Any, name: str, line: int) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ManifestError(f"{name}: record {line} must be an object")
    required = ("connector", "operation", "request")
    missing = [field for field in required if field not in record]
    if missing:
        raise ManifestError(f"{name}: record {line} missing {', '.join(missing)}")
    if not isinstance(record["connector"], str) or not record["connector"]:
        raise ManifestError(f"{name}: record {line} has an invalid connector")
    if not isinstance(record["operation"], str) or not record["operation"]:
        raise ManifestError(f"{name}: record {line} has an invalid operation")
    if not isinstance(record["request"], dict):
        raise ManifestError(f"{name}: record {line} request must be an object")
    return dict(record)


def _record_count(spec: CorpusSpec, content: bytes) -> int:
    if spec.kind != "connector_call_log":
        return 1
    records = []
    for line_number, line in enumerate(content.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ManifestError(f"{spec.name}: invalid JSON on line {line_number}") from exc
        records.append(_validate_call_record(record, spec.name, line_number))
    if not records:
        raise ManifestError(f"{spec.name}: call-log corpus is empty")
    return len(records)


def _validate_phone_health(spec: CorpusSpec, content: bytes) -> None:
    if spec.kind != "phone_health":
        return
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{spec.name}: phone health is not valid JSON") from exc
    required = {"status", "service", "version", "capabilities"}
    if not isinstance(payload, dict) or not required.issubset(payload):
        raise ManifestError(f"{spec.name}: phone health is missing required fields")
    if payload["status"] != "ok" or payload["service"] != "phone-bridge":
        raise ManifestError(f"{spec.name}: phone health is not an ok phone-bridge payload")


def _artifact_bytes(spec: CorpusSpec, root: Path) -> tuple[bytes, str, Path]:
    source_path = _safe_relative_path(root, spec.path)
    if source_path.is_file():
        content = source_path.read_bytes()
        source = "blob"
        if spec.sha256 and hashlib.sha256(content).hexdigest() != spec.sha256:
            raise ManifestError(f"{spec.name}: blob SHA-256 does not match the manifest")
    else:
        content = _synthetic_bytes(spec)
        source = "synthetic"
    _validate_phone_health(spec, content)
    _record_count(spec, content)
    return content, source, source_path


def ingest_manifest(
    manifest: Path | str,
    output_dir: Path | str,
) -> IngestReport:
    """Copy or synthesize every manifest artifact into ``output_dir``."""

    manifest_path, specs = load_manifest(manifest)
    root = manifest_path.parent
    destination = Path(output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    receipts: list[ArtifactReceipt] = []
    for spec in specs:
        content, source, input_path = _artifact_bytes(spec, root)
        output_path = (destination / spec.output).resolve()
        try:
            output_path.relative_to(destination)
        except ValueError as exc:
            raise ManifestError(f"{spec.name}: output escapes destination directory") from exc
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)
        receipts.append(
            ArtifactReceipt(
                name=spec.name,
                kind=spec.kind,
                source=source,
                input_path=str(input_path),
                output_path=str(output_path),
                sha256=hashlib.sha256(content).hexdigest(),
                record_count=_record_count(spec, content),
            )
        )
    report = IngestReport(str(manifest_path), str(destination), tuple(receipts))
    (destination / "INGEST_RECEIPT.json").write_text(
        json.dumps(report.as_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


def read_connector_call_log(path: Path | str) -> tuple[dict[str, Any], ...]:
    """Read and validate an ingested JSONL connector call log."""

    file_path = Path(path)
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            records.append(_validate_call_record(json.loads(line), file_path.name, line_number))
    return tuple(records)


def ingest_connector_call_log(target: Any, records: Iterable[Mapping[str, Any]]) -> int:
    """Insert records into a test ``CallLog``-like object.

    The test fixture exposes ``record`` so ingestion stays independent of
    DuckDB. This small adapter also makes the ingest useful to callers that
    provide their own in-memory ledger.
    """

    count = 0
    for record in records:
        normalized = _validate_call_record(dict(record), "connector-call-log", count + 1)
        target.record(normalized)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = ingest_manifest(args.manifest, args.output)
    print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

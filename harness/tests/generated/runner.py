"""Dependency-free verifier for the committed OpenSpec scenario corpus."""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

if __package__ in (None, ""):
    # Keep the verifier usable both as ``python -m ...`` and as a file.
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from harness.tests.generated.generate import (
        DEFAULT_OUTPUT_DIR,
        MANIFEST_FILENAME,
        SCENARIOS_FILENAME,
        render_dataset,
    )
    from harness.tests.generated.scenario_schema import (
        GENERATOR_VERSION,
        SCENARIO_COUNT,
        SCHEMA,
        SCHEMA_VERSION,
        ScenarioError,
        parse_jsonl,
        sha256_bytes,
    )
    from harness.tests.generated.templates import CASES
else:
    from .generate import (
        DEFAULT_OUTPUT_DIR,
        MANIFEST_FILENAME,
        SCENARIOS_FILENAME,
        render_dataset,
    )
    from .scenario_schema import (
        GENERATOR_VERSION,
        SCENARIO_COUNT,
        SCHEMA,
        SCHEMA_VERSION,
        ScenarioError,
        parse_jsonl,
        sha256_bytes,
    )
    from .templates import CASES


@contextmanager
def offline_guard() -> Iterator[None]:
    """Turn accidental network or child-process use into an immediate failure."""

    def blocked(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("generated OpenSpec verification is offline-only")

    targets = [
        (socket.socket, "connect"),
        (socket, "create_connection"),
        (socket, "getaddrinfo"),
        (subprocess, "Popen"),
        (subprocess, "run"),
        (subprocess, "call"),
        (subprocess, "check_call"),
        (subprocess, "check_output"),
        (urllib.request, "urlopen"),
    ]
    originals = [(target, name, getattr(target, name)) for target, name in targets]
    try:
        for target, name, _original in originals:
            setattr(target, name, blocked)
        yield
    finally:
        for target, name, original in originals:
            setattr(target, name, original)


def verify_dataset(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    """Validate count, schema, hashes, case coverage, and determinism."""

    manifest_path = output_dir / MANIFEST_FILENAME
    scenarios_path = output_dir / SCENARIOS_FILENAME
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        scenarios_bytes = scenarios_path.read_bytes()
    except (OSError, json.JSONDecodeError) as exc:
        raise ScenarioError(f"cannot read generated corpus: {exc}") from exc

    expected_cases = [case.source_case for case in CASES]
    if manifest.get("schema") != SCHEMA or manifest.get("schema_version") != SCHEMA_VERSION:
        raise ScenarioError("manifest schema mismatch")
    if manifest.get("generator_version") != GENERATOR_VERSION:
        raise ScenarioError("manifest generator version mismatch")
    if manifest.get("scenario_count") != SCENARIO_COUNT:
        raise ScenarioError("manifest scenario count mismatch")
    if manifest.get("source_cases") != expected_cases:
        raise ScenarioError("manifest source case catalog mismatch")
    if manifest.get("scenarios_sha256") != sha256_bytes(scenarios_bytes):
        raise ScenarioError("scenario corpus hash mismatch")

    records = parse_jsonl(scenarios_bytes)
    if len(records) != SCENARIO_COUNT:
        raise ScenarioError(f"expected {SCENARIO_COUNT} records, got {len(records)}")
    ids = [record["scenario_id"] for record in records]
    if len(set(ids)) != len(ids):
        raise ScenarioError("scenario IDs must be unique")
    if {record["source_case"] for record in records} != set(expected_cases):
        raise ScenarioError("every documented OpenSpec case must have a generated stub")
    for record in records:
        if "external_network" not in record["forbidden_effects"]:
            raise ScenarioError(f"{record['scenario_id']} lacks network prohibition")
        if record["setup"].get("external_io") != "disabled":
            raise ScenarioError(f"{record['scenario_id']} is not offline")

    expected_scenarios, expected_manifest = render_dataset()
    if scenarios_bytes != expected_scenarios:
        raise ScenarioError("scenario corpus is not reproducible from the generator")
    if manifest_path.read_bytes() != expected_manifest:
        raise ScenarioError("manifest is not reproducible from the generator")
    return {
        "status": "verified",
        "scenario_count": len(records),
        "source_case_count": len(expected_cases),
        "scenarios_sha256": sha256_bytes(scenarios_bytes),
        "offline": True,
        "deterministic": True,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        with offline_guard():
            report = verify_dataset(args.output_dir)
    except (AssertionError, OSError, ScenarioError, ValueError) as exc:
        print(f"verification error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

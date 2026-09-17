"""Generate the committed offline OpenSpec scenario corpus.

Examples:

    python3 -m harness.tests.generated.generate
    python3 -m harness.tests.generated.generate --check
    python3 -m harness.tests.generated.generate --count 32 --output-dir /tmp/openspec
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    # Keep the generator usable both as ``python -m ...`` and as a file.
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from harness.tests.generated.scenario_schema import (
        GENERATOR_VERSION,
        SCENARIO_COUNT,
        SCHEMA,
        SCHEMA_VERSION,
        SEED,
        canonical_json,
        canonical_jsonl,
        sha256_bytes,
        validate_scenario,
    )
    from harness.tests.generated.templates import CASES, build_scenario
else:
    from .scenario_schema import (
        GENERATOR_VERSION,
        SCENARIO_COUNT,
        SCHEMA,
        SCHEMA_VERSION,
        SEED,
        canonical_json,
        canonical_jsonl,
        sha256_bytes,
        validate_scenario,
    )
    from .templates import CASES, build_scenario

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent
SCENARIOS_FILENAME = "scenarios.jsonl"
MANIFEST_FILENAME = "manifest.json"


def generate_scenarios(count: int = SCENARIO_COUNT, seed: int = SEED) -> list[dict[str, Any]]:
    """Generate exactly ``count`` records with stable case-balanced ordering."""

    if count < len(CASES):
        raise ValueError(f"count must cover all {len(CASES)} OpenSpec cases")
    base, remainder = divmod(count, len(CASES))
    records: list[dict[str, Any]] = []
    for case_index, case in enumerate(CASES):
        variants = base + (case_index < remainder)
        for variant in range(1, variants + 1):
            record = build_scenario(case, variant, seed)
            validate_scenario(record)
            records.append(record)
    return records


def manifest_for(records: list[dict[str, Any]], scenarios_bytes: bytes, seed: int) -> dict[str, Any]:
    """Create the deterministic metadata file for a rendered corpus."""

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "artifact": "offline-synthetic-openspec-scenarios",
        "generator": "harness.tests.generated.generate",
        "generator_version": GENERATOR_VERSION,
        "seed": seed,
        "scenario_count": len(records),
        "source_case_count": len(CASES),
        "source_cases": [case.source_case for case in CASES],
        "scenarios_file": SCENARIOS_FILENAME,
        "scenarios_sha256": sha256_bytes(scenarios_bytes),
        "status": "stub",
    }


def render_dataset(count: int = SCENARIO_COUNT, seed: int = SEED) -> tuple[bytes, bytes]:
    """Render JSONL and manifest bytes without touching the filesystem."""

    records = generate_scenarios(count=count, seed=seed)
    scenarios_bytes = canonical_jsonl(records)
    manifest = manifest_for(records, scenarios_bytes, seed)
    manifest_bytes = (canonical_json(manifest) + "\n").encode("utf-8")
    return scenarios_bytes, manifest_bytes


def write_dataset(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    count: int = SCENARIO_COUNT,
    seed: int = SEED,
) -> tuple[Path, Path]:
    """Write a deterministic corpus and return its two output paths."""

    scenarios_bytes, manifest_bytes = render_dataset(count=count, seed=seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    scenarios_path = output_dir / SCENARIOS_FILENAME
    manifest_path = output_dir / MANIFEST_FILENAME
    scenarios_path.write_bytes(scenarios_bytes)
    manifest_path.write_bytes(manifest_bytes)
    return scenarios_path, manifest_path


def check_dataset(output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    """Fail if committed files differ from deterministic generator output."""

    scenarios_path = output_dir / SCENARIOS_FILENAME
    manifest_path = output_dir / MANIFEST_FILENAME
    expected_scenarios, expected_manifest = render_dataset()
    actual_scenarios = scenarios_path.read_bytes()
    actual_manifest = manifest_path.read_bytes()
    if actual_scenarios != expected_scenarios:
        raise ValueError(f"{scenarios_path} is stale; run the generator")
    if actual_manifest != expected_manifest:
        raise ValueError(f"{manifest_path} is stale; run the generator")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify committed output")
    parser.add_argument("--count", type=int, default=SCENARIO_COUNT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.check:
            if args.count != SCENARIO_COUNT or args.seed != SEED or args.output_dir != DEFAULT_OUTPUT_DIR:
                raise ValueError("--check only supports the committed default corpus")
            check_dataset(args.output_dir)
            print(f"verified {SCENARIO_COUNT} deterministic offline OpenSpec stubs")
        else:
            scenarios_path, manifest_path = write_dataset(args.output_dir, args.count, args.seed)
            print(f"generated {args.count} scenarios: {scenarios_path}")
            print(f"manifest: {manifest_path}")
    except (OSError, ValueError) as exc:
        print(f"generator error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

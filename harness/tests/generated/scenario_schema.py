"""Schema and canonical serialization helpers for generated OpenSpec stubs.

This module intentionally uses only the Python standard library.  The records
are contract-shaped data, not executable claims about a production system.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from typing import Any

SCHEMA = "sovereign.openspec.scenario"
SCHEMA_VERSION = "0.1.0"
GENERATOR_VERSION = "1.0.0"
SEED = 20260917
SCENARIO_COUNT = 1000

REQUIRED_FIELDS = frozenset(
    {
        "schema",
        "schema_version",
        "scenario_id",
        "source_case",
        "family",
        "variant",
        "seed",
        "setup",
        "steps",
        "expected",
        "invariants",
        "forbidden_effects",
        "status",
    }
)
ALLOWED_STATUS = frozenset({"stub"})


class ScenarioError(ValueError):
    """Raised when a generated scenario violates the corpus contract."""


def canonical_json(value: Any) -> str:
    """Return the stable JSON representation used for hashes and JSONL."""

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_jsonl(records: Iterable[Mapping[str, Any]]) -> bytes:
    """Serialize records as deterministic UTF-8 JSONL with a final newline."""

    return "".join(canonical_json(record) + "\n" for record in records).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ScenarioError(message)


def validate_scenario(scenario: Mapping[str, Any]) -> None:
    """Validate one scenario without importing a schema or network package."""

    _require(isinstance(scenario, Mapping), "scenario must be an object")
    keys = set(scenario)
    _require(keys == REQUIRED_FIELDS, f"unexpected scenario fields: {sorted(keys ^ REQUIRED_FIELDS)}")
    _require(scenario["schema"] == SCHEMA, "unsupported scenario schema")
    _require(scenario["schema_version"] == SCHEMA_VERSION, "unsupported scenario version")
    _require(
        isinstance(scenario["scenario_id"], str)
        and scenario["scenario_id"].startswith("OS-"),
        "scenario_id must be an OpenSpec identifier",
    )
    _require(
        isinstance(scenario["source_case"], str)
        and len(scenario["source_case"].split("-")) == 2,
        "source_case must look like CT-001",
    )
    _require(isinstance(scenario["family"], str) and scenario["family"], "family is required")
    _require(
        isinstance(scenario["variant"], int) and not isinstance(scenario["variant"], bool)
        and scenario["variant"] > 0,
        "variant must be a positive integer",
    )
    _require(
        isinstance(scenario["seed"], int) and not isinstance(scenario["seed"], bool),
        "seed must be an integer",
    )
    _require(isinstance(scenario["setup"], Mapping), "setup must be an object")
    _require(
        isinstance(scenario["steps"], list) and scenario["steps"],
        "steps must be a non-empty list",
    )
    for index, step in enumerate(scenario["steps"]):
        _require(isinstance(step, Mapping), f"step {index} must be an object")
        _require(
            isinstance(step.get("op"), str) and step["op"],
            f"step {index} must have an operation",
        )
        _require(isinstance(step.get("args"), Mapping), f"step {index} args must be an object")
    _require(isinstance(scenario["expected"], Mapping), "expected must be an object")
    _require(
        isinstance(scenario["expected"].get("outcome"), str)
        and scenario["expected"]["outcome"],
        "expected.outcome is required",
    )
    _require(
        scenario["expected"].get("code") is None
        or isinstance(scenario["expected"]["code"], str),
        "expected.code must be a string or null",
    )
    for field in ("invariants", "forbidden_effects"):
        values = scenario[field]
        _require(isinstance(values, list) and values, f"{field} must be non-empty")
        _require(
            all(isinstance(value, str) and value for value in values),
            f"{field} must contain non-empty strings",
        )
    _require(scenario["status"] in ALLOWED_STATUS, "generated records must remain stubs")


def parse_jsonl(raw: bytes) -> list[dict[str, Any]]:
    """Parse and validate a JSONL corpus, rejecting blank or malformed rows."""

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            raise ScenarioError(f"blank JSONL line at {line_number}")
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ScenarioError(f"invalid JSON on line {line_number}: {exc}") from exc
        validate_scenario(record)
        records.append(record)
    return records

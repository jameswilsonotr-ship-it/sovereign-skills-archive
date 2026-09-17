"""Offline checks for the minimum size of connector fixtures."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pytest


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"
MIN_RECORDS = 6
SUPPORTED_SUFFIXES = {".csv", ".json", ".jsonl", ".ndjson"}


def _fixture_files() -> list[Path]:
    """Return local connector fixture files, if the fixture tree is present."""
    if not FIXTURE_ROOT.is_dir():
        return []
    return sorted(
        path
        for path in FIXTURE_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def _records_from_json(path: Path) -> list[Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("records", "data", "items", "messages"):
            records = payload.get(key)
            if isinstance(records, list):
                return records
    raise AssertionError(
        f"{path} must contain a JSON array or an object with a records list"
    )


def _record_count(path: Path) -> int:
    """Count records without making network calls or importing connector code."""
    suffix = path.suffix.lower()
    if suffix in {".jsonl", ".ndjson"}:
        return sum(
            bool(line.strip())
            for line in path.read_text(encoding="utf-8").splitlines()
        )
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as fixture:
            return sum(1 for _ in csv.DictReader(fixture))
    return len(_records_from_json(path))


def test_connector_fixtures_have_minimum_records() -> None:
    """Every connector fixture that exists must contain at least six records."""
    fixture_paths = _fixture_files()
    if not fixture_paths:
        pytest.skip("no connector fixture files are present")

    for fixture_path in fixture_paths:
        assert _record_count(fixture_path) >= MIN_RECORDS, (
            f"{fixture_path} must contain at least {MIN_RECORDS} records"
        )

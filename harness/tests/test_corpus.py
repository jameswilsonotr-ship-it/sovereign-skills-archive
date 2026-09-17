from __future__ import annotations

import json
from pathlib import Path

import pytest

from sovereign_harness.corpus import (
    ingest_connector_call_log,
    ingest_manifest,
    read_connector_call_log,
)

pytestmark = pytest.mark.smoke

MANIFEST = Path(__file__).parents[2] / "docs" / "burn-wave" / "corpora" / "MANIFEST.json"


def test_missing_burn_wave_blobs_are_replaced_with_deterministic_fixtures(
    tmp_path: Path,
) -> None:
    report = ingest_manifest(MANIFEST, tmp_path)

    assert {artifact.source for artifact in report.artifacts} == {"synthetic"}
    assert report.record_count == 5
    assert json.loads((tmp_path / "phone_health.json").read_text())["status"] == "ok"
    assert len(read_connector_call_log(tmp_path / "connector_call_log.jsonl")) == 4

    receipt = json.loads((tmp_path / "INGEST_RECEIPT.json").read_text())
    assert receipt["record_count"] == 5
    assert receipt["artifacts"][1]["source"] == "synthetic"


def test_local_burn_wave_blobs_override_synthetic_data(tmp_path: Path) -> None:
    manifest_payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_payload["corpora"][0]["path"] = "blobs/phone_health.json"
    local_manifest = tmp_path / "MANIFEST.json"
    local_manifest.write_text(json.dumps(manifest_payload), encoding="utf-8")
    blobs = tmp_path / "blobs"
    blobs.mkdir()
    (blobs / "phone_health.json").write_text(
        json.dumps(
            {
                "status": "ok",
                "service": "phone-bridge",
                "version": "local",
                "capabilities": ["health", "offline-fixtures"],
            }
        )
    )
    report = ingest_manifest(local_manifest, tmp_path / "output")
    phone_artifact = next(
        artifact for artifact in report.artifacts if artifact.kind == "phone_health"
    )
    assert phone_artifact.source == "blob"
    assert json.loads((tmp_path / "output" / "phone_health.json").read_text())["version"] == "local"


def test_call_log_corpus_can_be_loaded_into_the_offline_ledger(
    tmp_path: Path,
    call_log,
) -> None:
    ingest_manifest(MANIFEST, tmp_path)
    records = read_connector_call_log(tmp_path / "connector_call_log.jsonl")

    assert ingest_connector_call_log(call_log, records) == 4
    assert call_log.count() == 4
    connectors = call_log.connection.execute(
        "SELECT connector FROM connector_calls ORDER BY connector"
    ).fetchall()
    assert connectors == [("drive",), ("github",), ("gmail",), ("linear",)]

"""Offline contract checks for connector configuration identity."""

from __future__ import annotations

import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _connector_configs() -> list[Path]:
    """Return connector JSON manifests without touching external services."""
    return sorted((REPOSITORY_ROOT / "skill_tree").glob("**/connectors/*/*.json"))


def test_connector_manifests_require_account_id() -> None:
    """Every connector manifest must identify the account it belongs to."""
    manifests = _connector_configs()
    assert manifests, "expected at least one connector manifest"

    missing_account_id: list[str] = []
    for manifest in manifests:
        with manifest.open(encoding="utf-8") as handle:
            payload = json.load(handle)

        if not isinstance(payload, dict) or not payload.get("account_id"):
            missing_account_id.append(str(manifest.relative_to(REPOSITORY_ROOT)))

    assert not missing_account_id, (
        "connector manifests must define a non-empty account_id: "
        + ", ".join(missing_account_id)
    )

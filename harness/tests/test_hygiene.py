from __future__ import annotations

from pathlib import Path

import pytest

from sovereign_harness import hygiene

pytestmark = pytest.mark.smoke


def test_keep_lake_query_hygiene_passes() -> None:
    repo_root = Path(__file__).parents[2]

    report = hygiene.check_keep_lake_query(repo_root)

    assert report.passed, report.issues


def test_hygiene_gate_rejects_live_skill_write(monkeypatch) -> None:
    repo_root = Path(__file__).parents[2]
    monkeypatch.setattr(
        hygiene,
        "_changed_paths",
        lambda *_args: {"skill_tree/skills/example/SKILL.md"},
    )

    report = hygiene.check_keep_lake_query(repo_root)

    assert not report.passed
    assert any("live SKILL.md writes" in issue for issue in report.issues)

from __future__ import annotations

from pathlib import Path

import pytest

from sovereign_harness.redaction import check_fixture_directory, scan_text

pytestmark = pytest.mark.smoke

FIXTURE_DIR = (
    Path(__file__).parents[1] / "src" / "sovereign_harness" / "fixtures"
)


def test_ultra_local_fixtures_pass_the_redaction_check() -> None:
    findings = check_fixture_directory(FIXTURE_DIR)

    assert list(FIXTURE_DIR.glob("*.json")), "the check must exercise local fixtures"
    assert not findings, findings


def test_redaction_findings_do_not_echo_synthetic_canaries() -> None:
    text = """
    {"email": "fixture.person@example.invalid",
     "phone": "+1 555-010-0100",
     "api_key": "fixture-key-1234567890"}
    """

    findings = scan_text(text, "synthetic-canary.json")

    assert {finding.rule for finding in findings} == {
        "credential-assignment",
        "email",
        "phone",
    }
    assert all(
        "fixture.person@example.invalid" not in repr(finding)
        and "fixture-key-1234567890" not in repr(finding)
        for finding in findings
    )

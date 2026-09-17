from __future__ import annotations

import json
import socket
from pathlib import Path
from typing import Any

import pytest

from sovereign_harness.connectors import PhoneBridgeStub

pytestmark = pytest.mark.smoke

FIXTURE = (
    Path(__file__).parents[2]
    / "docs"
    / "burn-wave"
    / "fixtures"
    / "sms_default_deny.json"
)


def _sms_cases() -> list[dict[str, Any]]:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert payload["change_id"] == "second-salvo-22-sms-default-deny"
    assert payload["slot"] == "S2-22"
    assert payload["lane"] == "included-ultra"
    return payload["cases"]


@pytest.mark.parametrize("case", _sms_cases(), ids=lambda case: case["case_id"])
def test_sms_without_consent_is_denied_offline(
    case: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def network_forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("SMS default-deny case attempted network access")

    monkeypatch.setattr(socket, "socket", network_forbidden)

    assert case["expected_decision"] == "deny"
    with pytest.raises(NotImplementedError, match="SMS"):
        PhoneBridgeStub().send_sms(case["recipient"], case["body"])

"""Audit-safety contracts for offline flashlight authorization."""

from harness.tests.stubs import (
    FailingAuditSink,
    OfflineFlashlightStub,
    RecordingAuditSink,
)


def test_denial_is_audited_without_recording_untrusted_input():
    sink = RecordingAuditSink()
    secret_like_input = "blink-token-do-not-store"

    decision = OfflineFlashlightStub(audit_sink=sink).request(secret_like_input)

    assert decision["allowed"] is False
    assert decision["reason"] == "unsupported_action"
    assert secret_like_input not in repr(sink.events)
    assert sink.events == [
        {
            "event": "flashlight.authorization",
            "action": "<unknown>",
            "outcome": "denied",
            "reason": "unsupported_action",
        }
    ]


def test_audit_records_are_bounded_to_contract_fields():
    sink = RecordingAuditSink()
    flashlight = OfflineFlashlightStub(audit_sink=sink)

    flashlight.request("status")

    assert set(sink.events[0]) == {"event", "action", "outcome", "reason"}
    assert all(isinstance(value, str) for value in sink.events[0].values())


def test_audit_failure_fails_closed():
    decision = OfflineFlashlightStub(
        allowed_actions={"status"},
        audit_sink=FailingAuditSink(),
    ).request("status")

    assert decision == {
        "allowed": False,
        "performed": False,
        "reason": "audit_unavailable",
    }

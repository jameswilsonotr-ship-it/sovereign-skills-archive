from sms_safety import (
    REDACTED,
    REDACTED_BODY,
    REDACTED_PHONE,
    SmsPolicy,
    SmsSenderStub,
    redact_mapping,
)


def test_sms_is_denied_by_default_without_transport_io():
    sender = SmsSenderStub()

    result = sender.send(
        "+1 (555) 010-0199",
        "Fake test message; do not deliver.",
        metadata={"request_id": "offline-case"},
    )

    assert result.status == "denied"
    assert result.reason == "default_deny"
    assert result.sent is False
    assert len(sender.audit_events) == 1
    assert sender.audit_events[0]["recipient"] == REDACTED_PHONE
    assert sender.audit_events[0]["body"] == REDACTED_BODY


def test_explicit_opt_in_remains_a_local_simulation():
    sender = SmsSenderStub(policy=SmsPolicy(allow_send=True))

    result = sender.send("+15550100199", "Fake test message; do not deliver.")

    assert result.status == "simulated"
    assert result.reason == "offline_stub"
    assert result.sent is False


def test_request_redaction_removes_body_phone_and_nested_secrets():
    sender = SmsSenderStub()

    result = sender.send(
        "+15550100199",
        "A private message containing fake-token-123.",
        metadata={
            "api_key": "fake-key-123",
            "nested": {
                "contact": "+1 555 010 0199",
                "note": "token=fake-token-456",
            },
            "tags": ["secret=fake-secret-789", "safe-label"],
        },
    )

    audit = result.audit_event
    assert audit["body"] == REDACTED_BODY
    assert audit["recipient"] == REDACTED_PHONE
    assert audit["metadata"]["api_key"] == REDACTED
    assert audit["metadata"]["nested"]["contact"] == REDACTED_PHONE
    assert audit["metadata"]["nested"]["note"] == REDACTED
    assert audit["metadata"]["tags"] == [REDACTED, "safe-label"]


def test_redact_mapping_preserves_non_sensitive_structure():
    redacted = redact_mapping(
        {
            "attempt": 1,
            "labels": ["offline", "pytest"],
            "details": {"mode": "stub"},
        }
    )

    assert redacted == {
        "attempt": 1,
        "labels": ["offline", "pytest"],
        "details": {"mode": "stub"},
    }

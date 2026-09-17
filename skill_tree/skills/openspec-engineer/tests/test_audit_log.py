import json

from scripts.audit_log import AuditLogger


def test_audit_log_redacts_sensitive_fields_and_values(tmp_path):
    destination = tmp_path / "audit.jsonl"

    with AuditLogger(destination) as audit:
        audit.record(
            "fixture",
            status="ok",
            token="github_pat_super_secret",
            detail="authorization: Bearer abc123",
        )

    record = json.loads(destination.read_text(encoding="utf-8"))
    assert record["token"] == "[REDACTED]"
    assert "[REDACTED]" in record["detail"]
    assert "super_secret" not in destination.read_text(encoding="utf-8")


def test_audit_log_without_destination_is_a_non_persisting_stub():
    record = AuditLogger().record("fixture", status="ok", value="local")

    assert record["event"] == "fixture"
    assert record["value"] == "local"

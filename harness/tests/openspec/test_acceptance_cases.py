from __future__ import annotations

import json


def _context(sut, key: str = "idem-001", **extra: object) -> dict[str, object]:
    return {
        "trace_id": sut.run.trace_id,
        "session_id": sut.run.session_id,
        "caller": "phone-session-coordinator",
        "idempotency_key": key,
        "side_effect_class": "read",
        **extra,
    }


def test_ct_001_valid_phone_event_normalization(sut):
    event = sut.provider.event(kind="session_started")
    result = sut.provider.ingest(event, sut.provider.sign(event))

    assert result["ok"] is True
    envelope = result["envelope"]
    assert {
        "schema",
        "schema_version",
        "event_id",
        "session_id",
        "trace_id",
        "source",
        "actor",
        "sequence",
        "provenance",
    } <= envelope.keys()


def test_ct_002_provider_event_deduplication(sut):
    event = sut.provider.event()
    signature = sut.provider.sign(event)

    first = sut.provider.ingest(event, signature)
    second = sut.provider.ingest(event, signature)

    assert first["ok"] is True
    assert second == {
        "ok": True,
        "duplicate": True,
        "event_id": event["event_id"],
        "trace_id": event["trace_id"],
    }
    assert [r["kind"] for r in sut.run.records].count("provider.accepted") == 1


def test_ct_003_conflicting_sequence_is_rejected(sut):
    first = sut.provider.event(event_id="evt-001", sequence=7)
    second = sut.provider.event(
        event_id="evt-002",
        sequence=7,
        payload={"text": "different payload"},
    )

    sut.provider.ingest(first, sut.provider.sign(first))
    result = sut.provider.ingest(second, sut.provider.sign(second))

    assert result == {"ok": False, "code": "CONFLICTING_SEQUENCE"}
    assert [r["kind"] for r in sut.run.records].count("provider.accepted") == 1


def test_ct_005_invalid_signature_does_not_ingest_payload(sut):
    event = sut.provider.event(payload={"text": "synthetic private content"})

    result = sut.provider.ingest(event, "not-a-valid-signature")

    assert result == {"ok": False, "code": "INVALID_SIGNATURE"}
    assert sut.provider.events == {}
    assert sut.run.records == []
    assert "synthetic private content" not in json.dumps(sut.run.logs)


def test_ct_008_missing_mcp_context_rejected_before_dispatch(sut):
    result = sut.gateway.call("memory.recall", {"query": "facts"}, {"trace_id": "trace"})

    assert result == {"ok": False, "code": "MISSING_CONTEXT"}
    assert sut.gateway.dispatches == []


def test_ct_009_unknown_normalized_tool_rejected(sut):
    result = sut.gateway.call(
        "model.raw_server_method",
        {},
        _context(sut),
    )

    assert result == {"ok": False, "code": "UNKNOWN_TOOL"}
    assert sut.gateway.dispatches == []


def test_ct_010_receipt_schema(sut):
    receipt = sut.store.write(
        "durable://artifact-001",
        {"result": "stub"},
        written_by="olivia",
    )

    assert {
        "receipt_id",
        "trace_id",
        "artifact_ref",
        "content_sha256",
        "written_by",
        "written_at",
        "parent_refs",
        "status",
    } <= receipt.keys()
    assert receipt["status"] == "VERIFIED"


def test_ph_002_denied_consent_stays_out_of_memory(sut):
    event = sut.provider.event(
        event_id="evt-denied",
        consent="denied",
        payload={"text": "do not retain"},
    )
    sut.provider.ingest(event, sut.provider.sign(event))

    result = sut.memory.write(
        "Recall",
        {"text": "do not retain"},
        ["evt-denied"],
        consent="denied",
    )

    assert result == {"ok": False, "code": "CONSENT_REQUIRED"}
    assert sut.memory.writes == []


def test_ph_004_partial_transcript_cannot_mutate(sut):
    sut.phone.partial("delete the archive")

    assert sut.gateway.dispatches == []
    assert sut.run.timeline == ["phone.partial"]


def test_ph_005_exact_confirmation_executes_once(sut):
    action_id = sut.phone.propose_mutation("durable://target", {"state": "changed"})

    result = sut.phone.confirm(action_id, "yes", now=10)

    assert result["ok"] is True
    assert len(sut.gateway.dispatches) == 1
    assert sut.phone.confirm(action_id, "yes", now=10)["code"] == "ACTION_CLOSED"
    assert len(sut.gateway.dispatches) == 1


def test_ph_007_stale_confirmation_has_no_side_effect(sut):
    action_id = sut.phone.propose_mutation("durable://target", {"state": "changed"})

    result = sut.phone.confirm(action_id, "yes", now=11)

    assert result == {"ok": False, "code": "STALE_CONFIRMATION"}
    assert sut.gateway.dispatches == []


def test_ph_013_secret_redaction_across_evidence_paths(sut):
    event = sut.provider.event(
        payload={"text": "provider-secret and mcp-secret must not persist"}
    )
    sut.provider.ingest(event, sut.provider.sign(event))
    sut.gateway.call(
        "memory.recall",
        {"query": "mcp-secret"},
        _context(sut, key="redaction-001"),
    )
    sut.store.write("durable://redacted", {"token": "provider-secret"})

    evidence = json.dumps(
        {
            "events": sut.provider.events,
            "dispatches": sut.gateway.dispatches,
            "items": sut.store.items,
            "receipts": sut.store.receipts(),
            "logs": sut.run.logs,
        }
    )
    assert "provider-secret" not in evidence
    assert "mcp-secret" not in evidence
    assert not sut.run.has_secret()


def test_mcp_006_idempotent_tool_call(sut):
    args = {"query": "same request"}
    first = sut.gateway.call("memory.recall", args, _context(sut, "idem-006"))
    second = sut.gateway.call("memory.recall", args, _context(sut, "idem-006"))

    assert first["ok"] is True
    assert second["replayed"] is True
    assert len(sut.gateway.dispatches) == 1


def test_mcp_008_downstream_timeout_is_retryable_not_success(sut):
    result = sut.gateway.call(
        "memory.recall",
        {"simulate_timeout": True},
        _context(sut, "timeout-008"),
    )

    assert result["ok"] is False
    assert result["code"] == "DOWNSTREAM_TIMEOUT"
    assert result["retryable"] is True
    assert sut.gateway.dispatches == []
    assert sut.store.receipts() == []


def test_lt_006_memory_write_requires_provenance(sut):
    result = sut.memory.write("Archival", {"fact": "unproven"}, [])

    assert result == {"ok": False, "code": "PROVENANCE_REQUIRED"}
    assert sut.memory.writes == []


def test_es_001_durable_before_wake_ordering(sut):
    request_id = sut.router.submit()

    assert sut.run.timeline == ["artifact.write", "queue.append", "handoff.set"]
    sut.router.wake(request_id)
    assert sut.run.timeline[-1] == "wake.send"


def test_es_006_duplicate_wake_is_idempotent(sut):
    request_id = sut.router.submit()

    first = sut.router.wake(request_id)
    second = sut.router.wake(request_id)

    assert first == {"ok": True, "duplicate": False}
    assert second == {"ok": True, "duplicate": True}
    assert sut.router.worker_runs[request_id] == 1


def test_es_016_stub_source_remains_unresolved(sut):
    request_id = sut.router.submit(
        sources=[{"ref": "durable://empty-stub", "content": ""}]
    )

    result = sut.router.run_worker(request_id)

    assert result["disposition"] == "needs-human"
    assert result["unresolved_refs"] == ["durable://empty-stub"]
    assert "fabricated" not in result["summary"]


def test_es_017_source_conflict_is_returned_with_refs(sut):
    request_id = sut.router.submit(
        sources=[
            {"ref": "durable://source-a", "content": "approve"},
            {"ref": "durable://source-b", "content": "reject"},
        ]
    )

    result = sut.router.run_worker(request_id)

    assert result["disposition"] == "needs-human"
    assert result["conflict_refs"] == [
        "durable://source-a",
        "durable://source-b",
    ]


def test_op_007_trace_continuity_across_escalation(sut):
    event = sut.provider.event()
    sut.provider.ingest(event, sut.provider.sign(event))
    sut.gateway.call("memory.recall", {"query": "trace"}, _context(sut, "trace-007"))
    request_id = sut.router.submit(trace_id=event["trace_id"])
    sut.router.wake(request_id)

    assert sut.run.records
    assert all(record["trace_id"] == event["trace_id"] for record in sut.run.records)

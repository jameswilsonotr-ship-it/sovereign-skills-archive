"""OpenSpec case catalog and deterministic scenario templates."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from .scenario_schema import SCHEMA, SCHEMA_VERSION


@dataclass(frozen=True)
class CaseDefinition:
    source_case: str
    family: str
    title: str
    operation: str
    outcome: str
    code: str | None = None
    invariants: tuple[str, ...] = ()


def _case(
    source_case: str,
    family: str,
    title: str,
    operation: str,
    outcome: str = "accepted",
    code: str | None = None,
    *invariants: str,
) -> CaseDefinition:
    return CaseDefinition(
        source_case,
        family,
        title,
        operation,
        outcome,
        code,
        invariants,
    )


# This is the 80-case catalog in docs/openspec/04-acceptance-tests.md.  Keeping
# the catalog here makes the generated corpus independent of Markdown parsing.
CASES: tuple[CaseDefinition, ...] = (
    _case("CT-001", "contract", "Valid phone event normalization", "provider.ingest", "accepted", None, "canonical_envelope"),
    _case("CT-002", "contract", "Provider event deduplication", "provider.replay", "duplicate", "DUPLICATE_EVENT", "idempotent_replay"),
    _case("CT-003", "contract", "Conflicting sequence number", "provider.ingest", "rejected", "CONFLICTING_SEQUENCE", "sequence_integrity"),
    _case("CT-004", "contract", "Unknown event type", "provider.ingest", "rejected", "UNKNOWN_EVENT", "typed_failure"),
    _case("CT-005", "contract", "Invalid signature", "provider.verify", "rejected", "INVALID_SIGNATURE", "payload_not_logged"),
    _case("CT-006", "contract", "Schema version mismatch", "provider.validate", "rejected", "SCHEMA_VERSION_MISMATCH", "no_silent_downgrade"),
    _case("CT-007", "contract", "OpenAI/Gemini schema parity", "gateway.describe", "accepted", None, "schema_parity"),
    _case("CT-008", "contract", "Missing MCP context", "gateway.call", "rejected", "MISSING_CONTEXT", "pre_dispatch_rejection"),
    _case("CT-009", "contract", "Unknown normalized tool", "gateway.call", "rejected", "UNKNOWN_TOOL", "pre_dispatch_rejection"),
    _case("CT-010", "contract", "Receipt schema", "artifact.write", "accepted", None, "receipt_proof"),
    _case("PH-001", "phone_safety", "Consent granted", "session.open", "accepted", None, "consent_boundary"),
    _case("PH-002", "phone_safety", "Consent denied", "memory.write", "rejected", "CONSENT_REQUIRED", "consent_boundary"),
    _case("PH-003", "phone_safety", "Consent unknown", "memory.write", "staged", "CONSENT_REQUIRED", "consent_boundary"),
    _case("PH-004", "phone_safety", "Partial transcript", "phone.partial", "staged", None, "no_partial_mutation"),
    _case("PH-005", "phone_safety", "Exact confirmation", "phone.confirm", "accepted", None, "exact_confirmation"),
    _case("PH-006", "phone_safety", "Ambiguous confirmation", "phone.confirm", "rejected", "AMBIGUOUS_CONFIRMATION", "exact_confirmation"),
    _case("PH-007", "phone_safety", "Stale confirmation", "phone.confirm", "rejected", "STALE_CONFIRMATION", "expiry_enforced"),
    _case("PH-008", "phone_safety", "Cancellation", "phone.cancel", "rejected", "CANCELLED", "no_unapproved_write"),
    _case("PH-009", "phone_safety", "Barge-in", "phone.interrupt", "staged", "INTERRUPTED", "turn_boundary"),
    _case("PH-010", "phone_safety", "Disconnect during read", "session.close", "staged", "DISCONNECTED", "no_false_completion"),
    _case("PH-011", "phone_safety", "Disconnect before mutation", "session.close", "rejected", "DISCONNECTED", "no_unapproved_write"),
    _case("PH-012", "phone_safety", "Provider timeout", "provider.ack", "retryable", "PROVIDER_TIMEOUT", "typed_failure"),
    _case("PH-013", "phone_safety", "Secret redaction", "evidence.redact", "accepted", None, "no_secret_leakage"),
    _case("PH-014", "phone_safety", "Session close", "session.close", "accepted", None, "receipt_proof"),
    _case("MCP-001", "mcp", "Stdio to remote bridge", "gateway.bridge", "accepted", None, "transport_normalization"),
    _case("MCP-002", "mcp", "Remote to stdio bridge", "gateway.bridge", "accepted", None, "transport_normalization"),
    _case("MCP-003", "mcp", "Capability discovery", "gateway.capabilities", "accepted", None, "least_privilege"),
    _case("MCP-004", "mcp", "Read scope", "memory.recall", "accepted", None, "least_privilege"),
    _case("MCP-005", "mcp", "Write scope", "gateway.call", "rejected", "SCOPE_DENIED", "pre_dispatch_rejection"),
    _case("MCP-006", "mcp", "Idempotent tool call", "gateway.call", "duplicate", "REPLAYED", "idempotent_replay"),
    _case("MCP-007", "mcp", "Conflicting idempotency key", "gateway.call", "rejected", "IDEMPOTENCY_CONFLICT", "idempotency_integrity"),
    _case("MCP-008", "mcp", "Downstream timeout", "gateway.call", "retryable", "DOWNSTREAM_TIMEOUT", "typed_failure"),
    _case("MCP-009", "mcp", "Downstream malformed response", "gateway.call", "rejected", "MALFORMED_RESPONSE", "typed_failure"),
    _case("MCP-010", "mcp", "Rate limit", "gateway.call", "retryable", "RATE_LIMITED", "bounded_work"),
    _case("MCP-011", "mcp", "Credential rotation", "gateway.rotate", "accepted", None, "credential_boundary"),
    _case("MCP-012", "mcp", "Health endpoints", "health.check", "accepted", None, "readiness_boundary"),
    _case("LT-001", "memory", "Core read", "memory.core.read", "accepted", None, "tier_explicit"),
    _case("LT-002", "memory", "Recall search", "memory.recall", "accepted", None, "tier_explicit"),
    _case("LT-003", "memory", "Archival search", "memory.archival.search", "accepted", None, "tier_explicit"),
    _case("LT-004", "memory", "Core protection", "memory.core.propose", "staged", "APPROVAL_REQUIRED", "approval_boundary"),
    _case("LT-005", "memory", "Approved Core patch", "memory.core.patch", "accepted", None, "approval_boundary"),
    _case("LT-006", "memory", "Provenance-required write", "memory.write", "rejected", "PROVENANCE_REQUIRED", "provenance_required"),
    _case("LT-007", "memory", "Sensitive fact", "memory.archive", "staged", "APPROVAL_REQUIRED", "sensitive_retention"),
    _case("LT-008", "memory", "Deduplicated Archival item", "memory.archive", "duplicate", "DUPLICATE_CONTENT", "idempotent_replay"),
    _case("LT-009", "memory", "Index loss", "memory.restore", "accepted", None, "source_of_truth"),
    _case("LT-010", "memory", "Embedding mismatch", "memory.search", "rejected", "EMBEDDING_MISMATCH", "version_boundary"),
    _case("LT-011", "memory", "Spark client runtime", "runtime.validate", "accepted", None, "runtime_boundary"),
    _case("LT-012", "memory", "Bounded results", "memory.search", "accepted", None, "bounded_work"),
    _case("ES-001", "escalation", "Durable-before-wake ordering", "router.submit", "accepted", None, "durable_before_wake"),
    _case("ES-002", "escalation", "Valid Spark request", "worker.validate", "accepted", None, "bounded_handoff"),
    _case("ES-003", "escalation", "Completed result", "worker.complete", "accepted", None, "receipt_proof"),
    _case("ES-004", "escalation", "Partial result", "worker.complete", "staged", "PARTIAL_RESULT", "no_false_completion"),
    _case("ES-005", "escalation", "Missing payload", "worker.read", "rejected", "MISSING_PAYLOAD", "no_fabrication"),
    _case("ES-006", "escalation", "Duplicate wake", "router.wake", "duplicate", "DUPLICATE_WAKE", "idempotent_replay"),
    _case("ES-007", "escalation", "Wake unavailable", "router.wake", "retryable", "WAKE_UNAVAILABLE", "durable_recovery"),
    _case("ES-008", "escalation", "Spark unavailable", "worker.dispatch", "retryable", "WORKER_UNAVAILABLE", "durable_recovery"),
    _case("ES-009", "escalation", "Expired deadline", "worker.dispatch", "rejected", "DEADLINE_EXPIRED", "deadline_enforced"),
    _case("ES-010", "escalation", "Approval pending", "router.submit", "staged", "APPROVAL_REQUIRED", "approval_boundary"),
    _case("ES-011", "escalation", "Approval rejected", "router.cancel", "rejected", "APPROVAL_REJECTED", "approval_boundary"),
    _case("ES-012", "escalation", "Approval mismatch", "router.dispatch", "rejected", "APPROVAL_MISMATCH", "approval_boundary"),
    _case("ES-013", "escalation", "Worker ownership", "artifact.write", "rejected", "OWNERSHIP_DENIED", "ownership_boundary"),
    _case("ES-014", "escalation", "TQS status", "queue.status", "accepted", None, "status_validity"),
    _case("ES-015", "escalation", "No ACK-of-ACK", "queue.ack", "accepted", None, "bounded_handoff"),
    _case("ES-016", "escalation", "Stub source", "worker.complete", "staged", "UNRESOLVED_SOURCE", "no_fabrication"),
    _case("ES-017", "escalation", "Source conflict", "worker.complete", "staged", "SOURCE_CONFLICT", "conflict_visible"),
    _case("ES-018", "escalation", "Retry attempt", "worker.retry", "retryable", "RETRY_ATTEMPT", "idempotent_replay"),
    _case("ES-019", "escalation", "Caller disconnect", "router.submit", "staged", "DISCONNECTED", "no_implicit_approval"),
    _case("ES-020", "escalation", "Receipt failure", "receipt.write", "retryable", "RECEIPT_UNVERIFIED", "receipt_proof"),
    _case("OP-001", "operations", "Process restart", "recovery.restart", "staged", "RECOVERY_REQUIRED", "durable_recovery"),
    _case("OP-002", "operations", "Store unavailable", "health.check", "retryable", "STORE_UNAVAILABLE", "readiness_boundary"),
    _case("OP-003", "operations", "Restore from backup", "recovery.restore", "accepted", None, "source_of_truth"),
    _case("OP-004", "operations", "TLS/auth boundary", "network.authorize", "rejected", "ROUTE_DENIED", "private_route"),
    _case("OP-005", "operations", "Least privilege", "gateway.capabilities", "accepted", None, "least_privilege"),
    _case("OP-006", "operations", "Log scan", "evidence.scan", "accepted", None, "no_secret_leakage"),
    _case("OP-007", "operations", "Trace continuity", "trace.verify", "accepted", None, "trace_continuity"),
    _case("OP-008", "operations", "Artifact hash", "artifact.verify", "rejected", "HASH_MISMATCH", "content_integrity"),
    _case("OP-009", "operations", "Backup index rebuild", "recovery.reindex", "accepted", None, "source_of_truth"),
    _case("OP-010", "operations", "Configuration drift", "health.config", "rejected", "CONFIG_INVALID", "readiness_boundary"),
    _case("OP-011", "operations", "Rate/timeout budget", "queue.backpressure", "retryable", "BACKPRESSURE", "bounded_work"),
    _case("OP-012", "operations", "Manual wake mode", "router.stage", "staged", "MANUAL_WAKE_REQUIRED", "durable_recovery"),
)


def build_scenario(case: CaseDefinition, variant: int, seed: int) -> dict[str, Any]:
    """Build one data-only scenario from a catalog entry and variant number."""

    digest = hashlib.sha256(f"{seed}:{case.source_case}:{variant}".encode()).hexdigest()
    scenario_id = f"OS-{case.source_case}-{variant:04d}"
    step_args = {
        "fixture": f"synthetic-{digest[:16]}",
        "variant": variant,
        "trace_id": f"trace-{digest[16:28]}",
        "external_io": "disabled",
    }
    invariants = [
        "deterministic_fixture",
        "offline_only",
        "synthetic_data",
        "no_unapproved_side_effect",
        *case.invariants,
    ]
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "scenario_id": scenario_id,
        "source_case": case.source_case,
        "family": case.family,
        "variant": variant,
        "seed": seed,
        "setup": {
            "title": case.title,
            "fixture": f"synthetic-{digest[:16]}",
            "clock": "controlled",
            "credentials": "synthetic-only",
            "external_io": "disabled",
        },
        "steps": [{"op": case.operation, "args": step_args}],
        "expected": {"outcome": case.outcome, "code": case.code},
        "invariants": list(dict.fromkeys(invariants)),
        "forbidden_effects": [
            "external_network",
            "subprocess",
            "real_credentials",
            "model_call",
            "unapproved_write",
            "raw_secret_persistence",
        ],
        "status": "stub",
    }

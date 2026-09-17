"""Deterministic, in-process doubles for the OpenSpec acceptance cases.

The doubles deliberately model boundaries rather than production integrations:
there are no sockets, subprocesses, credentials, or model calls here.
"""

from __future__ import annotations

import copy
import hashlib
import hmac
import json
from dataclasses import dataclass, field
from typing import Any


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def redact(value: Any, secrets: tuple[str, ...]) -> Any:
    if isinstance(value, dict):
        return {key: redact(item, secrets) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item, secrets) for item in value]
    if isinstance(value, str):
        for secret in secrets:
            value = value.replace(secret, "[REDACTED]")
        return value
    return value


@dataclass
class TestRun:
    """Small evidence ledger shared by every fake in one isolated test."""

    run_id: str = "test-run-001"
    trace_id: str = "trace-test-001"
    session_id: str = "ses-test-001"
    secrets: tuple[str, ...] = ("provider-secret", "mcp-secret")
    records: list[dict[str, Any]] = field(default_factory=list)
    logs: list[dict[str, Any]] = field(default_factory=list)
    timeline: list[str] = field(default_factory=list)

    def record(self, kind: str, **fields: Any) -> dict[str, Any]:
        entry = redact({"kind": kind, **fields}, self.secrets)
        self.records.append(entry)
        self.timeline.append(kind)
        return entry

    def log(self, message: str, **fields: Any) -> None:
        self.logs.append(redact({"message": message, **fields}, self.secrets))

    def has_secret(self) -> bool:
        haystack = canonical({"records": self.records, "logs": self.logs})
        return any(secret in haystack for secret in self.secrets)


class FakeStore:
    def __init__(self, run: TestRun) -> None:
        self.run = run
        self.items: dict[str, Any] = {}
        self._receipt_number = 0
        self._receipts: list[dict[str, Any]] = []

    def write(
        self,
        ref: str,
        payload: Any,
        *,
        written_by: str = "olivia",
        trace_id: str | None = None,
        parent_refs: list[str] | None = None,
        status: str = "VERIFIED",
    ) -> dict[str, Any]:
        safe_payload = redact(copy.deepcopy(payload), self.run.secrets)
        self.items[ref] = safe_payload
        digest = hashlib.sha256(canonical(safe_payload).encode()).hexdigest()
        self._receipt_number += 1
        receipt = {
            "receipt_id": f"rcpt-{self._receipt_number:03d}",
            "trace_id": trace_id or self.run.trace_id,
            "artifact_ref": ref,
            "content_sha256": digest,
            "written_by": written_by,
            "written_at": "2026-01-01T00:00:00Z",
            "parent_refs": parent_refs or [],
            "status": status,
        }
        self._receipts.append(redact(receipt, self.run.secrets))
        self.run.record("artifact.write", trace_id=receipt["trace_id"], ref=ref)
        return receipt

    def read(self, ref: str) -> Any:
        return copy.deepcopy(self.items[ref])

    def receipts(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._receipts)


class FakeProvider:
    """Signed callback verifier with replay and sequence protection."""

    def __init__(self, run: TestRun) -> None:
        self.run = run
        self.secret = "provider-secret"
        self.events: dict[str, dict[str, Any]] = {}
        self.sequence_digests: dict[tuple[str, int], str] = {}

    def event(
        self,
        kind: str = "utterance",
        *,
        event_id: str = "evt-001",
        sequence: int = 1,
        trace_id: str | None = None,
        payload: dict[str, Any] | None = None,
        consent: str = "granted",
    ) -> dict[str, Any]:
        return {
            "schema": "sovereign.phone.event",
            "schema_version": "0.1.0",
            "event_id": event_id,
            "session_id": self.run.session_id,
            "trace_id": trace_id or self.run.trace_id,
            "occurred_at": "2026-01-01T00:00:00Z",
            "source": {
                "kind": "phone",
                "provider": "fake-provider",
                "channel": "voice",
                "account_ref": "opaque-fake-account",
            },
            "actor": {"kind": "human", "consent": consent},
            "payload": {"kind": kind, "text": "hello", **(payload or {})},
            "policy": {
                "retention_class": "session",
                "requires_confirmation": False,
            },
            "provenance": {"parent_event_ids": [], "content_sha256": None},
            "sequence": sequence,
        }

    def sign(self, event: dict[str, Any]) -> str:
        return hmac.new(
            self.secret.encode(), canonical(event).encode(), hashlib.sha256
        ).hexdigest()

    def ingest(self, event: dict[str, Any], signature: str) -> dict[str, Any]:
        expected = self.sign(event)
        if not hmac.compare_digest(signature, expected):
            self.run.log(
                "invalid provider signature",
                event_id=event.get("event_id", "opaque"),
            )
            return {"ok": False, "code": "INVALID_SIGNATURE"}

        event_id = event["event_id"]
        digest = hashlib.sha256(canonical(event).encode()).hexdigest()
        sequence_key = (event["session_id"], event["sequence"])
        previous_sequence = self.sequence_digests.get(sequence_key)
        if previous_sequence and previous_sequence != digest:
            self.run.record(
                "security.sequence_conflict",
                trace_id=event["trace_id"],
                event_id=event_id,
            )
            return {"ok": False, "code": "CONFLICTING_SEQUENCE"}
        if event_id in self.events:
            return {
                "ok": True,
                "duplicate": True,
                "event_id": event_id,
                "trace_id": self.events[event_id]["trace_id"],
            }

        safe_event = redact(copy.deepcopy(event), self.run.secrets)
        self.events[event_id] = safe_event
        self.sequence_digests[sequence_key] = digest
        self.run.record(
            "provider.accepted",
            event_id=event_id,
            trace_id=event["trace_id"],
            sequence=event["sequence"],
        )
        return {
            "ok": True,
            "duplicate": False,
            "event_id": event_id,
            "trace_id": event["trace_id"],
            "envelope": safe_event,
        }


class FakeGateway:
    """Policy-aware normalized tool surface with idempotency."""

    def __init__(self, run: TestRun, store: FakeStore) -> None:
        self.run = run
        self.store = store
        self.allowlist = {"memory.recall": "read", "artifact.write": "write"}
        self.dispatches: list[dict[str, Any]] = []
        self._idempotency: dict[str, tuple[str, str, dict[str, Any]]] = {}

    def call(
        self,
        tool: str,
        args: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        required = ("trace_id", "session_id", "caller", "idempotency_key")
        if any(not context.get(key) for key in required):
            return {"ok": False, "code": "MISSING_CONTEXT"}
        if tool not in self.allowlist:
            return {"ok": False, "code": "UNKNOWN_TOOL"}

        key = context["idempotency_key"]
        args_digest = hashlib.sha256(canonical(args).encode()).hexdigest()
        prior = self._idempotency.get(key)
        if prior:
            prior_tool, prior_digest, prior_result = prior
            if prior_tool != tool or prior_digest != args_digest:
                return {"ok": False, "code": "IDEMPOTENCY_CONFLICT"}
            return {**prior_result, "replayed": True}

        if args.get("simulate_timeout"):
            result = {
                "ok": False,
                "code": "DOWNSTREAM_TIMEOUT",
                "retryable": True,
                "trace_id": context["trace_id"],
            }
            self._idempotency[key] = (tool, args_digest, result)
            return result

        if self.allowlist[tool] == "write" and not context.get("confirmed"):
            return {
                "ok": False,
                "code": "CONFIRMATION_REQUIRED",
                "retryable": False,
            }

        safe_args = redact(copy.deepcopy(args), self.run.secrets)
        self.dispatches.append({"tool": tool, "args": safe_args, "context": context})
        self.run.record("gateway.dispatch", trace_id=context["trace_id"], tool=tool)
        if tool == "memory.recall":
            result = {
                "ok": True,
                "trace_id": context["trace_id"],
                "result": {"tier": "Recall", "items": []},
            }
        else:
            receipt = self.store.write(
                args["ref"],
                args.get("value", {}),
                written_by=context["caller"],
                trace_id=context["trace_id"],
            )
            result = {
                "ok": True,
                "trace_id": context["trace_id"],
                "receipt_ref": receipt["receipt_id"],
            }
        self._idempotency[key] = (tool, args_digest, result)
        return result


class FakeMemory:
    def __init__(self, run: TestRun) -> None:
        self.run = run
        self.writes: list[dict[str, Any]] = []

    def write(
        self,
        tier: str,
        value: Any,
        source_refs: list[str] | None,
        *,
        consent: str = "granted",
    ) -> dict[str, Any]:
        if consent != "granted":
            return {"ok": False, "code": "CONSENT_REQUIRED"}
        if not source_refs:
            return {"ok": False, "code": "PROVENANCE_REQUIRED"}
        entry = {
            "tier": tier,
            "value": redact(value, self.run.secrets),
            "source_refs": source_refs,
        }
        self.writes.append(entry)
        self.run.record("memory.write", trace_id=self.run.trace_id, tier=tier)
        return {"ok": True, "entry": entry}


class FakePhoneSession:
    def __init__(self, run: TestRun, gateway: FakeGateway) -> None:
        self.run = run
        self.gateway = gateway
        self.pending: dict[str, dict[str, Any]] = {}
        self._action_number = 0

    def partial(self, text: str) -> None:
        self.run.record(
            "phone.partial",
            trace_id=self.run.trace_id,
            text=text,
        )

    def propose_mutation(self, ref: str, value: Any, *, expires_at: int = 10) -> str:
        self._action_number += 1
        action_id = f"action-{self._action_number:03d}"
        self.pending[action_id] = {
            "ref": ref,
            "value": value,
            "expires_at": expires_at,
            "closed": False,
        }
        self.run.record(
            "phone.confirmation_requested",
            trace_id=self.run.trace_id,
            action_id=action_id,
        )
        return action_id

    def confirm(self, action_id: str, answer: str, *, now: int) -> dict[str, Any]:
        action = self.pending[action_id]
        if action["closed"]:
            return {"ok": False, "code": "ACTION_CLOSED"}
        if answer == "cancel":
            action["closed"] = True
            return {"ok": False, "code": "CANCELLED"}
        if answer != "yes":
            return {"ok": False, "code": "AMBIGUOUS_CONFIRMATION"}
        if now > action["expires_at"]:
            action["closed"] = True
            return {"ok": False, "code": "STALE_CONFIRMATION"}
        result = self.gateway.call(
            "artifact.write",
            {"ref": action["ref"], "value": action["value"]},
            {
                "trace_id": self.run.trace_id,
                "session_id": self.run.session_id,
                "caller": "phone",
                "idempotency_key": action_id,
                "side_effect_class": "write",
                "confirmed": True,
            },
        )
        action["closed"] = True
        return result


class FakeRouter:
    def __init__(self, run: TestRun, store: FakeStore) -> None:
        self.run = run
        self.store = store
        self.requests: dict[str, dict[str, Any]] = {}
        self.wake_calls: list[str] = []
        self.worker_runs: dict[str, int] = {}
        self._request_number = 0

    def submit(
        self,
        *,
        trace_id: str | None = None,
        sources: list[dict[str, str]] | None = None,
    ) -> str:
        self._request_number += 1
        request_id = f"esc-{self._request_number:03d}"
        request_trace = trace_id or self.run.trace_id
        payload_ref = f"durable://{request_id}"
        payload = {"request_id": request_id, "sources": sources or []}
        self.store.write(
            payload_ref,
            payload,
            written_by="olivia",
            trace_id=request_trace,
        )
        self.run.record("queue.append", trace_id=request_trace, request_id=request_id)
        self.run.record(
            "handoff.set",
            trace_id=request_trace,
            request_id=request_id,
            status="AWAITING_VESPER",
        )
        self.requests[request_id] = {
            "trace_id": request_trace,
            "payload_ref": payload_ref,
            "sources": sources or [],
        }
        return request_id

    def wake(self, request_id: str) -> dict[str, Any]:
        if request_id in self.wake_calls:
            return {"ok": True, "duplicate": True}
        self.wake_calls.append(request_id)
        self.run.record(
            "wake.send",
            trace_id=self.requests[request_id]["trace_id"],
            request_id=request_id,
        )
        self.worker_runs[request_id] = self.worker_runs.get(request_id, 0) + 1
        return {"ok": True, "duplicate": False}

    def run_worker(self, request_id: str) -> dict[str, Any]:
        request = self.requests[request_id]
        sources = request["sources"]
        empty = [source["ref"] for source in sources if not source.get("content")]
        if empty:
            return {
                "disposition": "needs-human",
                "unresolved_refs": empty,
                "summary": "Source stub remains unresolved",
            }
        contents = {source.get("content") for source in sources}
        if len(contents) > 1:
            return {
                "disposition": "needs-human",
                "conflict_refs": [source["ref"] for source in sources],
                "summary": "Conflicting sources require review",
            }
        return {"disposition": "completed", "summary": "Bounded result"}


class StubHarness:
    def __init__(self) -> None:
        self.run = TestRun()
        self.store = FakeStore(self.run)
        self.provider = FakeProvider(self.run)
        self.gateway = FakeGateway(self.run, self.store)
        self.memory = FakeMemory(self.run)
        self.phone = FakePhoneSession(self.run, self.gateway)
        self.router = FakeRouter(self.run, self.store)


class _UnimplementedProxy:
    def __getattr__(self, name: str) -> "_UnimplementedProxy":
        return self

    def __call__(self, *_args: Any, **_kwargs: Any) -> Any:
        raise NotImplementedError("OpenSpec system under test is not implemented")


class UnimplementedHarness(_UnimplementedProxy):
    """Red-phase backend used to prove the acceptance tests are meaningful."""

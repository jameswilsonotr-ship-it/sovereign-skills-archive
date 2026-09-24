"""Test-only stubs for the offline flashlight contract.

These objects model authorization and audit behavior only.  They deliberately
have no backend, file handle, subprocess, socket, or platform-device access.
"""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


SUPPORTED_ACTIONS = frozenset(("on", "off", "status"))


@dataclass(frozen=True)
class AuditEvent:
    """The complete, non-sensitive audit record emitted by the stub."""

    event: str
    action: str
    outcome: str
    reason: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "event": self.event,
            "action": self.action,
            "outcome": self.outcome,
            "reason": self.reason,
        }


class RecordingAuditSink:
    """In-memory audit sink used by tests."""

    def __init__(self) -> None:
        self.events: List[Dict[str, str]] = []

    def __call__(self, event: AuditEvent) -> None:
        self.events.append(event.as_dict())


class FailingAuditSink:
    """Audit failure double; fail-closed behavior must not expose its error."""

    def __call__(self, event: AuditEvent) -> None:
        raise RuntimeError("synthetic audit sink failure")


class OfflineFlashlightStub:
    """Authorize simulated flashlight requests without performing them.

    The allow-list is intentionally empty by default.  Even when an action is
    explicitly allowed, the return value only records an authorization
    decision; it never claims that a physical flashlight was changed.
    """

    def __init__(
        self,
        *,
        allowed_actions: Iterable[str] = (),
        audit_sink: Optional[Any] = None,
    ) -> None:
        self._allowed_actions = frozenset(allowed_actions)
        self._audit_sink = audit_sink or RecordingAuditSink()

    @property
    def audit_sink(self) -> Any:
        return self._audit_sink

    def request(self, action: Any, *, intensity: Optional[int] = None) -> Dict[str, Any]:
        """Return an offline authorization decision for one request."""

        normalized_action = (
            action
            if isinstance(action, str) and action in SUPPORTED_ACTIONS
            else None
        )
        audit_action = normalized_action or "<unknown>"

        if normalized_action is None:
            return self._deny(
                audit_action,
                reason="unsupported_action",
            )

        if intensity is not None and (
            not isinstance(intensity, int) or isinstance(intensity, bool)
        ):
            return self._deny(
                normalized_action,
                reason="invalid_intensity",
            )

        if normalized_action not in self._allowed_actions:
            return self._deny(
                normalized_action,
                reason="capability_not_granted",
            )

        return self._decide(
            AuditEvent(
                event="flashlight.authorization",
                action=normalized_action,
                outcome="allowed",
                reason="explicit_capability",
            ),
            allowed=True,
        )

    def _deny(self, action: str, *, reason: str) -> Dict[str, Any]:
        return self._decide(
            AuditEvent(
                event="flashlight.authorization",
                action=action,
                outcome="denied",
                reason=reason,
            ),
            allowed=False,
        )

    def _decide(self, event: AuditEvent, *, allowed: bool) -> Dict[str, Any]:
        try:
            self._audit_sink(event)
        except Exception:
            # An unavailable audit path must never turn into an authorization.
            return {
                "allowed": False,
                "performed": False,
                "reason": "audit_unavailable",
            }

        return {
            "allowed": allowed,
            "performed": False,
            "reason": event.reason,
        }

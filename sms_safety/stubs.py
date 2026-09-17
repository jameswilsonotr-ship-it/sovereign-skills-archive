"""No-I/O SMS policy and redaction stubs.

The sender in this module is deliberately not a transport adapter. It records
only redacted audit data and reports whether an attempt was denied or
simulated. A future provider integration must be introduced separately and
must not be inferred from this stub.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Mapping

REDACTED = "[REDACTED]"
REDACTED_BODY = "[REDACTED_BODY]"
REDACTED_PHONE = "[REDACTED_PHONE]"

_PHONE_RE = re.compile(r"(?<!\w)(?:\+?[\d][\d().\-\s]{6,}[\d])(?!\w)")
_SENSITIVE_KEY_RE = re.compile(
    r"(?:authorization|api[_-]?key|password|secret|token|credential)",
    re.IGNORECASE,
)


def redact_phone(_value: str) -> str:
    """Return a stable placeholder instead of retaining a phone number."""

    return REDACTED_PHONE


def _redact_text(value: str) -> str:
    """Remove phone-like values and secret assignments from diagnostic text."""

    value = _PHONE_RE.sub(REDACTED_PHONE, value)
    return re.sub(
        r"(?i)\b(?:authorization|api[_-]?key|password|secret|token|credential)"
        r"(\s*[:=]\s*)[^\s,;]+",
        REDACTED,
        value,
    )


def redact_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively redact sensitive mapping keys and phone-like strings."""

    redacted: dict[str, Any] = {}
    for key, item in value.items():
        if _SENSITIVE_KEY_RE.search(str(key)):
            redacted[str(key)] = REDACTED
        elif isinstance(item, Mapping):
            redacted[str(key)] = redact_mapping(item)
        elif isinstance(item, list):
            redacted[str(key)] = [
                redact_mapping(entry)
                if isinstance(entry, Mapping)
                else _redact_text(entry)
                if isinstance(entry, str)
                else entry
                for entry in item
            ]
        elif isinstance(item, str):
            redacted[str(key)] = _redact_text(item)
        else:
            redacted[str(key)] = item
    return redacted


def redact_request(
    *, recipient: str, body: str, metadata: Mapping[str, Any]
) -> dict[str, Any]:
    """Build an audit-safe representation of an SMS request."""

    # The body is always replaced rather than pattern-scanned: message content
    # is private even when it contains no recognizable secret.
    return {
        "recipient": redact_phone(recipient),
        "body": REDACTED_BODY,
        "metadata": redact_mapping(metadata),
    }


@dataclass(frozen=True)
class SmsPolicy:
    """Policy gate for the stub; sending is disabled unless explicitly set."""

    allow_send: bool = False


@dataclass(frozen=True)
class SmsSendResult:
    """Result returned without ever contacting an SMS provider."""

    status: str
    sent: bool
    reason: str
    audit_event: dict[str, Any]


@dataclass
class SmsSenderStub:
    """Offline SMS sender that cannot perform a real send."""

    policy: SmsPolicy = field(default_factory=SmsPolicy)
    audit_events: list[dict[str, Any]] = field(default_factory=list)

    def send(
        self,
        recipient: str,
        body: str,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> SmsSendResult:
        """Deny by default, or report a local simulation when opted in.

        Even with ``allow_send=True``, this class never has a transport and
        always returns ``sent=False``. That makes it safe for offline pytest
        and prevents a test from accidentally delivering a real message.
        """

        metadata = metadata or {}
        audit_event = {
            "event": "sms_send_attempt",
            "status": "denied" if not self.policy.allow_send else "simulated",
            **redact_request(
                recipient=recipient,
                body=body,
                metadata=metadata,
            ),
        }
        self.audit_events.append(audit_event)

        if not self.policy.allow_send:
            return SmsSendResult(
                status="denied",
                sent=False,
                reason="default_deny",
                audit_event=audit_event,
            )

        return SmsSendResult(
            status="simulated",
            sent=False,
            reason="offline_stub",
            audit_event=audit_event,
        )

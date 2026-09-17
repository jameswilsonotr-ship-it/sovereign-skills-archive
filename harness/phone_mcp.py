"""Minimal offline phone MCP stub for SPEC-002 intent tests.

This module deliberately models capability boundaries instead of connecting to
an Android device.  ``health`` is read-only and available by default.
``flashlight`` and ``sms`` are side-effecting intents and are denied unless
the caller explicitly opts into an in-memory simulation.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class OfflinePhoneMCP:
    """A deterministic, in-process phone capability stub.

    No Termux command, subprocess, network request, environment variable, or
    device API is used.  The optional ``allow_side_effects`` switch only
    enables simulated state changes in this object.
    """

    SPEC = "SPEC-002"
    MODE = "offline"

    _INTENT_ALIASES = {
        "health": "health",
        "phone.health": "health",
        "phone_health": "health",
        "flashlight": "flashlight",
        "phone.flashlight": "flashlight",
        "phone_flashlight": "flashlight",
        "sms": "sms",
        "phone.sms": "sms",
        "phone_sms": "sms",
        "send_sms": "sms",
        "phone_send_sms": "sms",
    }

    def __init__(self, *, allow_side_effects: bool = False) -> None:
        self.allow_side_effects = allow_side_effects
        self._flashlight_on = False
        self._sms_outbox: list[dict[str, str]] = []

    def list_tools(self) -> list[dict[str, Any]]:
        """Return an MCP-shaped tool catalog without requiring an MCP SDK."""

        return [
            {
                "name": "phone_health",
                "description": "Read the offline phone stub health state.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            },
            {
                "name": "phone_flashlight",
                "description": "Simulate flashlight state; denied by default.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["on", "off", "toggle"],
                        }
                    },
                    "additionalProperties": False,
                },
            },
            {
                "name": "phone_sms",
                "description": "Simulate SMS enqueueing; denied by default.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "to": {"type": "string"},
                        "body": {"type": "string"},
                    },
                    "required": ["to", "body"],
                    "additionalProperties": False,
                },
            },
        ]

    def handle_intent(self, intent: str, **arguments: Any) -> dict[str, Any]:
        """Handle one SPEC-002 intent and return a JSON-serializable result."""

        normalized = self._INTENT_ALIASES.get(intent)
        if normalized is None:
            return self._error(
                intent=intent,
                code="UNKNOWN_INTENT",
                message=f"Unsupported SPEC-002 intent: {intent}",
            )

        if normalized == "health":
            return self._health()
        if normalized == "flashlight":
            return self._flashlight(arguments.get("action", "toggle"))
        return self._sms(arguments.get("to"), arguments.get("body"))

    def dispatch(self, request: Mapping[str, Any]) -> dict[str, Any]:
        """Dispatch a small MCP-like request envelope.

        Both ``intent`` and ``name`` are accepted to keep adapters thin.
        ``arguments`` and ``params`` are equivalent argument containers.
        Invalid envelopes become structured errors rather than exceptions.
        """

        if not isinstance(request, Mapping):
            return self._error(
                intent=None,
                code="INVALID_REQUEST",
                message="Request must be a mapping.",
            )

        intent = request.get("intent", request.get("name"))
        if not isinstance(intent, str):
            return self._error(
                intent=None,
                code="INVALID_REQUEST",
                message="Request requires a string 'intent' or 'name'.",
            )

        arguments = request.get("arguments", request.get("params", {}))
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, Mapping):
            return self._error(
                intent=intent,
                code="INVALID_REQUEST",
                message="'arguments' must be a mapping.",
            )

        return self.handle_intent(intent, **dict(arguments))

    def call_tool(
        self, name: str, arguments: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        """MCP-client-friendly alias for :meth:`handle_intent`."""

        return self.handle_intent(name, **dict(arguments or {}))

    @property
    def flashlight_on(self) -> bool:
        """Return simulated flashlight state."""

        return self._flashlight_on

    @property
    def sms_outbox(self) -> tuple[dict[str, str], ...]:
        """Return simulated messages without exposing a mutable list."""

        return tuple(self._sms_outbox)

    def _health(self) -> dict[str, Any]:
        return {
            "ok": True,
            "intent": "health",
            "status": "ok",
            "mode": self.MODE,
            "spec": self.SPEC,
            "termux": False,
            "capabilities": {
                "health": True,
                "flashlight": self.allow_side_effects,
                "sms": self.allow_side_effects,
            },
        }

    def _flashlight(self, action: Any) -> dict[str, Any]:
        if not self.allow_side_effects:
            return self._denied("flashlight")
        if action not in {"on", "off", "toggle"}:
            return self._error(
                intent="flashlight",
                code="INVALID_ARGUMENT",
                message="action must be one of: on, off, toggle.",
            )

        if action == "toggle":
            self._flashlight_on = not self._flashlight_on
        else:
            self._flashlight_on = action == "on"
        return {
            "ok": True,
            "intent": "flashlight",
            "mode": self.MODE,
            "simulated": True,
            "state": "on" if self._flashlight_on else "off",
        }

    def _sms(self, recipient: Any, body: Any) -> dict[str, Any]:
        if not self.allow_side_effects:
            return self._denied("sms")
        if not isinstance(recipient, str) or not recipient.strip():
            return self._error(
                intent="sms",
                code="INVALID_ARGUMENT",
                message="to must be a non-empty string.",
            )
        if not isinstance(body, str) or not body.strip():
            return self._error(
                intent="sms",
                code="INVALID_ARGUMENT",
                message="body must be a non-empty string.",
            )

        self._sms_outbox.append({"to": recipient, "body": body})
        return {
            "ok": True,
            "intent": "sms",
            "mode": self.MODE,
            "simulated": True,
            "queued": True,
            "outbox_size": len(self._sms_outbox),
        }

    def _denied(self, intent: str) -> dict[str, Any]:
        return self._error(
            intent=intent,
            code="DEFAULT_DENY",
            message=f"{intent} is disabled by the SPEC-002 offline default-deny policy.",
        )

    def _error(
        self, *, intent: str | None, code: str, message: str
    ) -> dict[str, Any]:
        return {
            "ok": False,
            "intent": intent,
            "mode": self.MODE,
            "error": {"code": code, "message": message},
        }

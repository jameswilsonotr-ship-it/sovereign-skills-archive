"""Offline acceptance tests for SPEC-002.

The repository does not contain the future phone MCP implementation.  This
small in-process harness models the contract boundary so the safety
invariants can be exercised now, without opening a socket, contacting
Tailscale, or requiring Android/Zenoh dependencies.
"""

import json
from dataclasses import dataclass, field
from typing import Any

import pytest


POLICY_VERSION = "phone-default-deny-v1"
PROTOCOL = "phone-mcp/v1"
CREATED_AT = "2026-09-17T04:00:00Z"


@dataclass
class Spy:
    calls: list[dict[str, Any]] = field(default_factory=list)

    def record(self, **event: Any) -> None:
        self.calls.append(event)


@dataclass
class TailscaleProvider:
    addresses: tuple[str, ...] = ()
    interface: str = "tailscale0"

    def eligible_addresses(self) -> tuple[str, ...]:
        return self.addresses


class OfflinePhoneMcp:
    """A deterministic contract double, not a production phone adapter."""

    def __init__(self, tailscale: TailscaleProvider | None = None) -> None:
        self.tailscale = tailscale or TailscaleProvider()
        self.intent_dispatcher = Spy()
        self.zenoh = Spy()
        self.flashlight = Spy()
        self.sms = Spy()
        self.package_resolver = Spy()
        self.audit = Spy()
        self.logs = Spy()
        self.listener = {
            "bind_mode": "tailscale",
            "interface": self.tailscale.interface,
            "addresses": [],
            "port": 8787,
            "wildcard": False,
            "bound": False,
        }
        self.bind_error: str | None = None

    def start_listener(self) -> dict[str, Any]:
        """Bind only to an eligible explicit address; never fall back."""

        addresses = self.tailscale.eligible_addresses()
        if not addresses:
            self.bind_error = "TAILSCALE_UNAVAILABLE"
            return self._result(
                "phone_listener",
                "not_ready",
                "BIND_FAILED",
                request_id="bind-1",
                details={"reason": self.bind_error},
            )

        self.listener.update(
            addresses=[addresses[0]],
            bound=True,
            wildcard=False,
        )
        self.bind_error = None
        return self._result(
            "phone_listener",
            "ready",
            "OK",
            request_id="bind-1",
        )

    def health(self, request_id: str, detail: str = "summary") -> dict[str, Any]:
        del detail  # The offline double always exposes the complete safe view.
        status = "ready" if self.listener["bound"] else "not_ready"
        result = self._result(
            "phone_health",
            status,
            "OK" if status == "ready" else "BIND_FAILED",
            request_id=request_id,
            transport="offline",
        )
        result.update(
            node={
                "lifecycle": "READY",
                "node_id": "offline-burner",
                "session_expires_at": "2026-09-17T04:15:00Z",
            },
            listener=dict(self.listener),
            intents={
                "registry_version": "phone-intents/v1",
                "flashlight": "denied_by_policy",
                "sms": "denied_by_policy",
            },
            zenoh={
                "availability": "unavailable",
                "transport": "offline",
                "simulation_enabled": False,
            },
            capabilities={"health": True, "flashlight": False, "sms": False},
        )
        self._audit(result)
        return result

    def call(
        self, operation: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        if operation == "phone_health":
            return self.health(arguments["request_id"], arguments.get("detail", "summary"))

        schemas = {
            "phone_flashlight": {"request_id", "action"},
            "phone_sms": {"request_id", "recipient", "body"},
        }
        if operation not in schemas:
            return self._result(
                operation,
                "rejected",
                "UNKNOWN_OPERATION",
                request_id=arguments.get("request_id", "generated-1"),
            )

        unknown = set(arguments) - schemas[operation]
        if unknown:
            result = self._result(
                operation,
                "rejected",
                "UNKNOWN_FIELD",
                request_id=arguments.get("request_id", "generated-1"),
                details={"field_count": len(unknown)},
            )
            self._audit(result)
            return result

        request_id = arguments.get("request_id", "generated-1")
        if operation == "phone_flashlight":
            if arguments.get("action") not in {"on", "off", "toggle"}:
                result = self._result(
                    operation,
                    "rejected",
                    "SCHEMA_INVALID",
                    request_id=request_id,
                )
                self._audit(result)
                return result
            result = self._result(
                operation,
                "denied",
                "POLICY_DENIED",
                request_id=request_id,
            )
        else:
            result = self._result(
                operation,
                "denied",
                "POLICY_DENIED",
                request_id=request_id,
            )

        # Policy terminates both named stubs before any adapter or transport.
        self._audit(result)
        self.logs.record(operation=operation, decision=result["code"])
        return result

    def _result(
        self,
        operation: str,
        status: str,
        code: str,
        *,
        request_id: str,
        transport: str = "offline",
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "protocol": PROTOCOL,
            "request_id": request_id,
            "operation": operation,
            "status": status,
            "code": code,
            "transport": transport,
            "policy_version": POLICY_VERSION,
            "created_at": CREATED_AT,
        }
        if details:
            result["details"] = details
        return result

    def _audit(self, result: dict[str, Any]) -> None:
        self.audit.record(
            request_id=result["request_id"],
            operation=result["operation"],
            status=result["status"],
            code=result["code"],
            policy_version=result["policy_version"],
            created_at=result["created_at"],
        )


@pytest.fixture
def ready_phone() -> OfflinePhoneMcp:
    phone = OfflinePhoneMcp(
        TailscaleProvider(addresses=("100.101.102.103",))
    )
    assert phone.start_listener()["status"] == "ready"
    return phone


def test_H_001_health_is_available_before_transport(ready_phone: OfflinePhoneMcp) -> None:
    result = ready_phone.health("h-001")

    assert result["status"] == "ready"
    assert result["request_id"] == "h-001"
    assert result["node"]["lifecycle"] == "READY"
    assert result["intents"]["flashlight"] == "denied_by_policy"
    assert result["intents"]["sms"] == "denied_by_policy"
    assert result["listener"]["bound"] is True
    assert ready_phone.intent_dispatcher.calls == []
    assert ready_phone.zenoh.calls == []


def test_H_002_health_is_side_effect_free(ready_phone: OfflinePhoneMcp) -> None:
    results = [ready_phone.health(f"h-{index}") for index in range(3)]

    assert [result["request_id"] for result in results] == ["h-0", "h-1", "h-2"]
    assert {result["zenoh"]["transport"] for result in results} == {"offline"}
    assert ready_phone.intent_dispatcher.calls == []
    assert ready_phone.zenoh.calls == []
    assert ready_phone.flashlight.calls == []
    assert ready_phone.sms.calls == []


def test_H_003_health_distinguishes_unavailable_zenoh(
    ready_phone: OfflinePhoneMcp,
) -> None:
    result = ready_phone.health("h-003", detail="full")

    assert result["zenoh"] == {
        "availability": "unavailable",
        "transport": "offline",
        "simulation_enabled": False,
    }


def test_H_006_health_reports_bind_failure_truthfully() -> None:
    phone = OfflinePhoneMcp()

    start_result = phone.start_listener()
    health = phone.health("h-006")

    assert start_result["code"] == "BIND_FAILED"
    assert health["status"] == "not_ready"
    assert health["code"] == "BIND_FAILED"
    assert health["listener"]["bound"] is False
    assert health["listener"]["wildcard"] is False
    assert health["listener"]["addresses"] == []


def test_I_001_registry_exposes_only_named_tools(ready_phone: OfflinePhoneMcp) -> None:
    registered = {"phone_health", "phone_flashlight", "phone_sms"}
    forbidden = {"android_send_intent", "run_intent", "start_component"}

    assert registered.isdisjoint(forbidden)
    assert "phone_health" in registered
    assert "phone_flashlight" in registered
    assert "phone_sms" in registered


def test_I_002_unknown_fields_are_rejected_without_side_effects(
    ready_phone: OfflinePhoneMcp,
) -> None:
    result = ready_phone.call(
        "phone_flashlight",
        {"request_id": "i-002", "action": "on", "component": "com.attacker.app"},
    )

    assert result["code"] == "UNKNOWN_FIELD"
    assert ready_phone.intent_dispatcher.calls == []
    assert ready_phone.flashlight.calls == []


@pytest.mark.parametrize("action", ["on", "off", "toggle"])
def test_I_003_I_004_flashlight_is_denied_for_every_action(
    ready_phone: OfflinePhoneMcp, action: str
) -> None:
    result = ready_phone.call(
        "phone_flashlight",
        {"request_id": f"light-{action}", "action": action},
    )

    assert result["status"] == "denied"
    assert result["code"] == "POLICY_DENIED"
    assert result["transport"] == "offline"
    assert ready_phone.intent_dispatcher.calls == []
    assert ready_phone.flashlight.calls == []


def test_I_005_flashlight_denial_stops_before_dispatch(
    ready_phone: OfflinePhoneMcp,
) -> None:
    result = ready_phone.call(
        "phone_flashlight",
        {"request_id": "i-005", "action": "toggle"},
    )

    assert result["code"] == "POLICY_DENIED"
    assert ready_phone.intent_dispatcher.calls == []


def test_I_006_sms_is_denied_without_provider_or_intent(
    ready_phone: OfflinePhoneMcp,
) -> None:
    result = ready_phone.call(
        "phone_sms",
        {"request_id": "i-006", "recipient": "+15550100123", "body": "hello"},
    )

    assert result["status"] == "denied"
    assert result["code"] == "POLICY_DENIED"
    assert ready_phone.sms.calls == []
    assert ready_phone.intent_dispatcher.calls == []


def test_I_007_sms_payload_is_not_echoed_or_retained(
    ready_phone: OfflinePhoneMcp,
) -> None:
    recipient = "+15550100123"
    body = "burner-secret-should-not-appear"
    ready_phone.call(
        "phone_sms",
        {"request_id": "i-007", "recipient": recipient, "body": body},
    )

    observed = json.dumps(
        {
            "audit": ready_phone.audit.calls,
            "logs": ready_phone.logs.calls,
        }
    )
    assert recipient not in observed
    assert body not in observed


def test_I_008_sms_denial_does_not_resolve_a_messaging_app(
    ready_phone: OfflinePhoneMcp,
) -> None:
    result = ready_phone.call(
        "phone_sms",
        {"request_id": "i-008", "recipient": "+15550100123", "body": "hello"},
    )

    assert result["code"] == "POLICY_DENIED"
    assert ready_phone.package_resolver.calls == []
    assert ready_phone.sms.calls == []


def test_T_001_T_002_ready_listener_is_explicit_and_non_wildcard(
    ready_phone: OfflinePhoneMcp,
) -> None:
    listener = ready_phone.health("t-001", detail="full")["listener"]

    assert listener["interface"] == "tailscale0"
    assert listener["addresses"] == ["100.101.102.103"]
    assert listener["wildcard"] is False
    assert listener["bound"] is True
    assert "0.0.0.0" not in listener["addresses"]
    assert "::" not in listener["addresses"]


def test_T_003_missing_tailscale_fails_closed_without_fallback() -> None:
    phone = OfflinePhoneMcp(TailscaleProvider(addresses=()))

    result = phone.start_listener()

    assert result["code"] == "BIND_FAILED"
    assert result["details"] == {"reason": "TAILSCALE_UNAVAILABLE"}
    assert phone.listener["bound"] is False
    assert phone.listener["addresses"] == []
    assert phone.listener["wildcard"] is False


def test_O_001_and_O_002_denials_are_auditable_and_zero_dispatch(
    ready_phone: OfflinePhoneMcp,
) -> None:
    ready_phone.health("o-health")
    ready_phone.call(
        "phone_flashlight", {"request_id": "o-light", "action": "on"}
    )
    ready_phone.call(
        "phone_sms",
        {"request_id": "o-sms", "recipient": "+15550100123", "body": "hello"},
    )

    assert [event["request_id"] for event in ready_phone.audit.calls] == [
        "o-health",
        "o-light",
        "o-sms",
    ]
    assert ready_phone.intent_dispatcher.calls == []
    assert ready_phone.sms.calls == []
    assert ready_phone.flashlight.calls == []

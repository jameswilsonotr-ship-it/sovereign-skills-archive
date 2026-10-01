"""Small offline-only test harness for the T3-23 Included Ultra slot.

The harness deliberately has no transport implementation.  A caller registers
fixture responses and the harness records requests against those fixtures.
This keeps tests deterministic and makes an accidental live call impossible
through this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping


class HarnessConfigurationError(ValueError):
    """Raised when the harness is configured outside the T3-23 contract."""


class FixtureNotFound(KeyError):
    """Raised when a case has no matching registered fixture."""


def _fixture_key(endpoint: str, payload: Mapping[str, Any]) -> str:
    """Build a stable key for a fixture request."""

    return f"{endpoint}:{json.dumps(payload, sort_keys=True, separators=(',', ':'))}"


@dataclass(frozen=True)
class SlotPolicy:
    """The only execution policy supported by this change."""

    slot_id: str = "T3-23"
    availability: str = "included"
    tier: str = "ultra"
    on_demand_fallback: bool = False

    def validate(self) -> None:
        """Reject configurations that could silently widen slot scope."""

        if self.slot_id != "T3-23":
            raise HarnessConfigurationError("harness is scoped to slot T3-23")
        if self.availability != "included":
            raise HarnessConfigurationError("slot must remain included")
        if self.tier != "ultra":
            raise HarnessConfigurationError("slot must remain Ultra tier")
        if self.on_demand_fallback:
            raise HarnessConfigurationError("on-demand fallback is disabled")


@dataclass(frozen=True)
class HarnessCase:
    """One request/response assertion executed entirely from fixtures."""

    case_id: str
    endpoint: str
    payload: Mapping[str, Any]
    expected_response: Any


@dataclass(frozen=True)
class RequestRecord:
    """A request observed by the fixture transport."""

    endpoint: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class HarnessResult:
    """A serializable result suitable for a local test receipt."""

    case_id: str
    passed: bool
    response: Any = None
    reason: str = ""
    requests: tuple[RequestRecord, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly representation of the result."""

        return {
            "case_id": self.case_id,
            "passed": self.passed,
            "response": self.response,
            "reason": self.reason,
            "requests": [
                {"endpoint": request.endpoint, "payload": dict(request.payload)}
                for request in self.requests
            ],
        }


@dataclass
class OfflineTestHarness:
    """Run cases against registered fixtures and nothing else."""

    policy: SlotPolicy = field(default_factory=SlotPolicy)
    _fixtures: dict[str, Any] = field(default_factory=dict, init=False)
    _requests: list[RequestRecord] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.policy.validate()

    def register_fixture(
        self,
        endpoint: str,
        response: Any,
        payload: Mapping[str, Any] | None = None,
    ) -> None:
        """Register a response for one exact endpoint/payload pair."""

        request_payload = {} if payload is None else dict(payload)
        self._fixtures[_fixture_key(endpoint, request_payload)] = response

    def request(self, endpoint: str, payload: Mapping[str, Any]) -> Any:
        """Resolve one request from fixtures, raising on an unknown request."""

        request_payload = dict(payload)
        self._requests.append(RequestRecord(endpoint, request_payload))
        key = _fixture_key(endpoint, request_payload)
        if key not in self._fixtures:
            raise FixtureNotFound(f"no fixture registered for {key}")
        return self._fixtures[key]

    def run(self, case: HarnessCase) -> HarnessResult:
        """Execute a case and compare its response with the expected value."""

        try:
            response = self.request(case.endpoint, case.payload)
        except FixtureNotFound as error:
            return HarnessResult(
                case_id=case.case_id,
                passed=False,
                reason=str(error),
                requests=tuple(self._requests),
            )

        passed = response == case.expected_response
        return HarnessResult(
            case_id=case.case_id,
            passed=passed,
            response=response,
            reason="" if passed else "response did not match expected fixture",
            requests=tuple(self._requests),
        )

    @property
    def requests(self) -> tuple[RequestRecord, ...]:
        """Return an immutable view of requests recorded so far."""

        return tuple(self._requests)

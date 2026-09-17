"""Offline pytest stubs for the Tailscale fail-closed MCP contract.

These tests deliberately exercise local doubles instead of a Tailscale daemon,
DNS, sockets, credentials, or an MCP service.  They are contract fixtures for
TS-001..TS-012; a production adapter can replace the probe and gate without
changing the security decisions asserted here.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass, field
from enum import Enum

import pytest


class ProbeStatus(Enum):
    HEALTHY = "healthy"
    DOWN = "down"
    TIMEOUT = "timeout"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class ProbeStub:
    """Deterministic health-probe double with no I/O implementation."""

    status: ProbeStatus
    calls: list[float] = field(default_factory=list)

    def check(self, timeout_seconds: float) -> ProbeStatus:
        self.calls.append(timeout_seconds)
        if self.status is ProbeStatus.TIMEOUT:
            raise TimeoutError("stub timeout")
        if self.status is ProbeStatus.ERROR:
            raise RuntimeError("stub probe error")
        return self.status


@dataclass(frozen=True)
class Decision:
    allowed: bool
    route: str | None
    reason: str


@dataclass
class FailClosedGateStub:
    """Pure local model of the authorization boundary."""

    probe: ProbeStub
    tailnet_endpoint: str = "http://mcp.tailnet.test"
    public_endpoint: str = "https://mcp.public.test"
    timeout_seconds: float = 0.25
    attempted_routes: list[str] = field(default_factory=list)

    def authorize(self) -> Decision:
        try:
            status = self.probe.check(self.timeout_seconds)
        except TimeoutError:
            return Decision(False, None, "health_probe_timeout")
        except Exception:
            return Decision(False, None, "health_probe_error")

        if status is not ProbeStatus.HEALTHY:
            return Decision(False, None, "mesh_unavailable")
        return Decision(True, self.tailnet_endpoint, "mesh_healthy")

    def request(self) -> Decision:
        """Authorize a request without sending one."""

        decision = self.authorize()
        if decision.allowed:
            self.attempted_routes.append(self.tailnet_endpoint)
        return decision


def test_ts_001_healthy_mesh_allows_mcp() -> None:
    """TS-001: a successful mesh probe permits MCP access."""

    gate = FailClosedGateStub(ProbeStub(ProbeStatus.HEALTHY))

    decision = gate.request()

    assert decision == Decision(True, gate.tailnet_endpoint, "mesh_healthy")


def test_ts_002_healthy_mcp_uses_tailnet_endpoint_only() -> None:
    """TS-002: an allowed request is routed to the mesh endpoint."""

    gate = FailClosedGateStub(
        ProbeStub(ProbeStatus.HEALTHY),
        tailnet_endpoint="http://mcp.internal.test",
        public_endpoint="https://mcp.public.test",
    )

    gate.request()

    assert gate.attempted_routes == [gate.tailnet_endpoint]
    assert gate.public_endpoint not in gate.attempted_routes


def test_ts_003_mesh_drop_denies_the_next_request() -> None:
    """TS-003: a drop invalidates authorization for the next request."""

    probe = ProbeStub(ProbeStatus.HEALTHY)
    gate = FailClosedGateStub(probe)
    assert gate.request().allowed is True

    probe.status = ProbeStatus.DOWN
    decision = gate.request()

    assert decision == Decision(False, None, "mesh_unavailable")
    assert gate.attempted_routes == [gate.tailnet_endpoint]


def test_ts_004_mesh_down_denies_without_a_route() -> None:
    """TS-004: unavailable mesh state is an authorization failure."""

    gate = FailClosedGateStub(ProbeStub(ProbeStatus.DOWN))

    decision = gate.request()

    assert decision.allowed is False
    assert decision.route is None
    assert gate.attempted_routes == []


def test_ts_005_public_reachability_is_not_a_fallback() -> None:
    """TS-005: a configured public endpoint is never an MCP recovery path."""

    gate = FailClosedGateStub(
        ProbeStub(ProbeStatus.DOWN),
        public_endpoint="https://reachable-public.test",
    )

    decision = gate.request()

    assert decision.allowed is False
    assert gate.public_endpoint not in gate.attempted_routes


def test_ts_006_probe_timeout_denies_mcp() -> None:
    """TS-006: timeout produces denial instead of an unbounded wait."""

    gate = FailClosedGateStub(ProbeStub(ProbeStatus.TIMEOUT))

    decision = gate.request()

    assert decision == Decision(False, None, "health_probe_timeout")
    assert gate.attempted_routes == []


def test_ts_007_probe_error_denies_mcp() -> None:
    """TS-007: probe errors fail closed."""

    gate = FailClosedGateStub(ProbeStub(ProbeStatus.ERROR))

    decision = gate.request()

    assert decision == Decision(False, None, "health_probe_error")


def test_ts_008_unknown_probe_state_denies_mcp() -> None:
    """TS-008: uncertainty never becomes permission."""

    gate = FailClosedGateStub(ProbeStub(ProbeStatus.UNKNOWN))

    decision = gate.request()

    assert decision == Decision(False, None, "mesh_unavailable")


def test_ts_009_probe_receives_the_configured_timeout_budget() -> None:
    """TS-009: the configured bounded budget is passed to each probe."""

    probe = ProbeStub(ProbeStatus.DOWN)
    gate = FailClosedGateStub(probe, timeout_seconds=0.125)

    gate.request()

    assert probe.calls == [0.125]


def test_ts_010_timeout_does_not_start_a_public_probe() -> None:
    """TS-010: mesh timeout stops authorization without another route probe."""

    probe = ProbeStub(ProbeStatus.TIMEOUT)
    gate = FailClosedGateStub(probe)

    gate.request()

    assert probe.calls == [gate.timeout_seconds]
    assert gate.attempted_routes == []


def test_ts_011_recovery_requires_a_fresh_successful_probe() -> None:
    """TS-011: recovery is allowed only after a new healthy result."""

    probe = ProbeStub(ProbeStatus.DOWN)
    gate = FailClosedGateStub(probe)
    assert gate.request().allowed is False

    probe.status = ProbeStatus.HEALTHY
    recovered = gate.request()

    assert recovered == Decision(True, gate.tailnet_endpoint, "mesh_healthy")
    assert probe.calls == [gate.timeout_seconds, gate.timeout_seconds]


def test_ts_012_gate_is_network_free(monkeypatch: pytest.MonkeyPatch) -> None:
    """TS-012: all contract cases run without opening sockets."""

    def forbidden_socket(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline stub attempted to open a socket")

    monkeypatch.setattr(socket, "socket", forbidden_socket)
    monkeypatch.setattr(socket, "create_connection", forbidden_socket)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden_socket)

    for status in ProbeStatus:
        gate = FailClosedGateStub(ProbeStub(status))
        decision = gate.request()
        assert decision.route in {None, gate.tailnet_endpoint}

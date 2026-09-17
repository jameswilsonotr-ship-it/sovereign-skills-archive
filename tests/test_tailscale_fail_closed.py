"""Offline acceptance tests for the Tailscale-only MCP access contract.

The repository does not currently ship an MCP runtime.  The small gate below
is therefore a deterministic acceptance model, not a network client.  Keeping
the model local makes these tests useful in CI without Tailscale, credentials,
DNS, sockets, or a live MCP service.
"""

import re
import unittest
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class ProbeStatus(Enum):
    HEALTHY = "healthy"
    DOWN = "down"
    TIMEOUT = "timeout"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class FakeHealthProbe:
    """A local probe double that never performs I/O."""

    status: ProbeStatus
    calls: List[float] = field(default_factory=list)

    def check(self, timeout_seconds: float) -> ProbeStatus:
        self.calls.append(timeout_seconds)
        if self.status is ProbeStatus.TIMEOUT:
            raise TimeoutError("deterministic test timeout")
        if self.status is ProbeStatus.ERROR:
            raise RuntimeError("deterministic test probe error")
        return self.status


@dataclass(frozen=True)
class Decision:
    allowed: bool
    route: Optional[str]
    reason: str


class LocalFailClosedMcpGate:
    """Pure decision model for the fail-closed acceptance contract."""

    def __init__(
        self,
        probe: FakeHealthProbe,
        tailnet_endpoint: str = "http://mcp.tailnet.example",
        public_endpoint: str = "https://mcp.public.example",
        timeout_seconds: float = 0.25,
    ) -> None:
        self.probe = probe
        self.tailnet_endpoint = tailnet_endpoint
        # This value is intentionally never consulted for route selection.
        self.public_endpoint = public_endpoint
        self.timeout_seconds = timeout_seconds
        self.attempted_routes: List[str] = []

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
        """Select a route without sending a request."""

        decision = self.authorize()
        if decision.allowed:
            self.attempted_routes.append(self.tailnet_endpoint)
        return decision


def _optional_acceptance_files() -> List[Path]:
    """Find optional OpenSpec/BASIC_TIER references without network access."""

    root = Path(__file__).resolve().parents[1]
    candidates: List[Path] = []
    spec_root = root / "docs" / "openspec" / "SPEC-002"
    if spec_root.is_file():
        candidates.append(spec_root)
    elif spec_root.is_dir():
        candidates.extend(path for path in spec_root.rglob("*") if path.is_file())

    for path in root.rglob("*"):
        if path.is_file() and path.name.lower().startswith("basic_tier"):
            candidates.append(path)

    return sorted(set(candidates))


class TailscaleFailClosedTests(unittest.TestCase):
    def test_mesh_drop_denies_mcp(self) -> None:
        """AC-001: a drop invalidates the next MCP authorization."""

        probe = FakeHealthProbe(ProbeStatus.HEALTHY)
        gate = LocalFailClosedMcpGate(probe)

        self.assertTrue(gate.request().allowed)
        self.assertEqual(gate.attempted_routes, [gate.tailnet_endpoint])

        probe.status = ProbeStatus.DOWN
        denied = gate.request()

        self.assertFalse(denied.allowed)
        self.assertIsNone(denied.route)
        self.assertEqual(denied.reason, "mesh_unavailable")
        self.assertEqual(gate.attempted_routes, [gate.tailnet_endpoint])

    def test_mesh_down_never_falls_back_to_public_internet(self) -> None:
        """AC-002: a reachable public endpoint is not an MCP recovery path."""

        probe = FakeHealthProbe(ProbeStatus.DOWN)
        gate = LocalFailClosedMcpGate(probe)

        denied = gate.request()

        self.assertFalse(denied.allowed)
        self.assertIsNone(denied.route)
        self.assertNotIn(gate.public_endpoint, gate.attempted_routes)
        self.assertEqual(gate.attempted_routes, [])
        self.assertEqual(probe.calls, [gate.timeout_seconds])

    def test_health_probe_timeout_denies_mcp(self) -> None:
        """AC-003: timeout is denial, with the configured bound preserved."""

        probe = FakeHealthProbe(ProbeStatus.TIMEOUT)
        gate = LocalFailClosedMcpGate(probe, timeout_seconds=0.125)

        denied = gate.request()

        self.assertFalse(denied.allowed)
        self.assertIsNone(denied.route)
        self.assertEqual(denied.reason, "health_probe_timeout")
        self.assertEqual(probe.calls, [0.125])
        self.assertEqual(gate.attempted_routes, [])

    def test_probe_error_and_unknown_state_deny_mcp(self) -> None:
        """AC-004: uncertainty never becomes permission."""

        for status, reason in (
            (ProbeStatus.ERROR, "health_probe_error"),
            (ProbeStatus.UNKNOWN, "mesh_unavailable"),
        ):
            with self.subTest(status=status):
                probe = FakeHealthProbe(status)
                gate = LocalFailClosedMcpGate(probe)

                denied = gate.request()

                self.assertFalse(denied.allowed)
                self.assertIsNone(denied.route)
                self.assertEqual(denied.reason, reason)
                self.assertEqual(gate.attempted_routes, [])

    def test_recovery_requires_a_fresh_successful_probe(self) -> None:
        """A later success may recover access, but a denial is never cached open."""

        probe = FakeHealthProbe(ProbeStatus.DOWN)
        gate = LocalFailClosedMcpGate(probe)
        self.assertFalse(gate.request().allowed)

        probe.status = ProbeStatus.HEALTHY
        recovered = gate.request()

        self.assertTrue(recovered.allowed)
        self.assertEqual(recovered.route, gate.tailnet_endpoint)
        self.assertEqual(probe.calls, [gate.timeout_seconds, gate.timeout_seconds])

    def test_optional_acceptance_references_are_checked_when_present(self) -> None:
        """Keep future SPEC-002/BASIC_TIER acceptance text aligned with policy."""

        references = _optional_acceptance_files()
        if not references:
            self.skipTest("optional SPEC-002 and BASIC_TIER references are absent")

        required_patterns = (
            r"\b(?:mesh|tailscale|tailnet)\b",
            r"\bmcp\b",
            r"\bpublic(?:\s+internet)?\b",
            r"\btimeout\b",
        )
        for path in references:
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            for pattern in required_patterns:
                with self.subTest(path=path, pattern=pattern):
                    self.assertRegex(text, re.compile(pattern))

    def test_policy_document_states_the_same_invariants(self) -> None:
        document = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "security"
            / "TAILSCALE_FAIL_CLOSED.md"
        ).read_text(encoding="utf-8").lower()

        for phrase in (
            "mesh drop",
            "probe timeout",
            "no public fallback",
            "deny",
            "offline",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, document)


if __name__ == "__main__":
    unittest.main()

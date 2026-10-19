import sys
from pathlib import Path
import unittest


CHANGE_ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(CHANGE_ROOT))

from harness import (  # noqa: E402
    HarnessCase,
    HarnessConfigurationError,
    OfflineTestHarness,
    SlotPolicy,
)


class OfflineTestHarnessTests(unittest.TestCase):
    def test_default_policy_is_included_ultra_only(self) -> None:
        harness = OfflineTestHarness()
        harness.register_fixture(
            "slot/check",
            {"status": "ready", "slot": "T3-23"},
            {"sample": 1},
        )

        result = harness.run(
            HarnessCase(
                case_id="included-ultra-ready",
                endpoint="slot/check",
                payload={"sample": 1},
                expected_response={"status": "ready", "slot": "T3-23"},
            )
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.as_dict()["requests"][0]["payload"], {"sample": 1})

    def test_fixture_lookup_is_order_independent(self) -> None:
        harness = OfflineTestHarness()
        harness.register_fixture("slot/check", {"ok": True}, {"b": 2, "a": 1})

        result = harness.run(
            HarnessCase(
                case_id="stable-key",
                endpoint="slot/check",
                payload={"a": 1, "b": 2},
                expected_response={"ok": True},
            )
        )

        self.assertTrue(result.passed)

    def test_missing_fixture_fails_without_fallback(self) -> None:
        harness = OfflineTestHarness()
        result = harness.run(
            HarnessCase(
                case_id="no-fallback",
                endpoint="unregistered",
                payload={},
                expected_response=None,
            )
        )

        self.assertFalse(result.passed)
        self.assertIn("no fixture registered", result.reason)
        self.assertEqual(len(result.requests), 1)

    def test_policy_rejects_non_included_or_non_ultra_configuration(self) -> None:
        policies = (
            SlotPolicy(availability="on-demand"),
            SlotPolicy(tier="standard"),
            SlotPolicy(on_demand_fallback=True),
        )
        for policy in policies:
            with self.subTest(policy=policy):
                with self.assertRaises(HarnessConfigurationError):
                    OfflineTestHarness(policy=policy)

    def test_policy_rejects_a_different_slot(self) -> None:
        with self.assertRaises(HarnessConfigurationError):
            OfflineTestHarness(policy=SlotPolicy(slot_id="T3-24"))


if __name__ == "__main__":
    unittest.main()

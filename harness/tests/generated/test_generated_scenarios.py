"""Standard-library checks for the committed generated OpenSpec corpus."""

from __future__ import annotations

import unittest

from harness.tests.generated.generate import render_dataset
from harness.tests.generated.runner import offline_guard, verify_dataset
from harness.tests.generated.scenario_schema import SCENARIO_COUNT


class GeneratedScenarioCorpusTests(unittest.TestCase):
    def test_committed_corpus_is_verified_offline(self) -> None:
        with offline_guard():
            report = verify_dataset()
        self.assertEqual(report["status"], "verified")
        self.assertEqual(report["scenario_count"], SCENARIO_COUNT)
        self.assertTrue(report["offline"])
        self.assertTrue(report["deterministic"])

    def test_rendering_is_byte_stable(self) -> None:
        self.assertEqual(render_dataset(), render_dataset())


if __name__ == "__main__":
    unittest.main()

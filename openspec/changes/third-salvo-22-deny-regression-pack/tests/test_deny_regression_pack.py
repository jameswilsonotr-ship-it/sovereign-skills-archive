import ast
import json
import sys
import unittest
from pathlib import Path


CHANGE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHANGE_DIR))

from pack.evaluator import INCLUDED, ON_DEMAND, SLOT, ULTRA, evaluate  # noqa: E402


class T322DenyRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cases_path = CHANGE_DIR / "pack" / "cases.json"
        cls.cases = json.loads(cases_path.read_text(encoding="utf-8"))

    def test_fixture_decisions_and_reason_codes(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                result = evaluate(case["request"])
                self.assertEqual(case["decision"], result["decision"])
                self.assertEqual(case["reason_codes"], result["reason_codes"])

    def test_only_exact_included_ultra_is_allowed(self):
        values = (None, "", INCLUDED, ON_DEMAND, "included")
        tiers = (None, "", ULTRA, "ultra", "Pro")
        allowed = []
        for entitlement in values:
            for tier in tiers:
                result = evaluate(
                    {"slot": SLOT, "entitlement": entitlement, "tier": tier}
                )
                if result["decision"] == "ALLOW":
                    allowed.append((entitlement, tier))
        self.assertEqual([(INCLUDED, ULTRA)], allowed)

    def test_on_demand_is_denied_even_at_ultra(self):
        result = evaluate(
            {"slot": SLOT, "entitlement": ON_DEMAND, "tier": ULTRA}
        )
        self.assertEqual("DENY", result["decision"])
        self.assertIn("ON_DEMAND_NOT_ALLOWED", result["reason_codes"])
        self.assertIsNone(result["fallback"])

    def test_all_denials_are_terminal_and_explainable(self):
        requests = (
            None,
            {},
            {"slot": SLOT, "entitlement": INCLUDED, "tier": "Pro"},
            {"slot": "T3-21", "entitlement": INCLUDED, "tier": ULTRA},
        )
        for request in requests:
            with self.subTest(request=request):
                result = evaluate(request)
                self.assertEqual("DENY", result["decision"])
                self.assertTrue(result["reason_codes"])
                self.assertIsNone(result["fallback"])
                self.assertEqual(SLOT, result["slot"])

    def test_evaluator_has_no_runtime_io_imports(self):
        source = (CHANGE_DIR / "pack" / "evaluator.py").read_text(
            encoding="utf-8"
        )
        tree = ast.parse(source)
        imports = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        }
        imports.update(
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        )
        self.assertEqual(
            {"__future__", "collections.abc", "typing"},
            imports,
        )


if __name__ == "__main__":
    unittest.main()

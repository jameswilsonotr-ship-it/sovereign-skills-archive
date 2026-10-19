#!/usr/bin/env python3
"""Unittest wrapper around sunset_smoke + unit checks."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from census import done, upsert  # noqa: E402
from gcm_lib import classify, run_id, stamps  # noqa: E402
from sunset_smoke import run_smoke  # noqa: E402


class GcmLibTests(unittest.TestCase):
    def test_stamps_have_both_zones(self):
        s = stamps()
        self.assertIn("T", s["stamp_utc"])
        self.assertTrue(s["stamp_utc"].endswith("Z"))
        self.assertIn("claim", s)

    def test_run_id_stable_shape(self):
        rid = run_id("smoke")
        self.assertTrue(rid.startswith("GCM-") or "_" in rid)
        self.assertGreaterEqual(len(rid), 8)

    def test_classify_secret(self):
        self.assertEqual(classify(Path("artifacts/secrets/tskey.txt")), "secret")

    def test_census_done(self):
        row = {"packed": True, "pointed": True, "redacted": "n/a"}
        self.assertTrue(done(row))
        self.assertFalse(done({"packed": True, "pointed": False, "redacted": "n/a"}))


class SmokeTests(unittest.TestCase):
    def test_harness_exit_payload(self):
        with tempfile.TemporaryDirectory() as td:
            report = run_smoke(Path(td))
        self.assertTrue(report["ok"])
        self.assertEqual(report["planted_class_files"], 12)
        self.assertEqual(report["census_status"], "DONE")
        self.assertGreaterEqual(report["omissions"], 1)
        blob = "".join(report["secrets_omitted"])
        self.assertTrue("secret" in blob.lower() or "cookies" in blob.lower())



class ExportLogTests(unittest.TestCase):
    def test_export_log_append_only(self):
        import tempfile
        import export_log
        td = Path(tempfile.mkdtemp()) / "EXPORT_LOG.jsonl"
        export_log.append_row(td, {"run_id": "r1", "verb": "smoke", "action": "SKIP-EXISTS", "path": "twin.md"})
        export_log.append_row(td, {"run_id": "r2", "verb": "smoke", "action": "EXPORTED", "path": "TOC.md"})
        text1 = td.read_text(encoding="utf-8")
        export_log.append_row(td, {"run_id": "r3", "verb": "smoke", "action": "OPERATOR-SAID-NO", "path": "live-sunset"})
        text2 = td.read_text(encoding="utf-8")
        self.assertTrue(text2.startswith(text1))
        self.assertEqual(len(export_log.read_rows(td)), 3)


if __name__ == "__main__":
    unittest.main()

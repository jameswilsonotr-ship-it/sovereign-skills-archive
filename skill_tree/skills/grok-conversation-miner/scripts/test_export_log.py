#!/usr/bin/env python3
"""GCM-WQ-020 smoke: append-only + hash chain + cite."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from export_log import ACTIONS, append_row, cite, read_rows, row_hash  # noqa: E402


class ExportLogTests(unittest.TestCase):
    def test_append_only_grows(self):
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "EXPORT_LOG.jsonl"
            a = append_row(log, run_id="r1", verb="sunset", conversation_key="2026-09-11_smoke", action="EXPORTED", path="twin.md")
            b = append_row(log, run_id="r1", verb="sunset", conversation_key="2026-09-11_smoke", action="SKIP-EXISTS", path="twin.md", pointer="FAKE")
            rows = read_rows(log)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["seq"], 1)
            self.assertEqual(rows[1]["seq"], 2)
            self.assertTrue(rows[0]["exported"])
            self.assertFalse(rows[1]["exported"])
            self.assertEqual(rows[1]["prev_row_sha256"], a["row_sha256"])
            self.assertEqual(rows[1]["row_sha256"], row_hash(rows[1]))
            self.assertNotEqual(a["row_sha256"], b["row_sha256"])
            c = cite(log)
            self.assertEqual(c["count"], 2)
            self.assertEqual(c["head_seq"], 2)
            self.assertTrue(c["file_sha256"])
            # rewrite is not exposed; file still two lines after another append
            append_row(log, run_id="r2", verb="dry-run", conversation_key="2026-09-11_smoke", action="WOULD-SKIP", path="extract.tar.gz")
            self.assertEqual(len(read_rows(log)), 3)

    def test_unknown_action_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            log = Path(td) / "EXPORT_LOG.jsonl"
            with self.assertRaises(ValueError):
                append_row(log, run_id="r", verb="sunset", conversation_key="k", action="QUIET-DROP")
            self.assertFalse(log.exists() and log.read_text().strip())
            self.assertIn("SKIP-OVERLAP", ACTIONS)


if __name__ == "__main__":
    unittest.main()

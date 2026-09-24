import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_openspec_ids.py"


class CheckOpenSpecIdsTest(unittest.TestCase):
    def test_duplicate_ids_fail_and_unique_ids_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = root / "spec.md"
            spec.write_text("## Criteria\n- AC-001: first criterion\n", encoding="utf-8")

            clean = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

            spec.write_text(
                "## Criteria\n- AC-001: first criterion\n- AC-001: duplicate\n",
                encoding="utf-8",
            )
            duplicate = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(duplicate.returncode, 1, duplicate.stdout + duplicate.stderr)
            self.assertIn("AC-001", duplicate.stdout)


if __name__ == "__main__":
    unittest.main()

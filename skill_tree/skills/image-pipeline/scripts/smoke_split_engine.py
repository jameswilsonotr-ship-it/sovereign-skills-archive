#!/usr/bin/env python3
"""Smoke: factory siblings exist and --help exits 0. Reconstructed 2026-09-11."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEED = [
    "inbound_classify.py",
    "segment_grid.py",
    "inbound_queue.py",
    "split_plan.py",
    "emit_intent.py",
    "scaleback_loop.py",
    "isolate_person.py",
    "hub_review.py",
    "keep_path.py",
]


def main() -> int:
    missing = [n for n in NEED if not (HERE / n).exists()]
    helps = []
    for n in NEED:
        p = HERE / n
        if not p.exists():
            continue
        proc = subprocess.run([sys.executable, str(p), "--help"], capture_output=True, text=True)
        helps.append({"script": n, "help_exit": proc.returncode})
    ok = not missing and all(h["help_exit"] == 0 for h in helps)
    print({"ok": ok, "missing": missing, "helps": helps, "reconstructed": "2026-09-11"})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

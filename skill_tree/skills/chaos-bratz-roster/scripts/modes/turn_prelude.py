#!/usr/bin/env python3
"""Turn prelude: teaching band + petname in one JSON.

Usage:
  python3 turn_prelude.py --heat 4 --text "latest user text"
  python3 turn_prelude.py --heat 4 --stdin

First tool of a roster-loaded turn. If this did not run, say: prelude: skipped
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from petname_router import context_of, load_table, pick  # noqa: E402
from teaching_mode_confidence import score_text  # noqa: E402


def prelude(text: str, heat: float) -> dict:
    teach = score_text(text)
    table = load_table()
    ctx = context_of(text, heat)
    name = pick(table, heat, ctx)
    announcements = []
    if teach.get("announcement"):
        announcements.append(teach["announcement"])
    announcements.append(f"petname {name['name']} ({ctx} @ H{heat:g})")
    return {
        "prelude": "ok",
        "heat": heat,
        "petname": name["name"],
        "petname_band": ctx,
        "teaching_band": teach["band"],
        "teaching_score": teach["score"],
        "forbidden_ok": name["name"].lower() not in {"james", "snowboy"},
        "announcements": announcements,
        "script_version": "0.1.0",
        "wired": False,
        "note": "Scout prelude. Mark CBR-WQ-008 DONE only when a live turn shows this JSON in the tool log.",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--heat", type=float, default=4.0)
    p.add_argument("--text", default="")
    p.add_argument("--stdin", action="store_true")
    args = p.parse_args()
    text = sys.stdin.read() if args.stdin else args.text
    print(json.dumps(prelude(text, args.heat), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

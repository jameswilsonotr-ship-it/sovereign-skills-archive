#!/usr/bin/env python3
"""IP-WQ-203 — cousins are not trash.

Never delete a rendered cousin because the pose was 'wrong'.
Record variant_of + verdict (lock|useful|park) on the keep and in VARIANTS.jsonl.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
LEDGER = Path("/home/workdir/artifacts/rendered/VARIANTS.jsonl")
REND = Path("/home/workdir/artifacts/rendered")


def stamp() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def mark(keep_path: Path, variant_of: str, verdict: str, note: str) -> dict:
    rec = json.loads(keep_path.read_text(encoding="utf-8"))
    rec.setdefault("variants", {})
    rec["variants"] = {
        "variant_of": variant_of,
        "verdict": verdict,
        "note": note,
        "at": stamp(),
        "policy": "IP-WQ-203-keep-cousins",
    }
    keep_path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "keep": str(keep_path),
        "slug": rec.get("slug"),
        "variant_of": variant_of,
        "verdict": verdict,
        "note": note,
        "at": stamp(),
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--keep", required=True)
    p.add_argument("--variant-of", default="")
    p.add_argument("--verdict", default="useful", choices=("lock", "useful", "park"))
    p.add_argument("--note", default="")
    args = p.parse_args()
    path = Path(args.keep)
    if not path.exists():
        path = REND / args.keep
    row = mark(path, args.variant_of, args.verdict, args.note)
    print(json.dumps({"ok": True, "row": row}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Lake-batch historical vacuum wrapper. GCM-WQ-008.

Walks a dated tree YYYY/MM/weekNN/YYYY-MM-DD.
Never slurps homogenized_shards.jsonl.
Per day: twin exists → SKIP-EXISTS + census point; else NO_TWIN card and continue
(keep-everything: do not delete; annotate).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from gcm_lib import era_for_date, stamp_iso, write_json


def walk_dated_tree(root: Path) -> list[dict]:
    days = []
    if not root.exists():
        return days
    slurps = list(root.rglob("homogenized_shards.jsonl"))
    if slurps:
        raise RuntimeError(f"REFUSE_SLURP {slurps[0]}")
    for day_dir in sorted(p for p in root.rglob("*") if p.is_dir() and len(p.name) == 10 and p.name[4] == "-"):
        twins = list(day_dir.glob("*.md"))
        receipts = list(day_dir.glob("RECEIPT*"))
        days.append(
            {
                "date": day_dir.name,
                "path": str(day_dir),
                "era": era_for_date(day_dir.name),
                "twin_count": len(twins),
                "receipt_count": len(receipts),
                "twins": [p.name for p in twins],
                "status": "SKIP-EXISTS" if twins else "NO_TWIN",
            }
        )
    return days


def run(root: Path, start: str | None = None, end: str | None = None) -> dict:
    days = walk_dated_tree(root)
    if start:
        days = [d for d in days if d["date"] >= start]
    if end:
        days = [d for d in days if d["date"] <= end]
    return {
        "stamp": stamp_iso(),
        "root": str(root),
        "start": start,
        "end": end,
        "days": days,
        "skip_exists": sum(1 for d in days if d["status"] == "SKIP-EXISTS"),
        "no_twin": sum(1 for d in days if d["status"] == "NO_TWIN"),
        "slurp": False,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("root", type=Path)
    p.add_argument("--from", dest="start")
    p.add_argument("--to", dest="end")
    p.add_argument("--out", type=Path)
    args = p.parse_args(argv)
    result = run(args.root, args.start, args.end)
    if args.out:
        write_json(args.out, result)
    print(json.dumps({k: result[k] for k in ("skip_exists", "no_twin", "slurp", "stamp")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())


def plan_month(root: Path, year: int, month: int) -> dict:
    start = f"{year:04d}-{month:02d}-01"
    if month == 12:
        end = f"{year:04d}-12-31"
    else:
        end = f"{year:04d}-{month+1:02d}-01"
    days = walk_dated_tree(root)
    days = [d for d in days if d["date"] >= start and d["date"] < end] if month != 12 else [d for d in days if d["date"] >= start]
    return days

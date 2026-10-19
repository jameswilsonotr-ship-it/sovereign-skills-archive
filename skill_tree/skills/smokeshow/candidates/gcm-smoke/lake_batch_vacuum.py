#!/usr/bin/env python3
"""GCM-WQ-008 lake-batch vacuum wrapper. Walks a dated fixture tree only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gcm_lib import stamps


def walk_days(root: Path) -> list[dict]:
    rows = []
    for day_dir in sorted(p for p in root.rglob("*") if p.is_dir() and len(p.name) == 10 and p.name[4] == "-"):
        twins = list(day_dir.glob("*.md"))
        rows.append({
            "date": day_dir.name,
            "path": str(day_dir),
            "twin": twins[0].name if twins else None,
            "status": "SKIP-EXISTS" if twins else "NO_TWIN",
        })
    return rows


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--from-date", default="")
    p.add_argument("--to-date", default="")
    args = p.parse_args(argv)
    rows = walk_days(args.root)
    if args.from_date:
        rows = [r for r in rows if r["date"] >= args.from_date]
    if args.to_date:
        rows = [r for r in rows if r["date"] <= args.to_date]
    print(json.dumps({"rows": rows, **stamps()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

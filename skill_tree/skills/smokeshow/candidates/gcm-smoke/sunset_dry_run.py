#!/usr/bin/env python3
"""GCM-WQ-004 dry-run: print L0–L8 table, write nothing unless --out card."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gcm_lib import jsonl_read, stamps

LANES = (
    ("L0", "identity"),
    ("L1", "lake twin"),
    ("L2", "lake receipt"),
    ("L3", "miner publish"),
    ("L4", "global extract"),
    ("L5", "cilia"),
    ("L6", "doorbell"),
    ("L7", "outbox card"),
    ("L8", "export recon"),
)


def decide(census_row: dict | None, flag: str) -> list[dict]:
    rows = []
    for code, name in LANES:
        status = "SKIP-NO-SHARD"
        if code == "L0":
            status = "RAN"
        elif code == "L8" and flag != "export-recon":
            status = "SKIP-NO-HIT"
        elif census_row:
            if code == "L1" and census_row.get("twin_id"):
                status = "SKIP-EXISTS"
            elif code == "L2" and census_row.get("receipt_id"):
                status = "SKIP-EXISTS"
            elif code == "L3" and census_row.get("miner_tar_id"):
                status = "SKIP-EXISTS"
            elif code == "L4" and census_row.get("global_extract_id"):
                status = "SKIP-EXISTS"
            elif code in {"L5", "L6", "L7"}:
                status = "WOULD-RAN"
        else:
            if code in {"L5", "L6", "L7"}:
                status = "WOULD-RAN"
        if flag == "lake-only" and code in {"L3", "L4", "L8"}:
            status = "SKIP-NO-HIT"
        if flag == "miner-only" and code in {"L1", "L2", "L6"}:
            status = "SKIP-NO-HIT"
        rows.append({"lane": code, "name": name, "status": status})
    return rows


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--flag", default="dry-run", choices=("dry-run", "lake-only", "miner-only", "export-recon"))
    p.add_argument("--census", type=Path)
    p.add_argument("--key")
    p.add_argument("--out", type=Path)
    args = p.parse_args(argv)
    row = None
    if args.census and args.key:
        row = next((r for r in jsonl_read(args.census) if r.get("key") == args.key), None)
    table = decide(row, args.flag)
    payload = {"flag": args.flag, "lanes": table, **stamps()}
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

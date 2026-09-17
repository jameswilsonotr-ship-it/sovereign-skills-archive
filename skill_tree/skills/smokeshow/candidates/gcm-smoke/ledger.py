#!/usr/bin/env python3
"""GCM-WQ-018 skill-tree conversation ledger row."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gcm_lib import jsonl_upsert, stamps


def add_row(path: Path, **fields) -> dict:
    row = {"skills_touched": [], "content_minted": [], "sandbox_egressed": [], **fields}
    if isinstance(row["skills_touched"], str):
        row["skills_touched"] = [s for s in row["skills_touched"].split(",") if s]
    row.update(stamps())
    jsonl_upsert(path, "run_id", row)
    return row


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--conversation-space", default="")
    p.add_argument("--skills-touched", default="")
    args = p.parse_args(argv)
    row = add_row(
        args.file,
        run_id=args.run_id,
        conversation_space=args.conversation_space,
        skills_touched=args.skills_touched,
    )
    print(json.dumps(row, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

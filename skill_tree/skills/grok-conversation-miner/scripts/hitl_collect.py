#!/usr/bin/env python3
"""Concatenate HITL-001 TELEMETRY.json packets into an append-only INDEX.jsonl."""
from __future__ import annotations

import json
from pathlib import Path

ROOTS = [
    Path("/home/workdir/artifacts/gcm_hitl/HITL-001_v1.3.0"),
    Path("/home/workdir/.grok/skills/grok-conversation-miner/references/hitl/runs"),
]
OUT = Path("/home/workdir/.grok/skills/grok-conversation-miner/references/hitl/runs/INDEX.jsonl")


def packets():
    seen = set()
    for root in ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("TELEMETRY.json")):
            raw = path.read_text(encoding="utf-8")
            key = raw
            if key in seen:
                continue
            seen.add(key)
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                row = {"hitl_id": "HITL-001", "error": f"bad json {path}: {exc}", "path": str(path)}
            row["_packet_path"] = str(path)
            yield row


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = list(packets())
    OUT.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
    print(f"wrote {len(rows)} rows -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

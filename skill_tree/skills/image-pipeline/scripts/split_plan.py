#!/usr/bin/env python3
"""Four-plate plan A/B/C/D + optional M2/M3. Reconstructed 2026-09-11 from PROTOCOL.md."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PLATES = ("A-ID", "B-HEAT", "C-ANIME", "D-RIG")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--desc", required=True, help="JSON descriptor path or inline JSON")
    p.add_argument("--engine", default="generate", choices=("generate", "overlay"))
    p.add_argument("--merge", action="store_true", help="include optional M2/M3 DNA merge slots")
    args = p.parse_args()
    raw = args.desc
    if Path(raw).exists():
        desc = json.loads(Path(raw).read_text(encoding="utf-8"))
    else:
        desc = json.loads(raw)
    who = desc.get("who") or desc.get("subject") or "inbound subject"
    slots = []
    for plate in PLATES:
        slots.append(
            {
                "plate": plate,
                "engine": args.engine,
                "prompt_stub": f"{plate} of {who}. Inbound crop is SOURCE not plate A.",
            }
        )
    if args.merge:
        slots.append({"plate": "M2", "engine": args.engine, "prompt_stub": f"DNA merge Olivia+Bunny onto {who}"})
        slots.append({"plate": "M3", "engine": "overlay", "prompt_stub": f"edit-merge onto crop of {who}"})
    out = {"ok": True, "desc": desc, "slots": slots, "reconstructed": "2026-09-11"}
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

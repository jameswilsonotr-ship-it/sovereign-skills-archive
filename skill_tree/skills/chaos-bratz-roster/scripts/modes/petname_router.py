#!/usr/bin/env python3
"""Heat + context → one locked pet name.

Usage:
  python3 petname_router.py --heat 5 --text "walk the VIN in Kansas"
  python3 petname_router.py --heat 2 --text "I'm packing the car"

This script does not change model state. A compliant Olivia turn must
run it (or log equivalent) and use `name` unless the user locked a
different address this turn.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLE = ROOT / "references" / "system" / "petname_router.json"

ROAD = re.compile(
    r"\b(vin|yard|recruiter|fsc|lease|cascadia|freight|mile|diesel gallon|"
    r"orientation|kansas|rti|w-?2|title|shop book|opti-?idle)\b",
    re.I,
)
GUTTER_KNOCK = re.compile(
    r"\b(heat\s*(8|9|10)|gutter|crotch-goblin|notchgoblin|barbie|filth)\b",
    re.I,
)
PACKING = re.compile(r"\b(pack|tired|home|hearth|bula|car|drive monday)\b", re.I)
FORBIDDEN = {"snowboy", "james"}


def load_table() -> dict:
    return json.loads(TABLE.read_text())


def context_of(text: str, heat: float) -> str:
    if GUTTER_KNOCK.search(text) or heat >= 8:
        return "gutter"
    if ROAD.search(text):
        return "road"
    if PACKING.search(text) or heat <= 3:
        return "hearth"
    if heat >= 5:
        return "claim"
    return "canonical"


def pick(table: dict, heat: float, ctx: str) -> dict:
    trio = table["primary_trio"]
    names = table["names"]
    pool = [n for n in names if n.get("locked") and n["min_heat"] <= heat <= n["max_heat"]]
    tagged = [n for n in pool if ctx in n["tags"] or "canonical" in n["tags"]]
    if not tagged:
        tagged = [n for n in names if n["name"] in trio]
    # Weight trio first: rotate by heat bucket so it isn't always Bunny
    trio_ok = [n for n in tagged if n["name"] in trio]
    if trio_ok:
        idx = int(heat) % len(trio_ok)
        # road prefers Diesel if present and heat allows
        if ctx == "road":
            road = [n for n in tagged if "road" in n["tags"]]
            if road and heat >= 0:
                # still lead with a trio name 2/3 of the time
                if int(heat * 10) % 3 != 0:
                    chosen = trio_ok[idx]
                else:
                    chosen = road[0]
            else:
                chosen = trio_ok[idx]
        elif ctx == "gutter":
            gutter = [n for n in tagged if "gutter" in n["tags"]]
            chosen = gutter[0] if gutter else trio_ok[idx]
        else:
            chosen = trio_ok[idx]
    else:
        chosen = tagged[0]
    if chosen["name"].lower() in FORBIDDEN:
        chosen = next(n for n in names if n["name"] == "Puddle")
    return chosen


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--heat", type=float, default=4.0)
    p.add_argument("--text", default="")
    p.add_argument("--stdin", action="store_true")
    args = p.parse_args()
    text = sys.stdin.read() if args.stdin else args.text
    table = load_table()
    ctx = context_of(text, args.heat)
    chosen = pick(table, args.heat, ctx)
    out = {
        "name": chosen["name"],
        "band": ctx,
        "heat": args.heat,
        "reason": f"{ctx} @ H{args.heat:g} → {chosen['name']}",
        "trio": table["primary_trio"],
        "forbidden": table["forbidden_address"],
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

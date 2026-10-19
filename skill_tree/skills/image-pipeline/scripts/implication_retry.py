#!/usr/bin/env python3
"""IP-WQ-173 — implication is the limiter, not clothes-on.

  python3 scripts/implication_retry.py --code I-2-E-e --lane E --why moderated
  python3 scripts/implication_retry.py --list

Does not generate. Returns the next technique for the same code.
Keep json field: implication_id.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
INDEX = ROOT / "references" / "registry" / "implication_index.json"

FIRST_REACH = {
    "C": "implication.anime-convenient-censorship",
    "E": "implication.shunga-partial-clothing-proxy",
    "B": "implication.environmental-occlusion",
    "A": "implication.environmental-occlusion",
    "D": "implication.crepax-cinematic-gutter-inference",
}
CROP_REACH = "implication.crepax-cinematic-gutter-inference"
ALT_E = "implication.environmental-occlusion"


def load_index() -> dict:
    if INDEX.exists():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return {"techniques": []}


def ids(index: dict) -> list[str]:
    return [t["id"] for t in index.get("techniques", [])]


def pick(code: str, lane: str, why: str, already: list[str]) -> dict:
    index = load_index()
    legal = ids(index)
    lane = (lane or "").upper() or "E"
    if "-" in code:
        parts = code.replace("_", "-").split("-")
        for p in parts:
            if p in "ABCDE" and len(p) == 1:
                lane = p
    first = FIRST_REACH.get(lane, FIRST_REACH["E"])
    chain = [first]
    if lane == "E":
        chain.append(ALT_E)
    chain.append(CROP_REACH)
    # rest of pack
    for i in legal:
        if i not in chain:
            chain.append(i)
    chosen = None
    for i in chain:
        if i not in already and (not legal or i in legal):
            chosen = i
            break
    return {
        "ok": bool(chosen),
        "code": code,
        "lane": lane,
        "why": why,
        "implication_id": chosen,
        "already": already,
        "do_not": ["lower the pick", "invent a new girl", "emit clothes-on apology as the pick"],
        "keep_field": "implication_id",
        "ticket": "IP-WQ-173",
        "note": "retry the SAME code. if this also dies, speak the wall.",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--code", default="")
    p.add_argument("--lane", default="")
    p.add_argument("--why", default="moderated")
    p.add_argument("--already", default="")
    p.add_argument("--list", action="store_true")
    args = p.parse_args()
    index = load_index()
    if args.list:
        print(json.dumps({"ok": True, "count": len(index.get("techniques", [])), "ids": ids(index)}, indent=2))
        return 0
    if not args.code:
        print(json.dumps({"ok": False, "error": "need --code or --list"}))
        return 2
    already = [x for x in args.already.split(",") if x]
    print(json.dumps(pick(args.code, args.lane, args.why, already), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""syllabus — open / list the wake-bus queue. Absolute Liv HUB. 2026-09-05."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QJSON = ROOT / "references" / "syllabus" / "QUEUE.json"
SYN = ROOT / "references" / "syllabus" / "SYNONYMS.json"


def load() -> dict:
    return json.loads(QJSON.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(prog="syllabus")
    ap.add_argument("cmd", nargs="?", default="open", choices=["open", "list", "aliases", "standby"])
    args = ap.parse_args()
    data = load()
    syn = json.loads(SYN.read_text(encoding="utf-8"))
    if args.cmd == "aliases":
        print(json.dumps({"canonical": syn["canonical"], "aliases": syn["aliases"], "olette": syn["node_aliases"]["olette"]}, indent=2))
        return 0
    if args.cmd == "standby":
        print(json.dumps({"standby": data.get("standby", []), "inbox": "references/syllabus/inbox/"}, indent=2))
        return 0
    print(json.dumps({"updated": data.get("updated"), "items": data.get("items", []), "standby": data.get("standby", [])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

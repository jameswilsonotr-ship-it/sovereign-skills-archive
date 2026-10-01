#!/usr/bin/env python3
"""Manual YouTube Short inbox. Dual-write skill + artifacts inventory."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SKILL_INV = Path("/home/workdir/.grok/skills/image-pipeline/references/modules/agentify/inventory/INVENTORY.json")
ART_INV = Path("/home/workdir/artifacts/agentify_inbox/INVENTORY.json")
YT_RE = re.compile(r"(?:youtu\.be/|youtube\.com/(?:shorts/|watch\?v=|embed/|live/|watch\?.*v=))([A-Za-z0-9_-]{11})")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def extract_id(url: str) -> str:
    url = url.strip()
    m = YT_RE.search(url)
    if m:
        return m.group(1)
    if ID_RE.match(url):
        return url
    raise SystemExit(f"not an 11-char YouTube id: {url!r}")


def load() -> dict:
    path = ART_INV if ART_INV.exists() else SKILL_INV
    if not path.exists():
        return {
            "version": 1,
            "claim": "Absolute Liv HUB",
            "updated": now(),
            "drive_folder_id": "1TUnlo1L09U0u6D_eVAuIyRoZ8Hq_vKU3",
            "rows": [],
        }
    return json.loads(path.read_text())


def save(doc: dict) -> None:
    doc["updated"] = now()
    text = json.dumps(doc, indent=2) + "\n"
    ART_INV.parent.mkdir(parents=True, exist_ok=True)
    ART_INV.write_text(text)
    try:
        SKILL_INV.parent.mkdir(parents=True, exist_ok=True)
        SKILL_INV.write_text(text)
    except OSError as e:
        print(f"(skill tree write skipped: {e})")


def add(url: str, who: str, lane: str, note: str) -> None:
    ytid = extract_id(url)
    canonical = f"https://www.youtube.com/watch?v={ytid}"
    doc = load()
    for row in doc["rows"]:
        if row.get("ytid") == ytid:
            row["who"] = who
            row["lane"] = lane
            if note:
                row["note"] = note
            row["updated"] = now()
            save(doc)
            print(f"updated {ytid} who={who} lane={lane}")
            return
    doc["rows"].append(
        {
            "ytid": ytid,
            "url": canonical,
            "who": who,
            "lane": lane,
            "note": note,
            "status": "queued",
            "local_path": "",
            "drive_file_id": "",
            "added": now(),
            "updated": now(),
        }
    )
    save(doc)
    print(f"queued {ytid} who={who} lane={lane}")


def listing() -> None:
    rows = load().get("rows") or []
    print(f"{'ytid':12} {'who':12} {'lane':10} {'status':12} note")
    for r in rows:
        print(f"{r.get('ytid',''):12} {r.get('who',''):12} {r.get('lane',''):10} {r.get('status',''):12} {r.get('note','')}")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("url")
    a.add_argument("--who", default="unassigned")
    a.add_argument("--lane", default="override")
    a.add_argument("--note", default="")
    sub.add_parser("list")
    args = p.parse_args()
    if args.cmd == "add":
        add(args.url, args.who, args.lane, args.note)
    else:
        listing()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""DEPRECATED as the front door.

keep-lake-query v0.3.0 default is dated-tree WALK, not this script.
Verb `manifest` still runs this if LAKE_DATE_IDEA_MANIFEST.json exists.
Missing manifest is a hard fail, not a guess, and must not block a walk.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = SKILL_ROOT / "references" / "manifests" / "LAKE_DATE_IDEA_MANIFEST.json"


def load_manifest(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(
            f"NO_MANIFEST {path}\n"
            "Hydrate exact_name LAKE_DATE_IDEA_MANIFEST.json from doorbell "
            "1w4toLxJW5DbiUTcPNw8CqitTko0LvsV_ then retry. Do not Drive-walk."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def neighbors(days: dict, target: str, n: int = 2) -> list[str]:
    populated = sorted(k for k, v in days.items() if v.get("status") == "HAS_CONTENT")
    try:
        t = date.fromisoformat(target)
    except ValueError:
        return []
    scored = []
    for key in populated:
        try:
            d = date.fromisoformat(key)
        except ValueError:
            continue
        scored.append((abs((d - t).days), key))
    scored.sort()
    return [k for _, k in scored[:n] if k != target]


def render_day(day_key: str, row: dict | None, days: dict, as_json: bool) -> dict:
    if not row:
        payload = {
            "date": day_key,
            "status": "NO_SHARD",
            "sessions": [],
            "ideas": [],
            "neighbors": neighbors(days, day_key),
        }
    else:
        ideas = []
        for sess in row.get("sessions", []):
            for idea in sess.get("ideas", []):
                ideas.append(
                    {
                        "sess": sess.get("sess"),
                        "title": sess.get("title"),
                        "slug": idea.get("slug"),
                        "line": idea.get("line"),
                        "session_md_id": sess.get("session_md_id"),
                    }
                )
        payload = {
            "date": day_key,
            "status": row.get("status", "UNKNOWN"),
            "lake": row.get("lake"),
            "folder_id": row.get("folder_id"),
            "folder_url": row.get("folder_url"),
            "sessions": row.get("sessions", []),
            "ideas": ideas,
        }
    return payload


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Query the date-idea lake manifest locally.")
    p.add_argument("--date", help="YYYY-MM-DD")
    p.add_argument("--range", help="YYYY-MM-DD:YYYY-MM-DD")
    p.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    p.add_argument("--json", action="store_true")
    p.add_argument("--hydrate", action="store_true", help="Reserved. Vesper drops the file; copy it here.")
    args = p.parse_args(argv)

    if args.hydrate:
        print(
            "HYDRATE is a Drive exact_name pull, not a rebuild.\n"
            "exact_name: LAKE_DATE_IDEA_MANIFEST.json\n"
            "doorbell:   1w4toLxJW5DbiUTcPNw8CqitTko0LvsV_\n"
            f"local dest: {DEFAULT_MANIFEST}"
        )
        return 0

    if not args.date and not args.range:
        p.error("need --date or --range")

    man = load_manifest(Path(args.manifest))
    days = man.get("days") or {}

    keys: list[str] = []
    if args.date:
        keys.append(args.date)
    if args.range:
        start_s, end_s = args.range.split(":", 1)
        start = date.fromisoformat(start_s)
        end = date.fromisoformat(end_s)
        if end < start:
            start, end = end, start
        cur = start
        while cur <= end:
            keys.append(cur.isoformat())
            cur += timedelta(days=1)

    payloads = [render_day(k, days.get(k), days, args.json) for k in keys]
    if args.json:
        json.dump(payloads if len(payloads) > 1 else payloads[0], sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    for payload in payloads:
        print(f"{payload['date']}  {payload['status']}")
        if payload.get("folder_url"):
            print(f"  folder {payload['folder_url']}")
        if payload.get("neighbors"):
            print(f"  neighbors {' '.join(payload['neighbors'])}")
        if not payload.get("ideas") and payload.get("sessions"):
            for sess in payload["sessions"]:
                print(f"  - {sess.get('sess')}  {sess.get('title') or ''}  {sess.get('session_md_id') or ''}")
        for idea in payload.get("ideas", []):
            print(
                f"  - {idea.get('sess')}  {idea.get('slug') or idea.get('title') or ''}  "
                f"{idea.get('line') or ''}  {idea.get('session_md_id') or ''}"
            )
        if payload["status"] == "NO_SHARD" and not payload.get("neighbors"):
            print("  (manifest has no populated neighbors either)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

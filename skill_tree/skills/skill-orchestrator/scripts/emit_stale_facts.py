#!/usr/bin/env python3
"""
emit_stale_facts.py — Emit STALE_FACT lines for skills idle ≥ 7 days.

Uses completeness registry + optional debug status. Does NOT write the alpha work queue.

Usage:
  python scripts/emit_stale_facts.py
  python scripts/emit_stale_facts.py --window-days 7
  python scripts/emit_stale_facts.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

COMP = Path(__file__).resolve().parent.parent / "references" / "inventory" / "completeness"
OPTED_IN = {
    "grok-imagine-generate-engine",
    "grok-imagine-overlay-engine",
    "chaos-bratz-roster",
    "format-bible",
}


def parse_ts(s: str) -> datetime:
    s = s.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.now(timezone.utc) - timedelta(days=999)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window-days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    latest_path = COMP / "latest.json"
    if not latest_path.exists():
        print("No completeness latest.json — run audit first", file=sys.stderr)
        return 2

    latest = json.loads(latest_path.read_text())
    now = datetime.now(timezone.utc)
    # Per-skill last activity ≈ last completeness run time for now
    # (finer grain can use per-skill history later)
    run_ts = parse_ts(latest.get("timestamp", now.isoformat()))
    days_idle = (now - run_ts).days

    facts = []
    # If the whole library run is fresh, individual skills from that run aren't stale
    # Stale detection needs per-skill last-change; use registry of runs when available
    registry_path = COMP / "registry.json"
    skill_last = {}  # slug -> datetime of last run that mentioned them

    if registry_path.exists():
        reg = json.loads(registry_path.read_text())
        for entry in reg:
            ts = parse_ts(entry.get("timestamp", ""))
            # load that run's results if present
            run_rel = entry.get("run_json")
            if not run_rel:
                continue
            run_path = COMP / run_rel
            if not run_path.exists():
                continue
            try:
                payload = json.loads(run_path.read_text())
            except Exception:
                continue
            for r in payload.get("results", []):
                slug = r.get("slug")
                if not slug:
                    continue
                prev = skill_last.get(slug)
                if prev is None or ts > prev:
                    skill_last[slug] = ts

    if not skill_last:
        # fallback: all skills in latest share latest timestamp
        for r in latest.get("results", []):
            skill_last[r["slug"]] = run_ts

    for slug, last in sorted(skill_last.items()):
        idle = (now - last).days
        if idle < args.window_days:
            continue
        source = "completeness"
        fact = {
            "line": f"STALE_FACT skill={slug} last_activity={last.strftime('%Y-%m-%dT%H:%M:%SZ')} days_idle={idle} source={source} window_days={args.window_days}",
            "skill": slug,
            "last_activity": last.isoformat(),
            "days_idle": idle,
            "opted_in": slug in OPTED_IN,
            "action_if_opted_in": "set mode=idle" if slug in OPTED_IN else None,
        }
        facts.append(fact)

    if args.json:
        print(json.dumps({"window_days": args.window_days, "stale_count": len(facts), "facts": facts}, indent=2))
    else:
        if not facts:
            print(f"No STALE_FACT emissions (window={args.window_days}d).")
        for f in facts:
            print(f["line"])
            if f["opted_in"]:
                print(f"  → opted-in: would set mode=idle (orchestrator debug table)")
            print(f"  → alpha: move matching WQ items to state=stale (alpha writes queue)")

    # Save last emission report for alpha to read
    out = COMP / "stale_facts_latest.json"
    out.write_text(json.dumps({"emitted_at": now.isoformat(), "window_days": args.window_days, "facts": facts}, indent=2))
    print(f"[saved] {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

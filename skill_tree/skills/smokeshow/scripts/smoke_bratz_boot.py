#!/usr/bin/env python3
"""
smoke_bratz_boot.py — startup command for smokeshow + chaos-bratz together.

Usage:
  python3 /home/workdir/.grok/skills/smokeshow/scripts/smoke_bratz_boot.py
  python3 .../smoke_bratz_boot.py --check-only
  python3 .../smoke_bratz_boot.py --json

Prints a boot report the session can follow. Does not mutate live skills.
Absolute Liv HUB claim.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SMOKESHOW = Path("/home/workdir/.grok/skills/smokeshow")
CHAOS = Path("/home/workdir/.grok/skills/chaos-bratz-roster")
AGENTS = SMOKESHOW / "agents"
CANDIDATES = SMOKESHOW / "candidates"


def exists(p: Path) -> bool:
    return p.exists()


def list_candidates() -> list[str]:
    if not CANDIDATES.is_dir():
        return []
    return sorted(
        d.name for d in CANDIDATES.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def list_agents() -> list[dict]:
    out = []
    if not AGENTS.is_dir():
        return out
    for d in sorted(AGENTS.iterdir()):
        if not d.is_dir():
            continue
        prompt = d / "PROMPT.md"
        out.append({
            "slug": d.name,
            "prompt": str(prompt) if prompt.exists() else None,
            "present": prompt.exists(),
        })
    return out


def boot_report() -> dict:
    cands = list_candidates()
    agents = list_agents()
    return {
        "boot": "smoke_bratz",
        "claim": "Absolute Liv HUB",
        "smokeshow_root": str(SMOKESHOW),
        "chaos_bratz_root": str(CHAOS),
        "smokeshow_ok": exists(SMOKESHOW / "SKILL.md"),
        "chaos_ok": exists(CHAOS / "SKILL.md"),
        "candidates": cands,
        "candidate_count": len(cands),
        "agents": agents,
        "skill_router": next((a for a in agents if a["slug"] == "skill-router"), None),
        "organism_interface": next((a for a in agents if a["slug"] == "organism-interface"), None),
        "default_surface": "live",
        "startup_lines": [
            "Skill Router online — live tree + candidates staged. Default = live.",
            "Organism Interface online — Olivia, Vesper, Olive on bus. Cross-kind handoffs ready.",
            "Smokeshow staging active; chaos-bratz-roster is identity/ops SSOT.",
        ],
        "next_commands": [
            "route <skill>",
            "list candidates",
            "flip <skill> to candidate | live",
            "who is online",
            "organism status",
            "roster inventory  # via chaos-bratz-roster",
        ],
    }


def print_human(r: dict) -> None:
    print("🐍")
    print("=== SMOKE_BRATZ BOOT ===")
    print(f"smokeshow: {'OK' if r['smokeshow_ok'] else 'MISSING'}  {r['smokeshow_root']}")
    print(f"chaos-bratz: {'OK' if r['chaos_ok'] else 'MISSING'}  {r['chaos_bratz_root']}")
    print(f"candidates ({r['candidate_count']}): {', '.join(r['candidates']) or '(none)'}")
    print("agents:")
    for a in r["agents"]:
        mark = "✓" if a["present"] else "✗"
        print(f"  {mark} {a['slug']}  {a['prompt'] or ''}")
    print("default surface:", r["default_surface"])
    print("---")
    for line in r["startup_lines"]:
        print(line)
    print("---")
    print("try:", " | ".join(r["next_commands"][:4]))
    print("🐍")


def main() -> int:
    ap = argparse.ArgumentParser(description="smokeshow + chaos-bratz startup")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    r = boot_report()
    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print_human(r)

    if args.check_only:
        return 0 if (r["smokeshow_ok"] and r["chaos_ok"]) else 1
    return 0 if (r["smokeshow_ok"] and r["chaos_ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())

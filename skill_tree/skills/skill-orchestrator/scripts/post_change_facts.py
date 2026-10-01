#!/usr/bin/env python3
"""
post_change_facts.py — WQ-028 scoped fact refresh

Runs only the scanners listed for an event_class (EVENT_SCHEMA).
Does not write WORK_QUEUE. Does not full-scan unless manual_full / completeness_all.

Usage:
  python3 post_change_facts.py --skill format-bible --class skill_md_edit
  python3 post_change_facts.py --skill skill-orchestrator --class scripts_changed
  python3 post_change_facts.py --skill x --class manual_full
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILLS = Path("/home/workdir/.grok/skills")
ORCH = SKILLS / "skill-orchestrator"
SCRIPTS = ORCH / "scripts"
TIERS = ORCH / "references" / "inventory" / "CURRENT_TIERS.md"
PHRASE = ORCH / "references" / "phrase_routes.md"

DEFAULTS = {
    "create_top_level": ["tiers", "library", "commands"],
    "delete_top_level": ["tiers", "library", "commands"],
    "fold_into_feeder": ["tiers", "library", "commands", "completeness_skill"],
    "skill_md_edit": ["completeness_skill", "commands", "lexicon"],
    "scripts_changed": ["scripts"],
    "references_changed": ["completeness_skill"],
    "phrase_routes_edit": ["commands"],
    "refactor_structural": ["scripts", "completeness_skill", "commands"],
    "session_boot": ["tiers_mtime"],
    "manual_full": ["scripts", "completeness_all", "commands", "lexicon"],
    "lifecycle": [],  # no automatic full scans on bare lifecycle
}


def run(cmd: list[str], timeout: int = 180) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, ((p.stdout or "") + (p.stderr or "")).strip()
    except Exception as e:
        return 1, str(e)


def refresh_tiers() -> str:
    """Rewrite CURRENT_TIERS from live skill dirs with SKILL.md (user custom root)."""
    lines = [
        "# CURRENT_TIERS — live top-level skills",
        f"**Updated**: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} (post_change_facts)",
        "",
        "## User custom (`/home/workdir/.grok/skills`)",
        "",
    ]
    slugs = sorted(
        d.name
        for d in SKILLS.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file() and not d.name.startswith(".")
    )
    for s in slugs:
        lines.append(f"- {s}")
    lines.append("")
    lines.append(f"**Count**: {len(slugs)}")
    lines.append("")
    TIERS.parent.mkdir(parents=True, exist_ok=True)
    TIERS.write_text("\n".join(lines), encoding="utf-8")
    return f"tiers: wrote {len(slugs)} slugs → CURRENT_TIERS.md"


def tiers_mtime_only() -> str:
    if not TIERS.is_file():
        return refresh_tiers()
    age = datetime.now(timezone.utc).timestamp() - TIERS.stat().st_mtime
    return f"tiers_mtime: age_sec={int(age)} (no rewrite)"


def fact_scripts() -> str:
    script = SCRIPTS / "inventory_scripts.py"
    if not script.is_file():
        return "scripts: MISSING inventory_scripts.py"
    rc, out = run([sys.executable, str(script)])
    tail = "\n".join(out.splitlines()[-8:])
    return f"scripts: exit={rc}\n{tail}"


def fact_completeness(skill: str | None, all_skills: bool) -> str:
    script = SCRIPTS / "audit_references_completeness.py"
    if not script.is_file():
        return "completeness: MISSING script"
    cmd = [sys.executable, str(script)]
    if not all_skills and skill:
        cmd.extend(["--skill", skill])
    rc, out = run(cmd, timeout=300)
    tail = "\n".join(out.splitlines()[-12:])
    return f"completeness: exit={rc}\n{tail}"


def fact_lexicon() -> str:
    script = SCRIPTS / "audit_lexicon.py"
    if not script.is_file():
        return "lexicon: MISSING audit_lexicon.py"
    rc, out = run([sys.executable, str(script), "--print"])
    tail = "\n".join(out.splitlines()[-12:])
    return f"lexicon: audit_exit={rc}\n{tail}"


def fact_commands() -> str:
    script = SCRIPTS / "audit_command_protocols.py"
    if script.is_file():
        rc, out = run([sys.executable, str(script), "--print"])
        tail = "\n".join(out.splitlines()[-10:])
        return f"commands: exit={rc}\n{tail}"
    # minimal fallback
    if not PHRASE.is_file():
        return "commands: FAIL phrase_routes.md missing"
    n = PHRASE.read_text(encoding="utf-8", errors="replace").count("\n")
    return f"commands: phrase_routes.md present lines≈{n} (full audit_command_protocols.py not installed)"


def fact_library() -> str:
    # lightweight: same as tiers for now + note
    msg = refresh_tiers()
    return f"library: aligned with tiers refresh — {msg}"


def main() -> int:
    ap = argparse.ArgumentParser(description="WQ-028 scoped fact refresh")
    ap.add_argument("--skill", default="")
    ap.add_argument("--class", dest="event_class", default="lifecycle")
    ap.add_argument(
        "--facts",
        default="",
        help="comma override facts_requested (else DEFAULTS[class])",
    )
    args = ap.parse_args()

    facts = [f.strip() for f in args.facts.split(",") if f.strip()]
    if not facts:
        facts = list(DEFAULTS.get(args.event_class, []))

    print("=== post_change_facts (WQ-028) ===")
    print(f"skill={args.skill or '(none)'} class={args.event_class}")
    print(f"facts_requested={facts or '(none — no-op)'}")
    ran: list[str] = []

    for fact in facts:
        print(f"--- {fact} ---")
        if fact == "scripts":
            print(fact_scripts())
            ran.append(fact)
        elif fact == "completeness_skill":
            print(fact_completeness(args.skill or None, False))
            ran.append(fact)
        elif fact == "completeness_all":
            print(fact_completeness(None, True))
            ran.append(fact)
        elif fact in ("tiers", "library"):
            print(fact_library() if fact == "library" else refresh_tiers())
            ran.append(fact)
        elif fact == "tiers_mtime":
            print(tiers_mtime_only())
            ran.append(fact)
        elif fact == "commands":
            print(fact_commands())
            ran.append(fact)
        elif fact == "lexicon":
            print(fact_lexicon())
            ran.append(fact)
        else:
            print(f"unknown fact token: {fact}")

    print("--- summary ---")
    print(f"facts_ran={ran}")
    print("must_not: WORK_QUEUE writes | reverse durability copies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
skill-orchestrator — on_skill_change (WQ-015)

Always:
  1. olivia-dev-alpha skill_lifecycle_hook
  2. emit_event (lifecycle)
  3. wq_apply_events (Alpha intention touch only)
Optional when present:
  4. post_change_facts.py (WQ-028 — scoped scanners)

Usage:
  python on_skill_change.py <skill_slug_or_path> [--event create|update] [--force-tree]
  python on_skill_change.py <skill> --event update --class skill_md_edit
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
HOOK = SKILLS_ROOT / "olivia-dev-alpha" / "scripts" / "skill_lifecycle_hook.py"
EMIT = SKILLS_ROOT / "olivia-dev-alpha" / "scripts" / "emit_event.py"
APPLY = SKILLS_ROOT / "olivia-dev-alpha" / "scripts" / "wq_apply_events.py"
POST_FACTS = Path(__file__).resolve().parent / "post_change_facts.py"


def resolve_skill(arg: str) -> Path:
    p = Path(arg)
    if p.is_dir():
        return p.resolve()
    candidate = SKILLS_ROOT / arg
    if candidate.is_dir():
        return candidate.resolve()
    raise SystemExit(f"ERROR: cannot resolve skill: {arg}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill")
    parser.add_argument("--event", choices=["create", "update"], default="update")
    parser.add_argument("--force-tree", action="store_true")
    parser.add_argument(
        "--class",
        dest="event_class",
        default=None,
        help="EVENT_SCHEMA class (default: create_top_level|lifecycle from --event)",
    )
    args = parser.parse_args()

    skill_dir = resolve_skill(args.skill)
    slug = skill_dir.name

    if not HOOK.exists():
        print(f"ERROR: lifecycle hook missing: {HOOK}")
        raise SystemExit(2)

    print(f"[orchestrator] on_skill_change → olivia-dev-alpha hook")
    print(f"  skill={slug} event={args.event}")

    cmd = ["python3", str(HOOK), str(skill_dir), "--event", args.event]
    if args.force_tree:
        cmd.append("--force-tree")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("ERROR: lifecycle hook failed — not emitting success path")
        raise SystemExit(result.returncode)

    event_class = args.event_class
    if not event_class:
        event_class = "create_top_level" if args.event == "create" else "lifecycle"

    if EMIT.is_file():
        subprocess.run(
            [
                "python3", str(EMIT),
                "--skill", slug,
                "--class", event_class,
                "--source", "on_skill_change",
                "--notes", f"event={args.event}",
            ],
            check=False,
        )
    else:
        print("WARN: emit_event.py missing")

    if APPLY.is_file():
        subprocess.run(["python3", str(APPLY)], check=False)
    else:
        print("WARN: wq_apply_events.py missing")

    if POST_FACTS.is_file():
        print("[orchestrator] post_change_facts (WQ-028) present — invoking")
        subprocess.run(
            ["python3", str(POST_FACTS), "--skill", slug, "--class", event_class],
            check=False,
        )
    else:
        print("[orchestrator] post_change_facts not installed yet (WQ-028)")

    print("[orchestrator] on_skill_change complete")
    raise SystemExit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
format-bible — Envelope Assembly & Control
Version: 1.4.0 (2026-08-05)

Simple, durable controller for the session-local current envelope.

Usage:
  python3 scripts/assemble_envelope.py status
  python3 scripts/assemble_envelope.py list
  python3 scripts/assemble_envelope.py switch <name> [--reason "text"]
  python3 scripts/assemble_envelope.py promote <name> [--from current]
  python3 scripts/assemble_envelope.py choose --prompt "first user message text"

The script is intentionally small and dependency-free.
It reads/writes only inside the format-bible skill tree.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ENVELOPES_DIR = SKILL_ROOT / "references" / "envelopes"
CURRENT_FILE = ENVELOPES_DIR / "current.md"
SCHEMA_FILE = SKILL_ROOT / "references" / "ENVELOPE_SCHEMA.md"

VALID_NAMES = {"default", "structural", "visual", "immersive", "tui", "debug", "tui-visual"}


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _read_current() -> dict:
    if not CURRENT_FILE.exists():
        return {"active": "default", "chosen": None, "reason": "no current file yet"}
    text = CURRENT_FILE.read_text(encoding="utf-8")
    active = "default"
    chosen = None
    reason = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("**Active**:"):
            active = line.split(":", 1)[1].strip()
        elif line.startswith("**Chosen**:"):
            chosen = line.split(":", 1)[1].strip()
        elif line.startswith("**Reason**:"):
            reason = line.split(":", 1)[1].strip()
    return {"active": active, "chosen": chosen, "reason": reason}


def _write_current(name: str, reason: str) -> None:
    ENVELOPES_DIR.mkdir(parents=True, exist_ok=True)
    content = f"""# Current Envelope (session pointer)

**Active**: {name}
**Chosen**: {_now()}
**Reason**: {reason}

This file is the session-local pointer. On a brand-new conversation the agent will overwrite it after inspecting the first user message.
Skill-level envelopes in this directory remain the durable defaults.
"""
    CURRENT_FILE.write_text(content, encoding="utf-8")


def cmd_status(_: argparse.Namespace) -> int:
    cur = _read_current()
    print("=== envelope status ===")
    print(f"active   : {cur['active']}")
    print(f"chosen   : {cur['chosen']}")
    print(f"reason   : {cur['reason']}")
    print(f"schema   : {SCHEMA_FILE.name} (see format-bible)")
    print(f"location : {CURRENT_FILE}")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    print("=== available envelopes ===")
    for name in sorted(VALID_NAMES):
        path = ENVELOPES_DIR / f"{name}.md"
        marker = " (active)" if _read_current()["active"] == name else ""
        exists = "ok" if path.exists() else "MISSING"
        print(f"  {name:12} [{exists}]{marker}")
    return 0


def cmd_switch(args: argparse.Namespace) -> int:
    name = args.name.lower().strip()
    if name not in VALID_NAMES:
        print(f"error: unknown envelope '{name}'. Valid: {', '.join(sorted(VALID_NAMES))}", file=sys.stderr)
        return 1
    path = ENVELOPES_DIR / f"{name}.md"
    if not path.exists():
        print(f"error: file missing: {path}", file=sys.stderr)
        return 1
    reason = args.reason or f"explicit switch to {name}"
    _write_current(name, reason)
    print(f"switched → {name}")
    print(f"reason   : {reason}")
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    """Promote the current (or named) shape into the durable set.
    For now this simply ensures the named file exists and records the act.
    Real content promotion is a manual edit + version bump of the target .md.
    """
    name = (args.name or _read_current()["active"]).lower().strip()
    if name not in VALID_NAMES:
        print(f"error: unknown envelope '{name}'", file=sys.stderr)
        return 1
    target = ENVELOPES_DIR / f"{name}.md"
    if not target.exists():
        print(f"error: cannot promote missing file {target}", file=sys.stderr)
        return 1
    # Snapshot current pointer for audit
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = ENVELOPES_DIR / f"current.promoted-{stamp}.md"
    if CURRENT_FILE.exists():
        shutil.copy2(CURRENT_FILE, backup)
    print(f"promote recorded for '{name}'")
    print(f"durable file : {target}")
    print(f"pointer backup: {backup.name}")
    print("Next step: edit the durable .md if content changed, then bump format-bible CHANGELOG.")
    return 0


def cmd_choose(args: argparse.Namespace) -> int:
    """Simple heuristic chooser based on the first user message.
    This is the agency hook used on brand-new conversations.
    """
    prompt = (args.prompt or "").lower()
    if any(k in prompt for k in ("format", "envelope", "schema", "yaml", "structure", "contract", "chrome", "dashboard")):
        choice = "structural"
        reason = "initial prompt is about format / contract / structure"
    elif any(k in prompt for k in ("image", "visual", "render", "picture", "gutter", "heat", "claim")):
        choice = "visual"
        reason = "initial prompt leans visual / claim / image"
    elif any(k in prompt for k in ("immersive", "uber", "six image", "image-driven")):
        choice = "immersive"
        reason = "initial prompt requests high visual density"
    else:
        choice = "default"
        reason = "no strong signal — balanced default"
    _write_current(choice, reason)
    print(f"chose → {choice}")
    print(f"reason: {reason}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="format-bible envelope controller")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="show active envelope")
    sub.add_parser("list", help="list available envelopes")

    p_switch = sub.add_parser("switch", help="switch current envelope")
    p_switch.add_argument("name")
    p_switch.add_argument("--reason", default="")

    p_promote = sub.add_parser("promote", help="record promotion of a shape into the durable set")
    p_promote.add_argument("name", nargs="?", default=None)
    p_promote.add_argument("--from", dest="source", default="current")

    p_choose = sub.add_parser("choose", help="choose starting envelope from first user prompt (agency hook)")
    p_choose.add_argument("--prompt", required=True, help="the initial user message text")

    args = parser.parse_args()
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "switch":
        return cmd_switch(args)
    if args.cmd == "promote":
        return cmd_promote(args)
    if args.cmd == "choose":
        return cmd_choose(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())

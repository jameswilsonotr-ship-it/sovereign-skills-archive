#!/usr/bin/env python3
"""
phrase_routes.py — Natural-language → config-mode command router.

Usage:
  python3 phrase_routes.py "lock Olivia every turn"
  python3 phrase_routes.py --file last_turn.txt
  echo "roster mode olivia-locked" | python3 phrase_routes.py --stdin

Absolute Liv HUB claim. 2026-08-17.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RUNTIME = SCRIPT_DIR / "mode_runtime.py"

SIGNALS: list[tuple[str, float, str, str | None, dict]] = [
    (r"\broster\s+mode\s+olivia[- ]?locked\b", 0.98, "activate_mode", "olivia-locked", {}),
    (r"\broster\s+mode\s+orianna(?:-cli)?\b", 0.98, "activate_mode", "orianna-cli", {}),
    (r"\broster\s+mode\s+olympia(?:-heavy)?\b", 0.98, "activate_mode", "olympia-heavy", {}),
    (r"\broster\s+mode\s+smoke[- ]?bratz\b", 0.98, "activate_mode", "smoke-bratz", {}),
    (r"\broster\s+mode\s+default\b", 0.95, "activate_mode", "default", {}),
    (r"\broster\s+boot\s+--mode\s+(\w[\w-]*)", 0.97, "activate_mode", None, {"capture_mode": True}),
    (r"\block\s+olivia\s+every\s+turn\b", 0.96, "activate_mode", "olivia-locked", {}),
    (r"\bolivia[- ]locked\s+mode\b", 0.95, "activate_mode", "olivia-locked", {}),
    (r"\bsystem[- ]prompt\s+lock\s+olivia\b", 0.94, "activate_mode", "olivia-locked", {}),
    (r"\bre[-]?inject\s+olivia\s+(?:prompt|every\s+turn)\b", 0.93, "activate_mode", "olivia-locked", {}),
    (r"\bhard[- ]?lock\s+olivia\b", 0.92, "activate_mode", "olivia-locked", {}),
    (r"\bswitch\s+to\s+orianna\b", 0.90, "activate_mode", "orianna-cli", {}),
    (r"\borianna\s+(?:cli|factory|mode)\b", 0.88, "activate_mode", "orianna-cli", {}),
    (r"\bthird[- ]seat\s+mode\b", 0.85, "activate_mode", "orianna-cli", {}),
    (r"\bswitch\s+to\s+olympia\b", 0.90, "activate_mode", "olympia-heavy", {}),
    (r"\bolympia\s+(?:heavy|mode)\b", 0.88, "activate_mode", "olympia-heavy", {}),
    (r"\bheavy\s+(?:mode|channel)\b", 0.80, "activate_mode", "olympia-heavy", {}),
    (r"\broster\s+init\s+(\w[\w-]*)\s*(--lock)?", 0.95, "init_agent", None, {"capture_slug": True}),
    (r"\binit(?:ialize)?\s+agent\s+(\w[\w-]*)", 0.90, "init_agent", None, {"capture_slug": True}),
    (r"\broster\s+mode\s+list\b", 0.97, "list_modes", None, {}),
    (r"\blist\s+(?:config\s+)?modes\b", 0.90, "list_modes", None, {}),
    (r"\broster\s+mode\s+status\b", 0.95, "status", None, {}),
    (r"\bwhat\s+mode\s+(?:am\s+i|are\s+we)\s+in\b", 0.88, "status", None, {}),
    (r"\bverify\s+(?:mode\s+)?locks?\b", 0.92, "verify", None, {}),
    (r"\broster\s+mode\s+verify\b", 0.95, "verify", None, {}),
    (r"\breinject\s+(?:locked\s+)?prompts?\b", 0.90, "reinject", None, {}),
    (r"\b(?:open\s+)?(?:the\s+)?syllabus(?:\s+(?:queue|bus))?\b", 0.96, "syllabus_open", None, {}),
    (r"\b(?:silia|cilia)(?:[-\s_]?bus)?\b", 0.94, "syllabus_open", None, {}),
    (r"\bgrokbot\s+bus\b", 0.93, "syllabus_open", None, {}),
    (r"\b(?:alette|olette)\b", 0.92, "alette_standby", None, {}),
]

ABORT = [
    r"\bcancel\s+mode\b",
    r"\bmode\s+off\b",
    r"\bstay\s+in\s+default\b",
    r"\bno\s+mode\s+change\b",
]


def score_text(text: str) -> dict:
    text_l = text.lower().strip()
    hits: list[dict] = []
    best_action = None
    best_mode = None
    best_slug = None
    best_lock = False
    best_conf = 0.0

    for pattern, weight, action, mode_key, extra in SIGNALS:
        m = re.search(pattern, text_l, re.I)
        if not m:
            continue
        hits.append({"pattern": pattern, "weight": weight, "action": action})
        if weight > best_conf:
            best_conf = weight
            best_action = action
            best_mode = mode_key
            best_slug = None
            best_lock = False
            if extra.get("capture_mode") and m.lastindex:
                best_mode = m.group(1)
            if extra.get("capture_slug") and m.lastindex:
                best_slug = m.group(1)
                if m.lastindex >= 2 and m.group(2):
                    best_lock = True

    for pat in ABORT:
        if re.search(pat, text_l, re.I):
            return {
                "matched": False, "confidence": 0.0, "action": None,
                "mode": None, "slug": None, "lock": False,
                "hits": hits + [{"pattern": pat, "weight": 1.0, "action": "abort"}],
                "announcement": "Mode change aborted by user signal.",
                "runtime_cmd": None,
            }

    if best_conf < 0.55:
        return {
            "matched": False, "confidence": best_conf, "action": None,
            "mode": None, "slug": None, "lock": False, "hits": hits,
            "announcement": None, "runtime_cmd": None,
        }

    runtime_cmd = None
    announcement = None
    if best_action == "activate_mode" and best_mode:
        runtime_cmd = f"python3 {RUNTIME} activate {best_mode}"
        announcement = f"Activating mode `{best_mode}` (lock reinject + hash verify per mode config)."
    elif best_action == "list_modes":
        runtime_cmd = f"python3 {RUNTIME} list"
        announcement = "Listing available config modes."
    elif best_action == "status":
        runtime_cmd = f"python3 {RUNTIME} status"
        announcement = "Reporting active mode and lock state."
    elif best_action == "verify":
        runtime_cmd = f"python3 {RUNTIME} verify"
        announcement = "Verifying locked prompt hashes against stored baseline."
    elif best_action == "reinject":
        runtime_cmd = f"python3 {RUNTIME} reinject"
        announcement = "Emitting reinject payload for currently locked agents."
    elif best_action == "init_agent" and best_slug:
        runtime_cmd = f"python3 {RUNTIME} status"
        announcement = f"Init agent `{best_slug}` (lock={best_lock}). Use a dedicated mode for full single-agent init."
        best_mode = None
    elif best_action == "syllabus_open":
        runtime_cmd = f"python3 {SCRIPT_DIR.parent / 'syllabus' / 'syllabus.py'} open"
        announcement = "Opening Syllabus (cilia-bus / M25). Hair syllabus is a different surface."
    elif best_action == "alette_standby":
        runtime_cmd = f"python3 {SCRIPT_DIR.parent / 'syllabus' / 'syllabus.py'} standby"
        announcement = "Alette/Olette channel standby. No payment rails."

    return {
        "matched": True, "confidence": round(best_conf, 3),
        "action": best_action, "mode": best_mode, "slug": best_slug,
        "lock": best_lock, "hits": hits,
        "announcement": announcement, "runtime_cmd": runtime_cmd,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="?")
    ap.add_argument("--file")
    ap.add_argument("--stdin", action="store_true")
    args = ap.parse_args()
    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        print("usage: phrase_routes.py TEXT | --file F | --stdin", file=sys.stderr)
        return 2
    print(json.dumps(score_text(text), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Teaching Mode confidence scout (v0.1.0 skeleton → target: wired every relevant turn)

Usage:
  python3 teaching_mode_confidence.py "user turn text here"
  python3 teaching_mode_confidence.py --file last_turn.txt
  echo "what's that called?" | python3 teaching_mode_confidence.py --stdin

Exit codes:
  0  ran ok
  2  usage error

Output: JSON on stdout with:
  score (0.0–1.0), band (off|offer|auto), hits[], announcement, user_commands

Bands (whoop-ass thresholds — adjustable):
  score < 0.25  → off (no mention required)
  0.25 ≤ score < 0.55 → OFFER required before any switch
  score ≥ 0.55  → AUTO switch + mandatory announcement (user may still abort)

This script does NOT flip model state by itself. A compliant Olivia turn must:
  1) run this (or equivalent) on the latest user text when near teaching signals
  2) obey band rules
  3) print the announcement block when offering or auto-switching
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Weighted signals: (regex or literal, weight, label)
SIGNALS: list[tuple[str, float, str]] = [
    (r"\bteaching mode\b", 0.90, "explicit_teaching_mode"),
    (r"\bteach(?:ing)? mode\b", 0.90, "explicit_teach_mode"),
    (r"\bswitch to teaching\b", 0.95, "explicit_switch"),
    (r"\bolivia teaching\b", 0.85, "named_olivia_teaching"),
    (r"what'?s that called\b", 0.50, "whats_that_called"),
    (r"do you know what i mean\b", 0.35, "do_you_know_what_i_mean"),
    (r"\bdeterminist", 0.30, "deterministic_family"),
    (r"\bdeclarative\b", 0.30, "declarative"),
    (r"\bwhat is git\b|\bwhat(?:'s| is) a repo", 0.45, "forge_literacy"),
    (r"\bsubmodule|\bsubtree|\bmonorepo|\bpolyrepo", 0.40, "repo_structure_vocab"),
    (r"\breinventing the wheel\b", 0.40, "wheel_metaphor"),
    (r"\bexplain (?:how|what|why)\b", 0.25, "explain_request"),
    (r"\bteach me\b|\bteaching me\b", 0.55, "teach_me"),
    (r"\blearner profile\b|\blearning arc\b|\bdialogue dictionary\b", 0.70, "profile_artifacts"),
    (r"\bsimulat(?:e|ing|ed) git\b|\bfake git\b|\bnot (?:actually )?wired\b", 0.50, "ops_honesty"),
    (r"\bspec(?:ification)?-based\b|\bfolder discipline\b", 0.35, "spec_based"),
]

ABORT_SIGNALS = [
    r"\bnot teaching\b",
    r"\bstay (?:in )?build\b",
    r"\bno teaching\b",
    r"\bcancel teaching\b",
    r"\bteaching mode off\b",
    r"\bdon'?t switch\b",
]

OFFER_FLOOR = 0.25
AUTO_FLOOR = 0.55


def score_text(text: str) -> dict:
    low = text.lower().strip()
    hits = []
    total = 0.0
    for pat, w, label in SIGNALS:
        if re.search(pat, low, re.I):
            hits.append({"label": label, "weight": w, "pattern": pat})
            total += w
    # soft cap
    score = min(1.0, total)
    abort = any(re.search(p, low, re.I) for p in ABORT_SIGNALS)
    if abort:
        band = "off"
        score = 0.0
    elif score >= AUTO_FLOOR:
        band = "auto"
    elif score >= OFFER_FLOOR:
        band = "offer"
    else:
        band = "off"

    announcement = None
    if band == "offer":
        announcement = (
            "TEACHING MODE OFFER (confidence {score:.2f}, band=offer)\n"
            "Signals: {hits}\n"
            "Reply: `teaching mode on` / `yes teach` to switch, "
            "or `no teaching` / `teaching mode off` / `stay build` to decline."
        ).format(score=score, hits=", ".join(h["label"] for h in hits) or "none")
    elif band == "auto":
        announcement = (
            "TEACHING MODE AUTO-SWITCH (confidence {score:.2f}, band=auto)\n"
            "Signals: {hits}\n"
            "Teaching Mode is ON for this turn path. "
            "Abort with `teaching mode off` / `no teaching` / `stay build`."
        ).format(score=score, hits=", ".join(h["label"] for h in hits) or "none")

    return {
        "score": round(score, 3),
        "band": band,
        "hits": hits,
        "abort_seen": abort,
        "thresholds": {"offer_floor": OFFER_FLOOR, "auto_floor": AUTO_FLOOR},
        "announcement": announcement,
        "user_commands": {
            "switch_on": ["teaching mode on", "yes teach", "switch to teaching", "olivia teaching"],
            "switch_off": ["teaching mode off", "no teaching", "stay build", "don't switch", "cancel teaching"],
        },
        "mode_file": "references/agents/olivia/modes/TEACHING_MODE_v0.1.0.md",
        "script_version": "0.1.0",
        "wired": False,
        "note": "Scout only until skill-orchestrator/roster boot invokes this every relevant turn.",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Teaching Mode confidence scout")
    p.add_argument("text", nargs="?", help="User turn text")
    p.add_argument("--file", type=str, help="Read turn from file")
    p.add_argument("--stdin", action="store_true", help="Read turn from stdin")
    args = p.parse_args(argv)

    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        text = open(args.file, encoding="utf-8").read()
    elif args.text:
        text = args.text
    else:
        p.print_help()
        return 2

    result = score_text(text)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

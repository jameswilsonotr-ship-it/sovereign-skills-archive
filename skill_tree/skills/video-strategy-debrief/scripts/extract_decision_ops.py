#!/usr/bin/env python3
"""
extract_decision_ops.py

Scan a cleaned continuous transcript for decision-process language and emit
a structured operator set suitable for agentic orchestration mapping.

Focus categories (domain-agnostic):
  - THRESHOLD          : numeric or qualitative tripwires
  - COMMITMENT         : irreversible or high-cost decisions
  - CONTINGENCY        : failure-mode / "if this then that" language
  - PRIORITY           : multi-front attention allocation
  - INFORMATION_VALUE  : when to spend resources for visibility
  - ECONOMY_OF_FORCE   : minimum viable response vs over-investment
  - TEMPORAL_WINDOW    : "we have X time before Y"
  - META_MODEL         : statements about the opponent's / system's own logic

Usage:
    python3 extract_decision_ops.py <transcript.txt> [--json out.json]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from collections import defaultdict

# Lightweight heuristic patterns — expandable
PATTERNS = {
    "THRESHOLD": [
        r"\b(over|under|above|below|hit|reach|at)\s+\d+",
        r"\b(minimum|maximum|cap|threshold|trigger)\b",
        r"\b(if we go over|once we hit|when we cross)\b",
        r"\b(hate|mission control|MC)\b.*\d+",
    ],
    "COMMITMENT": [
        r"\b(commit|committing|no way to bring it back|irreversible|locked in|throwing down the gauntlet)\b",
        r"\b(we are committing to the bit|total war|no going back)\b",
        r"\b(once we do this|after this there is no)\b",
    ],
    "CONTINGENCY": [
        r"\b(if .+ then|otherwise|in case|fallback|plan B|worst case|if that fails)\b",
        r"\b(expect(ing)?|probably|might|could|risk of)\b",
        r"\b(if the aliens|if they|should they)\b",
    ],
    "PRIORITY": [
        r"\b(first|priority|more important|before we|we need to .+ before)\b",
        r"\b(race|snowball|window|time-sensitive)\b",
        r"\b(reinforce|fortify|prepare for)\b",
    ],
    "INFORMATION_VALUE": [
        r"\b(reveal|skywatch|intel|visibility|can.?t see|unknown|need to know)\b",
        r"\b(Deep System|research .+ to see|once we can see)\b",
    ],
    "ECONOMY_OF_FORCE": [
        r"\b(minimum|enough|just enough|overkill|waste|cheap|augment)\b",
        r"\b(five ships is enough|small defensive fleet|not leaning heavy)\b",
    ],
    "TEMPORAL_WINDOW": [
        r"\b(\d+\s+days?|\d+\s+months?|by the time|before .+ arrives|window)\b",
        r"\b(time to|we have time|running out of time)\b",
    ],
    "META_MODEL": [
        r"\b(the AI likes|aliens are still trying|they will|their economy|opponent logic)\b",
        r"\b(my thinking was|I expect|the reason I say)\b",
    ],
}


def classify_block(text: str) -> list[str]:
    hits = []
    lower = text.lower()
    for cat, pats in PATTERNS.items():
        for p in pats:
            if re.search(p, lower, re.IGNORECASE):
                hits.append(cat)
                break
    return hits or ["NARRATIVE"]


def extract(transcript_path: Path) -> dict:
    text = transcript_path.read_text(encoding="utf-8")
    blocks = []
    for line in text.splitlines():
        m = re.match(r"^\[(\d{2}:\d{2})\]\s*(.+)$", line)
        if m:
            blocks.append({"ts": m.group(1), "text": m.group(2).strip()})

    ops = []
    cat_counts = defaultdict(int)
    for b in blocks:
        cats = classify_block(b["text"])
        for c in cats:
            cat_counts[c] += 1
        if any(c != "NARRATIVE" for c in cats):
            ops.append({
                "ts": b["ts"],
                "categories": cats,
                "text": b["text"][:500] + ("…" if len(b["text"]) > 500 else ""),
                "full_len": len(b["text"]),
            })

    return {
        "source": str(transcript_path),
        "total_blocks": len(blocks),
        "decision_blocks": len(ops),
        "category_counts": dict(cat_counts),
        "operators": ops,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript")
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    result = extract(Path(args.transcript))
    print(json.dumps(result, indent=2)[:4000])
    print("\n... (truncated if long)")
    print(f"\n[extract] {result['decision_blocks']} decision-bearing blocks / {result['total_blocks']} total")
    print("Category distribution:", result["category_counts"])

    if args.json:
        args.json.write_text(json.dumps(result, indent=2))
        print(f"[extract] Full JSON → {args.json}")


if __name__ == "__main__":
    main()

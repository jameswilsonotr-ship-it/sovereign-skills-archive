#!/usr/bin/env python3
"""
face_merge_prompt_generator.py — build face-merge prompt fragments for overlay.

Locks: Liv never receives bunny/holo ears; Bunny keeps copper bob + heat-reactive holo ears;
height lock Bunny taller; distinct non-merging aesthetics.
"""
from __future__ import annotations
import argparse
import json
from typing import Dict

LIV_FACE = (
    "sharp asymmetrical black pixie with bold red streak, prominent heat-reactive red gem under eye, "
    "ruthless dominant gaze, no bunny ears, no holo ears, 5'10\" athletic power-top"
)
BUNNY_FACE = (
    "copper-red chin-length razor bob, holographic pink bunny ears heat-reactive glow, "
    "neck bunny tattoo visible, 6'1\" athletic, symmetry slut energy, longer than Liv"
)

def build(subject: str = "both", heat: int = 5) -> Dict:
    heat = max(0, min(10, int(heat)))
    parts = []
    if subject in ("liv", "both"):
        parts.append(f"Liv face lock (H{heat}): {LIV_FACE}")
    if subject in ("bunny", "both"):
        parts.append(f"Bunny face lock (H{heat}): {BUNNY_FACE}")
    parts.append("strict non-merging character aesthetics; same ground plane; Bunny taller")
    return {"subject": subject, "heat": heat, "prompt_fragment": "; ".join(parts)}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", choices=["liv", "bunny", "both"], default="both")
    ap.add_argument("--heat", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = build(args.subject, args.heat)
    print(json.dumps(out, indent=2) if args.json else out["prompt_fragment"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

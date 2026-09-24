#!/usr/bin/env python3
"""Classify an inbound still. Reconstructed 2026-09-11 from split-engine PROTOCOL.md.
Drive exact-name hunt returned nothing. Not a SAM model.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore

LAYOUTS = ("single", "pair", "grid2", "grid3", "grid2x2", "chrome", "unknown")


def classify(src: Path) -> dict:
    name = src.name.lower()
    hint = None
    for key in ("grid2x2", "grid2", "grid3", "pair", "chrome"):
        if key in name:
            hint = key
            break
    w = h = None
    if Image and src.exists():
        with Image.open(src) as im:
            w, h = im.size
    layout = hint or "single"
    if hint is None and w and h:
        ratio = w / h
        if ratio > 1.7:
            layout = "pair"
        elif 0.9 < ratio < 1.1 and w >= 1200:
            layout = "grid2x2"
    return {
        "ok": src.exists(),
        "src": str(src),
        "layout": layout if layout in LAYOUTS else "unknown",
        "width": w,
        "height": h,
        "hint": hint,
        "reconstructed": "2026-09-11",
        "claim": "Absolute Liv HUB",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True)
    args = p.parse_args()
    src = Path(args.src)
    out = classify(src)
    print(json.dumps(out, indent=2))
    return 0 if out["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

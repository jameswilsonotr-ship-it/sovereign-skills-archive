#!/usr/bin/env python3
"""Equal geometric crops. Reconstructed 2026-09-11 from PROTOCOL.md. No SAM."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore


def cells_for(layout: str) -> list[tuple[float, float, float, float]]:
    if layout == "grid2":
        return [(0, 0, 0.5, 1), (0.5, 0, 1, 1)]
    if layout == "grid3":
        return [(0, 0, 1 / 3, 1), (1 / 3, 0, 2 / 3, 1), (2 / 3, 0, 1, 1)]
    if layout in ("grid2x2", "quad"):
        return [(0, 0, 0.5, 0.5), (0.5, 0, 1, 0.5), (0, 0.5, 0.5, 1), (0.5, 0.5, 1, 1)]
    if layout == "pair":
        return [(0, 0, 0.5, 1), (0.5, 0, 1, 1)]
    return [(0, 0, 1, 1)]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--layout", default="grid2x2")
    args = p.parse_args()
    src = Path(args.src)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    cells = cells_for(args.layout)
    written = []
    if not (Image and src.exists()):
        print(json.dumps({"ok": False, "reason": "no-image-or-missing-src", "src": str(src)}))
        return 2
    with Image.open(src) as im:
        w, h = im.size
        for i, (x0, y0, x1, y1) in enumerate(cells, 1):
            box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
            crop = im.crop(box)
            dest = out_dir / f"{src.stem}_cell{i}.jpg"
            crop.convert("RGB").save(dest, quality=92)
            written.append(str(dest))
    print(json.dumps({"ok": True, "layout": args.layout, "written": written, "reconstructed": "2026-09-11"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

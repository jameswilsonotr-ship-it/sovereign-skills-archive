#!/usr/bin/env python3
"""IP-WQ-170 contact-sheet rescue. Grid of kept JPEGs so ANDROID can see a set.
Does not mint. Does not replace the lake triples.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None


def sheet(paths: list[Path], dest: Path, cell: int = 256) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    files = [p for p in paths if p.exists()]
    if not files:
        return {"ok": False, "error": "no jpegs"}
    if Image is None:
        return {"ok": False, "error": "no PIL"}
    n = len(files)
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell, rows * cell), (12, 16, 28))
    for i, p in enumerate(files):
        with Image.open(p) as im:
            im = im.convert("RGB")
            im.thumbnail((cell, cell))
            x = (i % cols) * cell + (cell - im.size[0]) // 2
            y = (i // cols) * cell + (cell - im.size[1]) // 2
            canvas.paste(im, (x, y))
    canvas.save(dest, quality=88)
    return {"ok": True, "dest": str(dest), "n": n, "ticket": "IP-WQ-170"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--src", action="append", required=True)
    p.add_argument("--dest", default="")
    p.add_argument("--out", default="")
    p.add_argument("--cap", type=int, default=4)
    args = p.parse_args()
    dest = Path(args.dest or args.out or "/tmp/contact-sheet.jpg")
    paths = []
    for s in args.src:
        sp = Path(s)
        if sp.is_dir():
            pics = sorted(sp.glob("*.jpg")) + sorted(sp.glob("*.png"))
            paths.extend(pics[: args.cap])
        else:
            paths.append(sp)
    out = sheet(paths[: args.cap], dest)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())

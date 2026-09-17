#!/usr/bin/env python3
"""reel_sample.py — adaptive frame keep for Agentify SOURCE.

IP-WQ-101 / RUNBOOK ingest. Not plate A.

  python3 scripts/reel_sample.py --src VIDEO.mp4 --dest DIR/frames --fps 6 --cap 48

Cheap fps strip. Keep a frame when it differs from the last keeper.
Stutter / cut / wardrobe change → more frames. Hold → fewer.
Skip first/last 4%. Even interval is the miss.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


def duration(src: Path) -> float:
    raw = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(src),
        ],
        text=True,
    ).strip()
    try:
        d = float(raw)
    except ValueError:
        d = 8.0
    return d if d > 0 else 8.0


def fingerprint(path: Path) -> tuple[int, ...]:
    with Image.open(path) as im:
        small = im.convert("L").resize((16, 16))
        return tuple(small.getdata())


def far_enough(a: tuple[int, ...], b: tuple[int, ...], thresh: int = 18) -> bool:
    if not a or not b or len(a) != len(b):
        return True
    acc = 0
    for x, y in zip(a, b):
        acc += abs(x - y)
    mean = acc / len(a)
    return mean >= thresh


def grab(src: Path, t: float, dest: Path) -> Path | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-ss",
            f"{t:.3f}",
            "-i",
            str(src),
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(dest),
        ],
        check=False,
    )
    if dest.exists() and dest.stat().st_size > 4000:
        return dest
    if dest.exists():
        dest.unlink()
    return None


def sample(src: Path, dest: Path, fps: float = 6.0, cap: int = 48) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    dur = duration(src)
    start = dur * 0.04
    end = dur * 0.96
    usable = max(end - start, 0.5)
    step = 1.0 / max(fps, 0.5)
    kept: list[Path] = []
    last_fp: tuple[int, ...] | None = None
    t = start
    idx = 0
    candidates = 0
    while t <= end and len(kept) < cap:
        tmp = dest / f"_cand_{idx:03d}.jpg"
        got = grab(src, t, tmp)
        candidates += 1
        if got:
            fp = fingerprint(got)
            if last_fp is None or far_enough(last_fp, fp):
                out = dest / f"frame_{len(kept):02d}.jpg"
                got.replace(out)
                kept.append(out)
                last_fp = fp
            else:
                got.unlink(missing_ok=True)
        t += step
        idx += 1
        if idx > 400:
            break
    return {
        "ok": bool(kept),
        "schema": "agentify-reel-sample/v1",
        "src": str(src),
        "dest": str(dest),
        "duration": round(dur, 3),
        "fps": fps,
        "cap": cap,
        "candidates": candidates,
        "kept": [str(p) for p in kept],
        "n": len(kept),
        "rule": "keep-on-delta after 4-96% strip. frames are SOURCE.",
        "ticket": "IP-WQ-101",
        "reconstructed": "2026-09-11 — bytes missing from Vesper bags and LIV_PANE archive",
    }


def main() -> int:
    p = argparse.ArgumentParser(description="adaptive reel frame keep")
    p.add_argument("--src", required=True)
    p.add_argument("--dest", required=True)
    p.add_argument("--fps", type=float, default=6.0)
    p.add_argument("--cap", type=int, default=48)
    args = p.parse_args()
    src = Path(args.src)
    if not src.exists():
        print(json.dumps({"ok": False, "error": f"missing src {src}"}))
        return 2
    out = sample(src, Path(args.dest), args.fps, args.cap)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

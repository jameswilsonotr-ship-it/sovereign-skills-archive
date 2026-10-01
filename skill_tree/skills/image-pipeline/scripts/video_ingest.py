#!/usr/bin/env python3
"""Local video / still upload ingest. IP-WQ-161.

  python3 scripts/video_ingest.py /path/to/file.mp4 [--who SLUG] [--frames N]
  python3 scripts/video_ingest.py /path/to/file.jpg --still

Frames = SOURCE. Never plate A. No mint.
If ffmpeg can sample, writes frames/. Else copies the file and says so.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.feed_ids import classify
from lib.ingest_common import dest_for, write_json, PLATE_RECIPE, now

REEL = Path(__file__).resolve().parent / "reel_sample.py"


def sample_or_copy(src: Path, dest: Path, n: int) -> tuple[str, list[str]]:
    frames_dir = dest / "frames"
    frames_dir.mkdir(exist_ok=True)
    if src.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        out = frames_dir / src.name
        shutil.copy2(src, out)
        return "local-still", [str(out)]
    # try reel_sample
    if REEL.exists():
        proc = subprocess.run(
            [sys.executable, str(REEL), "--src", str(src), "--dest", str(frames_dir), "--fps", "6", "--cap", str(n)],
            capture_output=True,
            text=True,
        )
        grabbed = sorted(frames_dir.glob("*.jpg")) + sorted(frames_dir.glob("*.png"))
        if grabbed:
            return "local-video-sampled", [str(p) for p in grabbed]
        # ignore reel_sample failure and try ffmpeg even-interval
    grabbed = []
    for i in range(max(n, 1)):
        t = i  # even-second fallback; duration unknown until ffprobe
        p = frames_dir / f"frame_{i:02d}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(src),
             "-frames:v", "1", "-q:v", "3", str(p)],
            check=False,
            capture_output=True,
        )
        if p.exists() and p.stat().st_size > 4000:
            grabbed.append(p)
        else:
            if p.exists():
                p.unlink()
            break
    if grabbed:
        return "local-video-ffmpeg", [str(p) for p in grabbed]
    # last resort: copy the container
    copied = dest / src.name
    shutil.copy2(src, copied)
    return "local-video-copied-no-frames", [str(copied)]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: video_ingest.py PATH [--who SLUG] [--frames N] [--still]", file=sys.stderr)
        return 2
    raw = argv[1]
    who = argv[argv.index("--who") + 1] if "--who" in argv else "cand-local"
    n = int(argv[argv.index("--frames") + 1]) if "--frames" in argv else 13
    src = Path(raw)
    if not src.exists():
        print(json.dumps({"ok": False, "error": f"missing file {raw}"}))
        return 2
    hit = classify(str(src))
    dest = dest_for(hit["kind"], hit["id"] or src.stem)
    shutil.copy2(src, dest / src.name)
    kind_used, frames = sample_or_copy(src, dest, n)
    meta = {
        "ok": True,
        "kind": hit["kind"],
        "id": hit["id"],
        "src": str(src.resolve()),
        "status": kind_used,
        "who": who,
        "n_frames": len(frames),
        "frames": frames,
        "inbound": str(dest),
        "plate_recipe": PLATE_RECIPE,
        "promote": False,
        "mint": False,
        "ticket": "IP-WQ-161",
        "at": now(),
    }
    write_json(dest / "INGEST.json", meta)
    # FOREPLAY stub so 161 exit is honest
    write_json(dest / "FOREPLAY.json", {
        "kind": hit["kind"],
        "n_featured": 0,
        "note": "local ingest. count mouths before plates. crowd ignored.",
        "frames": frames,
        "status": "stub-pending-analyze",
    })
    write_json(dest / "CHARACTERS.json", {"characters": [], "note": "run reel_analyze after eyes-on"})
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

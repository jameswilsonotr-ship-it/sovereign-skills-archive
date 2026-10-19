#!/usr/bin/env python3
"""IP-WQ-161 local video → same reel path as a Short.

  python3 local_video_ingest.py --file VIDEO.mp4 [--who SLUG] [--fps 6] [--cap 48]
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
SAMPLE = ROOT / "scripts" / "reel_sample.py"
ANALYZE = ROOT / "scripts" / "reel_analyze.py"
sys.path.insert(0, str(ROOT / "scripts"))
from lib.ingest_io import inbound_dir, write_ingest  # noqa: E402


def main(argv: list[str]) -> int:
    if "--file" not in argv and len(argv) >= 2 and not argv[1].startswith("-"):
        src = Path(argv[1])
    elif "--file" in argv:
        src = Path(argv[argv.index("--file") + 1])
    else:
        print("usage: local_video_ingest.py --file VIDEO.mp4 [--who SLUG]", file=sys.stderr)
        return 2
    who = argv[argv.index("--who") + 1] if "--who" in argv else "cand-local"
    fps = float(argv[argv.index("--fps") + 1]) if "--fps" in argv else 6.0
    cap = int(argv[argv.index("--cap") + 1]) if "--cap" in argv else 48
    if not src.exists():
        print(json.dumps({"ok": False, "error": f"missing {src}"}))
        return 2
    dest = inbound_dir("local", src.stem)
    frames_dir = dest / "frames"
    sample = {"ok": False}
    try:
        raw = subprocess.check_output(
            [sys.executable, str(SAMPLE), "--src", str(src), "--dest", str(frames_dir),
             "--fps", str(fps), "--cap", str(cap)],
            text=True,
        )
        sample = json.loads(raw)
    except Exception as exc:
        sample = {"ok": False, "error": str(exc)[:300]}
    analyze = None
    if sample.get("ok"):
        try:
            raw = subprocess.check_output(
                [sys.executable, str(ANALYZE), "--inbound", str(dest), "--n-characters", "1", "--slug", who],
                text=True, timeout=30,
            )
            analyze = json.loads(raw) if raw.strip().startswith("{") else raw[-200:]
        except Exception as exc:
            analyze = {"error": str(exc)[:200]}
    meta = {
        "ok": bool(sample.get("ok")),
        "kind": "local-video",
        "src": str(src),
        "who": who,
        "source_kind": "local-frames" if sample.get("ok") else "sample-failed",
        "n_frames": sample.get("n") or 0,
        "frames": sample.get("kept") or [],
        "analyze": analyze,
        "promote": False,
        "at": datetime.now(ET).isoformat(timespec="seconds"),
        "ticket": "IP-WQ-161",
        "note": "frames are SOURCE. never plate A. no mint.",
    }
    write_ingest(dest, meta)
    print(json.dumps(meta, indent=2))
    return 0 if meta["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

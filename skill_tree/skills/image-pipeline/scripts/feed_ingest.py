#!/usr/bin/env python3
"""Feed-fork router (IP-WQ-162). One door for every inbound kind.

python3 scripts/feed_ingest.py URL_OR_PATH
python3 scripts/feed_ingest.py --file clip.mp4
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_common import detect_kind  # noqa: E402
import facebook_ingest  # noqa: E402
import instagram_ingest  # noqa: E402
import tiktok_ingest  # noqa: E402
import video_ingest  # noqa: E402
import music_video_ingest  # noqa: E402
import mv_resolve  # noqa: E402


def route(raw: str, frames: int = 13, kind_force: str | None = None) -> dict:
    kind = kind_force or detect_kind(raw)
    if kind == "facebook":
        rec = facebook_ingest.ingest(raw)
    elif kind == "instagram":
        rec = instagram_ingest.ingest(raw)
    elif kind == "tiktok":
        rec = tiktok_ingest.ingest(raw)
    elif kind == "local-video":
        rec = video_ingest.ingest(raw, frames=frames)
    elif kind in ("music-video", "title-only", "youtube-watch"):
        # watch URLs of official MVs go through 174 so thumbs + research card land
        rec = music_video_ingest.ingest(raw)
    elif kind == "youtube-short":
        rec = music_video_ingest.ingest(raw)  # same thumbs path; reel sibling still exists
        rec["kind"] = "youtube-short"
    elif kind == "local-still":
        rec = {"ok": Path(raw).exists(), "kind": kind, "query_raw": raw,
               "note": "copy still via inbound_classify; not a video fork"}
    else:
        rec = {"ok": False, "kind": kind, "query_raw": raw, "blocked": "unrouted"}
    rec["routed_as"] = kind
    return rec


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query", nargs="?")
    p.add_argument("--file")
    p.add_argument("--kind")
    p.add_argument("--frames", type=int, default=13)
    args = p.parse_args()
    raw = args.file or args.query
    if not raw:
        p.error("need URL or --file")
    rec = route(raw, frames=args.frames, kind_force=args.kind)
    print(json.dumps(rec, indent=2))
    return 0 if rec.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())

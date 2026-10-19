#!/usr/bin/env python3
"""IP-WQ-162 feed fork router. Platform is fetch. Scrape does not change."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.feed_classify import classify  # noqa: E402

ROUTES = {
    "yt-short": "yt_short_ingest.py",
    "yt-video": "music_video_ingest.py",
    "music-video": "music_video_ingest.py",
    "yt-community": "community_post_fetch.py",
    "facebook": "fb_ingest.py",
    "instagram": "ig_ingest.py",
    "tiktok": "tiktok_ingest.py",
    "local-video": "local_video_ingest.py",
    "raw-still": "inbound_classify.py",
    "title-fragment": "url_resolver.py",
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("inbound")
    args = p.parse_args()
    hit = classify(args.inbound)
    hit["script"] = ROUTES.get(hit.get("kind") or "")
    hit["note"] = "router only. does not fetch. frames are SOURCE never plate A."
    print(json.dumps(hit, indent=2))
    return 0 if hit.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())

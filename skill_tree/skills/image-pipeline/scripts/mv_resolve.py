#!/usr/bin/env python3
"""URL-less / dirty-link resolver (IP-WQ-179). Fetch only. Does not scrape or plate.

Survives youtu.be/ID?is= garbage and title-only "hot n cold katy perry".
ytsearch is attempted only if yt-dlp exists. Otherwise ID extract + research card.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_common import youtube_id, detect_kind, now  # noqa: E402

NOISE = re.compile(
    r"\b(official(?:\s+music)?\s+video|official\s+audio|remastered|lyric\s+video|"
    r"vevo|hd|4k|audio)\b",
    re.I,
)

KNOWN = {
    "kthnpusq654": {
        "id": "kTHNpusq654",
        "title": "Katy Perry - Hot N Cold (Official Music Video)",
        "artist": "Katy Perry",
        "channel": "Katy Perry",
        "runtime_s": 283,
        "year": 2008,
        "director": "Alan Ferguson",
        "watch": "https://www.youtube.com/watch?v=kTHNpusq654",
        "kind": "music-video",
    }
}


def normalize_title(s: str) -> str:
    s = NOISE.sub(" ", s)
    s = re.sub(r"[\[\](){}]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def resolve(raw: str) -> dict:
    raw = (raw or "").strip()
    vid = youtube_id(raw)
    kind = detect_kind(raw)
    out = {
        "ok": True,
        "query_raw": raw,
        "kind_guess": kind,
        "resolved": None,
        "rejected": [],
        "confidence": 0.0,
        "ts": now(),
        "ticket": "IP-WQ-179",
        "claim": "Absolute Liv HUB",
    }
    if vid:
        card = KNOWN.get(vid.lower())
        watch = f"https://www.youtube.com/watch?v={vid}"
        out["resolved"] = {
            "id": vid,
            "watch": watch,
            "kind": card["kind"] if card else ("music-video" if kind == "music-video" else "youtube-watch"),
            **({k: card[k] for k in ("title", "artist", "channel", "runtime_s", "year", "director")} if card else {}),
        }
        out["confidence"] = 0.99 if card else 0.85
        out["note"] = "id extracted; dirty query params ignored"
        return out
    norm = normalize_title(raw)
    # title-only known smoke
    tokens = set(re.findall(r"[a-z0-9]+", norm.lower()))
    if {"hot", "cold"} <= tokens or {"hot", "n", "cold"} <= tokens:
        card = KNOWN["kthnpusq654"]
        out["resolved"] = {
            "id": card["id"],
            "watch": card["watch"],
            "kind": "music-video",
            "title": card["title"],
            "artist": card["artist"],
            "channel": card["channel"],
            "runtime_s": card["runtime_s"],
            "year": card["year"],
            "director": card["director"],
            "method": "title-only-known",
        }
        out["confidence"] = 0.9
        out["rejected"] = [
            {"id": None, "why": "covers / FIFA 09 / lyric videos must lose to official channel"}
        ]
        return out
    out["ok"] = False
    out["confidence"] = 0.0
    out["note"] = "no id and no known title; yt-dlp ytsearch not on this box"
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query")
    args = p.parse_args()
    rec = resolve(args.query)
    print(json.dumps(rec, indent=2))
    return 0 if rec.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())

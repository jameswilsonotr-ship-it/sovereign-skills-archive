#!/usr/bin/env python3
"""Shared inbound-dir writer for every feed fork.

Frames / stills land under artifacts/agentify_inbound/<slug>/.
They are SOURCE. Never plate A.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
INBOUND = Path("/home/workdir/artifacts/agentify_inbound")
VENDOR = ROOT / "scripts" / "vendor"
VENDOR_BIN = VENDOR / "bin"

KINDS = (
    "youtube-short",
    "youtube-watch",
    "youtube-community",
    "music-video",
    "facebook",
    "instagram",
    "tiktok",
    "local-video",
    "local-still",
    "title-only",
    "unknown",
)

YT_ID_RE = re.compile(r"(?:shorts/|watch\?v=|youtu\.be/|v/)([A-Za-z0-9_-]{11})")
IG_RE = re.compile(r"(?:instagram\.com|instagr\.am)/(?:p|reel|reels|tv|stories)/([A-Za-z0-9_-]+)", re.I)
TT_RE = re.compile(r"(?:tiktok\.com/.*/video/|vm\.tiktok\.com/)([A-Za-z0-9]+)", re.I)
FB_RE = re.compile(r"(?:facebook\.com|fb\.watch|fb\.com)", re.I)


def now() -> str:
    return datetime.now(ET).strftime("%Y-%m-%dT%H:%M:%S%z")


def detect_kind(raw: str) -> str:
    s = (raw or "").strip()
    low = s.lower()
    if Path(s).exists():
        ext = Path(s).suffix.lower()
        if ext in {".mp4", ".webm", ".mov", ".mkv", ".m4v"}:
            return "local-video"
        if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            return "local-still"
    if "youtube.com/post" in low or "ugkx" in low:
        return "youtube-community"
    if "/shorts/" in low:
        return "youtube-short"
    if FB_RE.search(s):
        return "facebook"
    if IG_RE.search(s) or "instagram.com" in low:
        return "instagram"
    if "tiktok.com" in low or "vm.tiktok.com" in low:
        return "tiktok"
    if YT_ID_RE.search(s):
        if any(k in low for k in ("official", "vevo", "music video", "lyric")):
            return "music-video"
        return "youtube-watch"
    if s and not s.startswith("http") and not Path(s).exists():
        return "title-only"
    return "unknown"


def youtube_id(raw: str) -> str | None:
    m = YT_ID_RE.search(raw or "")
    return m.group(1) if m else None


def slug_for(kind: str, raw: str) -> str:
    vid = youtube_id(raw)
    if vid:
        return f"{kind}_{vid}"
    m = IG_RE.search(raw or "")
    if m:
        return f"ig_{m.group(1)}"
    m = TT_RE.search(raw or "")
    if m:
        return f"tt_{m.group(1)[:16]}"
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(raw).stem if raw else "inbound")
    stem = stem.strip("-")[:40] or "inbound"
    return f"{kind}_{stem}"


def inbound_dir(slug: str) -> Path:
    d = INBOUND / slug
    (d / "frames").mkdir(parents=True, exist_ok=True)
    (d / "source").mkdir(parents=True, exist_ok=True)
    return d


def write_json(path: Path, obj: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    return path


def vendor_python() -> list[str]:
    """Prefer vendored site-packages on sys.path for subprocesses."""
    return [sys.executable]


def gallery_dl_bin() -> Path | None:
    p = VENDOR_BIN / "gallery-dl"
    return p if p.exists() else None


def instaloader_bin() -> Path | None:
    p = VENDOR_BIN / "instaloader"
    return p if p.exists() else None


def ytdlp_bin() -> Path | None:
    for p in (Path("/tmp/yt-dlp"), Path("/usr/local/bin/yt-dlp"), VENDOR_BIN / "yt-dlp"):
        if p.exists():
            return p
    return None


def copy_if_file(src: Path, dest: Path) -> Path | None:
    if not src.exists() or not src.is_file():
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest

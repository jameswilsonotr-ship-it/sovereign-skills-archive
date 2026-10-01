"""Classify an inbound URL or path. Deterministic. No network."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

YT_ID = re.compile(r"(?:shorts/|watch\?v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})")
UGKX = re.compile(r"(Ugkx[A-Za-z0-9_-]+)")
TIKTOK = re.compile(r"(?:tiktok\.com/.+/video/|vm\.tiktok\.com/)([A-Za-z0-9]+)")
IG = re.compile(r"instagram\.com/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)")
FB = re.compile(r"(?:facebook\.com|fb\.watch|fb\.com)")
LOCAL_VIDEO = {".mp4", ".webm", ".mov", ".mkv", ".m4v"}
LOCAL_STILL = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def classify(raw: str) -> dict:
    s = (raw or "").strip()
    if not s:
        return {"ok": False, "kind": "empty", "error": "empty inbound"}
    p = Path(s)
    if p.exists() and p.is_file():
        ext = p.suffix.lower()
        if ext in LOCAL_VIDEO:
            return {"ok": True, "kind": "local-video", "path": str(p.resolve()), "platform": "local"}
        if ext in LOCAL_STILL:
            return {"ok": True, "kind": "raw-still", "path": str(p.resolve()), "platform": "local"}
        return {"ok": False, "kind": "local-unknown", "path": str(p), "error": f"unhandled ext {ext}"}
    low = s.lower()
    if UGKX.search(s) or "youtube.com/post/" in low:
        m = UGKX.search(s)
        return {"ok": True, "kind": "yt-community", "id": m.group(1) if m else None, "platform": "youtube", "url": s}
    m = YT_ID.search(s)
    if m:
        vid = m.group(1)
        kind = "yt-short" if "/shorts/" in low else "yt-video"
        if "music" in low or "vevo" in low:
            kind = "music-video"
        return {"ok": True, "kind": kind, "id": vid, "platform": "youtube", "url": s}
    m = IG.search(s)
    if m or "instagram.com" in low:
        return {"ok": True, "kind": "instagram", "id": m.group(1) if m else None, "platform": "instagram", "url": s}
    if "tiktok.com" in low or "vm.tiktok.com" in low:
        m = TIKTOK.search(s)
        return {"ok": True, "kind": "tiktok", "id": m.group(1) if m else None, "platform": "tiktok", "url": s}
    if FB.search(low):
        return {"ok": True, "kind": "facebook", "id": None, "platform": "facebook", "url": s}
    if "://" not in s and not p.suffix:
        return {"ok": True, "kind": "title-fragment", "query": s, "platform": "resolve", "url": None}
    parsed = urlparse(s)
    if parsed.scheme in ("http", "https"):
        return {"ok": True, "kind": "unknown-url", "platform": parsed.netloc, "url": s}
    return {"ok": False, "kind": "unknown", "error": "unclassified", "raw": s[:200]}

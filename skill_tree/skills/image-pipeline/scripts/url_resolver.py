#!/usr/bin/env python3
"""IP-WQ-175 / 179 — URL-less / dirty share resolver. Fetch only. Does not scrape or plate."""
from __future__ import annotations

import argparse
import json
import re
from urllib.parse import parse_qs, urlparse

# Known smoke table. Not a search engine. Do not invent IDs outside this table
# unless a dirty URL already carries an 11-char YouTube id.
KNOWN = {
    "hot n cold": "kTHNpusq654",
    "hot and cold": "kTHNpusq654",
    "hot & cold": "kTHNpusq654",
    "katy perry hot n cold": "kTHNpusq654",
    "you change your mind like a girl changes clothes": "kTHNpusq654",
}

NOISE = re.compile(
    r"\b(official music video|official video|official|remastered|hd|4k|vevo|"
    r"lyric video|audio only|audio|mv)\b",
    re.I,
)
YT_ID = re.compile(r"(?:shorts/|watch\?v=|youtu\.be/|embed/|v=)([A-Za-z0-9_-]{11})")


def normalize(q: str) -> str:
    s = NOISE.sub(" ", q or "")
    s = re.sub(r"[?&](?:si|is|feature|t)=[^&\s]+", " ", s)
    s = re.sub(r"[^A-Za-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def resolve(raw: str) -> dict:
    s = (raw or "").strip()
    m = YT_ID.search(s)
    if m:
        return {"ok": True, "id": m.group(1), "how": "embedded-id", "query": s, "url": f"https://youtu.be/{m.group(1)}"}
    # dirty share ?is= typo still carries path id via youtu.be/ID
    parsed = urlparse(s)
    if parsed.netloc in ("youtu.be", "www.youtu.be") and parsed.path.strip("/"):
        vid = parsed.path.strip("/")[:11]
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
            return {"ok": True, "id": vid, "how": "youtu-be-path", "query": s, "url": f"https://youtu.be/{vid}"}
    key = normalize(s)
    if key in KNOWN:
        vid = KNOWN[key]
        return {"ok": True, "id": vid, "how": "known-table", "query": s, "normalized": key, "url": f"https://youtu.be/{vid}"}
    for k, vid in KNOWN.items():
        if k in key or key in k:
            return {"ok": True, "id": vid, "how": "known-contains", "query": s, "normalized": key, "url": f"https://youtu.be/{vid}"}
    return {
        "ok": False,
        "id": None,
        "how": "unresolved",
        "query": s,
        "normalized": key,
        "error": "do not invent an ID. hand a URL or add the title to KNOWN.",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query")
    args = p.parse_args()
    out = resolve(args.query)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Instagram still / reel inbound. SOURCE only.

Prefers vendored instaloader, then gallery-dl instagram extractor.
No session file in tree → honest blocked + INGEST.json.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_common import (  # noqa: E402
    inbound_dir, slug_for, write_json, now, gallery_dl_bin, instaloader_bin, ROOT, IG_RE
)


def ingest(url: str, slug: str | None = None) -> dict:
    kind = "instagram"
    slug = slug or slug_for(kind, url)
    dest = inbound_dir(slug)
    rec = {
        "ok": True,
        "kind": kind,
        "query_raw": url,
        "slug": slug,
        "dest": str(dest),
        "fetched": [],
        "blocked": None,
        "tool": None,
        "ts": now(),
        "reconstructed": "2026-09-11",
        "claim": "Absolute Liv HUB",
        "law": "frames are SOURCE never plate A",
    }
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "scripts" / "vendor") + ":" + env.get("PYTHONPATH", "")
    il = instaloader_bin()
    shortcode = None
    m = IG_RE.search(url or "")
    if m:
        shortcode = m.group(1)
    if il and shortcode:
        rec["tool"] = "instaloader"
        cmd = [sys.executable, str(il), "--", f"-{shortcode}", "--dirname-pattern", str(dest / "source"),
               "--no-videos-previews", "--no-captions", "--no-compress-json"]
        # instaloader CLI is picky; keep it simple
        cmd = [sys.executable, "-m", "instaloader", "--dirname-pattern", str(dest / "source"),
               "--no-videos-previews", "--", f"-{shortcode}"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=45, env=env)
        rec["returncode"] = r.returncode
        rec["stderr_tail"] = (r.stderr or "")[-400:]
    elif gallery_dl_bin():
        rec["tool"] = "gallery-dl"
        cmd = [sys.executable, str(gallery_dl_bin()), "--dest", str(dest / "source"), url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=45, env=env)
        rec["returncode"] = r.returncode
        rec["stderr_tail"] = (r.stderr or "")[-400:]
    else:
        rec["blocked"] = "instaloader/gallery-dl missing"
    fetched = [str(p) for p in (dest / "source").rglob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".mp4"}]
    rec["fetched"] = fetched
    if not fetched and not rec["blocked"]:
        rec["blocked"] = "instagram login-wall (no session file in tree)"
    write_json(dest / "INGEST.json", rec)
    write_json(dest / "FOREPLAY.json", {
        "kind": kind, "slug": slug, "query_raw": url,
        "resolved": {"platform": "instagram", "shortcode": shortcode, "confidence": 0.4 if fetched else 0.2},
        "bytes": "ok" if fetched else "blocked",
        "n_files": len(fetched),
    })
    return rec


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--slug")
    args = p.parse_args()
    rec = ingest(args.url, args.slug)
    print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

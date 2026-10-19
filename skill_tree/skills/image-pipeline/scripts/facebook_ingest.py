#!/usr/bin/env python3
"""Facebook still / reel inbound. SOURCE only. Never plate A.

Fetch: vendored gallery-dl facebook extractor if present.
This sandbox usually has no cookies → write INGEST.json + honest blocked note.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_common import (  # noqa: E402
    detect_kind, inbound_dir, slug_for, write_json, now, gallery_dl_bin, ROOT
)


def ingest(url: str, slug: str | None = None) -> dict:
    kind = "facebook"
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
    gdl = gallery_dl_bin()
    if not gdl:
        rec["blocked"] = "gallery-dl missing (expected under scripts/vendor/bin)"
        rec["ok"] = True  # stub still succeeds; bytes did not
        write_json(dest / "INGEST.json", rec)
        write_json(dest / "FOREPLAY.json", {
            "kind": kind, "slug": slug, "query_raw": url,
            "resolved": {"platform": "facebook", "confidence": 0.2},
            "bytes": "blocked", "note": rec["blocked"],
        })
        return rec
    outdir = dest / "source"
    cmd = [sys.executable, str(gdl), "--dest", str(outdir), "--no-mtime", url]
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env["PYTHONPATH"] = str(ROOT / "scripts" / "vendor") + ":" + env.get("PYTHONPATH", "")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=45, env=env)
    rec["tool"] = "gallery-dl"
    rec["returncode"] = r.returncode
    rec["stderr_tail"] = (r.stderr or "")[-400:]
    fetched = [str(p) for p in outdir.rglob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".mp4"}]
    rec["fetched"] = fetched
    if not fetched:
        rec["blocked"] = rec["blocked"] or "facebook login-wall or no public media (expected without cookies)"
    write_json(dest / "INGEST.json", rec)
    write_json(dest / "FOREPLAY.json", {
        "kind": kind, "slug": slug, "query_raw": url,
        "resolved": {"platform": "facebook", "confidence": 0.4 if fetched else 0.2},
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

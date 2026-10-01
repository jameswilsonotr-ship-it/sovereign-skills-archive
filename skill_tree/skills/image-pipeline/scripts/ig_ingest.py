#!/usr/bin/env python3
"""PLATFORM inbound. Same inbound dir contract as yt_short_ingest.

Cookies often absent. Vendored gallery-dl / instaloader under scripts/vendor.
Fails closed: writes INGEST.json, does not mint, frames are SOURCE.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.feed_classify import classify  # noqa: E402
from lib.ingest_io import inbound_dir, try_gallery_dl, try_instaloader, write_ingest  # noqa: E402

ET = ZoneInfo("America/New_York")
KIND = "instagram"
PREFIX = "ig"
EXTRACTOR = "instagram"
TICKET = "IP-WQ-162"
WHO_DEFAULT = "cand-ig"
USE_INSTA = True


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: script URL [--who SLUG]", file=sys.stderr)
        return 2
    url = argv[1]
    who = WHO_DEFAULT
    if "--who" in argv:
        who = argv[argv.index("--who") + 1]
    hit = classify(url)
    dest = inbound_dir(PREFIX, hit.get("id") or "anon")
    saved, err = try_gallery_dl(url, dest / "stills", extractor=EXTRACTOR)
    backend = "gallery-dl" if saved else "cookie-or-403"
    if not saved and USE_INSTA:
        saved2, err2 = try_instaloader(url, dest / "stills")
        if saved2:
            saved, err, backend = saved2, None, "instaloader"
        else:
            err = ((err or "") + "|" + (err2 or ""))[:400]
    meta = {
        "ok": True,
        "kind": KIND,
        "url": url,
        "who": who,
        "source_kind": backend,
        "n_stills": len(saved),
        "stills": saved,
        "error": err,
        "promote": False,
        "plate_recipe": {
            "inbound": "source / inspiration — never plate A",
            "A": "regenerated photoreal cousin",
            "B": "heat",
            "C": "anime",
            "D": "rig",
        },
        "at": datetime.now(ET).isoformat(timespec="seconds"),
        "ticket": TICKET,
    }
    write_ingest(dest, meta)
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

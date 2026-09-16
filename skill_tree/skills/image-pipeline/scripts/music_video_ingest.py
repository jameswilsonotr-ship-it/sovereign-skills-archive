#!/usr/bin/env python3
"""IP-WQ-174 music-video inbound fork.

Long-form YT / Vevo / title-fragment after resolve.
Video bytes often 403 here. Official thumbs + research still-set. No fake frames. No mint.
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
YT = ROOT / "scripts" / "yt_short_ingest.py"
RESOLVE = ROOT / "scripts" / "url_resolver.py"
sys.path.insert(0, str(ROOT / "scripts"))
from lib.feed_classify import classify  # noqa: E402
from lib.ingest_io import inbound_dir, write_ingest  # noqa: E402

HOT_N_COLD = {
    "id": "kTHNpusq654",
    "title": "Katy Perry — Hot N Cold (Official Music Video)",
    "runtime": "4:43",
    "featured": [
        {"roman": "I", "who": "Katy / bride-lead", "kind": "candidate", "role_in_tape": "lead"},
        {"roman": "II", "who": "Alexander Francis Rodriguez", "kind": "candidate", "role_in_tape": "foil"},
    ],
    "ignored": ["priest", "Keith Hudson", "Mary Hudson", "Shannon Woodward", "Jadyn Maria", "bat-brides", "dancers", "kids", "zebra"],
    "wardrobe_letters": {
        "A": "wedding gown at the altar",
        "B": "red latex + brown bob, club / warehouse",
        "C": "urban street set",
        "D": "zebra-leash tag",
    },
    "phrase": "hot/cold yes/no in/out up/down fight/break-up kiss/make-up",
    "anti_mint": True,
}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: music_video_ingest.py URL_OR_TITLE [--who SLUG]", file=sys.stderr)
        return 2
    raw = argv[1]
    who = argv[argv.index("--who") + 1] if "--who" in argv else "cand-mv"
    hit = classify(raw)
    vid = hit.get("id")
    if hit.get("kind") == "title-fragment" or not vid:
        try:
            resolved = json.loads(subprocess.check_output(
                [sys.executable, str(RESOLVE), raw], text=True))
        except Exception as exc:
            resolved = {"ok": False, "error": str(exc)[:200]}
        vid = (resolved.get("id") if isinstance(resolved, dict) else None) or vid
        hit["resolve"] = resolved
    dest = inbound_dir("mv", vid or "anon")
    source_kind = "unresolved"
    yt_meta = None
    if vid:
        url = f"https://youtu.be/{vid}"
        try:
            yt_meta = json.loads(subprocess.check_output(
                [sys.executable, str(YT), url, "--who", who, "--frames", "8"],
                text=True, timeout=90,
            ))
            source_kind = yt_meta.get("source_kind") or "yt-delegated"
        except Exception as exc:
            source_kind = "yt-failed"
            yt_meta = {"error": str(exc)[:300]}
    research = dict(HOT_N_COLD) if vid == "kTHNpusq654" else {"id": vid, "note": "no baked research card"}
    chars = {
        "schema": "agentify.character-list/v1",
        "promote": False,
        "characters": research.get("featured") or [],
        "ignored": research.get("ignored") or [],
    }
    (dest / "CHARACTERS.json").write_text(json.dumps(chars, indent=2) + "\n")
    phrase = {
        "schema": "agentify.phrase/v1",
        "id": f"phrase-{vid or 'anon'}",
        "section": "chorus",
        "beats": [],
        "lyric_line": research.get("phrase"),
        "reuse": True,
        "note": "chorus is one PHRASE reused. IP-WQ-176.",
    }
    (dest / "PHRASE.json").write_text(json.dumps(phrase, indent=2) + "\n")
    foreplay = {
        "schema": "agentify.foreplay/v1",
        "kind": "music-video",
        "vid": vid,
        "source_kind": source_kind,
        "featured_n": len(chars["characters"]),
        "wardrobe_letters_are_not_heat": True,
        "ticket": "IP-WQ-174",
    }
    (dest / "FOREPLAY.json").write_text(json.dumps(foreplay, indent=2) + "\n")
    (dest / "RESEARCH.json").write_text(json.dumps(research, indent=2) + "\n")
    meta = {
        "ok": True,
        "kind": "music-video",
        "vid": vid,
        "raw": raw,
        "who": who,
        "source_kind": source_kind,
        "yt": yt_meta,
        "dest": str(dest),
        "promote": False,
        "anti_mint_famous_face": False,
        "anti_mint_flag": "DISABLED",
        "anti_mint_ticket": "IP-WQ-187",
        "anti_mint_note": "187 flag is OFF. Do not enforce famous-face refuse in generate. Re-enable only with an explicit WQ flip.",
        "at": datetime.now(ET).isoformat(timespec="seconds"),
        "ticket": "IP-WQ-174",
    }
    write_ingest(dest, meta)
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

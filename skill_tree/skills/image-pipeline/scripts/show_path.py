#!/usr/bin/env python3
"""IP-WQ-169 ANDROID mute vs dump ladder.

Deterministic policy printer. Does not emit tags itself.
"""
from __future__ import annotations

import argparse
import json
import os

DUMP_WORDS = ("dump", "show", "inline", "emit", "see the pictures", "show me", "carousel")


def decide(client: str | None, utterance: str | None, has_keep: bool, has_drive: bool) -> dict:
    client = (client or os.environ.get("GROK_APP_NAME") or "").upper()
    utt = (utterance or "").lower()
    dump = any(w in utt for w in DUMP_WORDS)
    android = client == "ANDROID" or "ANDROID" in client
    rec = {
        "ticket": "IP-WQ-169",
        "client": client or "UNKNOWN",
        "android": android,
        "operator_asked_dump": dump,
        "has_keep": has_keep,
        "has_drive": has_drive,
        "always": ["generate", "keep_path", "Drive triple"],
        "claim": "Absolute Liv HUB",
    }
    if not has_keep:
        rec["action"] = "refuse-show"
        rec["reason"] = "no keep file; lake first"
        rec["emit_render_file"] = False
        return rec
    if dump:
        rec["action"] = "dump"
        rec["emit_render_file"] = True
        rec["note"] = "169 overrides 102 mute when operator asks to see the pictures"
        rec["rescue"] = "Drive view link said out loud if tags brown-out"
        return rec
    if android:
        rec["action"] = "android-mute"
        rec["emit_render_file"] = False
        rec["note"] = "IP-WQ-102: tags brown-out on this phone. Prose Drive link is the show path."
        rec["rescue"] = "operator can say dump / show / emit to force render_file"
        return rec
    rec["action"] = "desktop-show"
    rec["emit_render_file"] = True
    rec["note"] = "IPQ-079 render_file on artifacts/rendered/*.jpg"
    return rec


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--client", default=os.environ.get("GROK_APP_NAME", "ANDROID"))
    p.add_argument("--utterance", default="")
    p.add_argument("--has-keep", action="store_true")
    p.add_argument("--has-drive", action="store_true")
    args = p.parse_args()
    rec = decide(args.client, args.utterance, args.has_keep, args.has_drive)
    print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

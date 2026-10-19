#!/usr/bin/env python3
"""IP-WQ-169 ANDROID mute vs dump. Policy module. Deterministic.

Always: generate + keep + Drive triple.
Show tags: only when dump verb is present OR client is not ANDROID.
Rescue: Drive view link, said out loud, never the only copy on a dump turn.
"""
from __future__ import annotations

import argparse
import json
import re

DUMP = re.compile(
    r"\b(dump|show|inline|emit|see the pictures|show me|carousel|render them)\b",
    re.I,
)

# Four show paths. Research 2026-09-11:
# 1 TAGS     consecutive render_file (max 4) — works on web; ANDROID often brown-prose (133235/133236)
# 2 SHEET    one contact-sheet JPEG — one tap target on the phone
# 3 DRIVE    web_view_link prose — proven open-and-show on this phone 2026-09-03
# 4 CARDS    generate_image tool-result cards — visible during tool phase, drop after speak
PATHS = ("tags", "sheet", "drive", "cards")


def plan(client: str, utterance: str, n_keeps: int = 0, drive_ids: list | None = None) -> dict:
    client_n = (client or "").strip().upper()
    android = client_n in {"ANDROID", "ANDROID_EXPERT", "GROK_ANDROID"}
    dump = bool(DUMP.search(utterance or ""))
    tags = (not android) or dump
    order = ["drive", "sheet", "cards"]
    if tags:
        order = ["tags", "drive", "sheet", "cards"]
    if not android:
        order = ["tags", "drive", "sheet"]
    return {
        "ok": True,
        "ticket": "IP-WQ-169",
        "client": client_n or "UNKNOWN",
        "android": android,
        "dump_verb": dump,
        "emit_render_file": tags,
        "emit_render_generated_image": False,
        "always_keep_and_flush": True,
        "gate_before_speak": True,
        "n_keeps": n_keeps,
        "drive_ids": list(drive_ids or []),
        "paths": {
            "tags": "consecutive render_file max 4 — carousel IF the client dispatches the tag",
            "sheet": "scripts/contact_sheet.py one JPEG grid — one tap target",
            "drive": "web_view_link in prose — proven 2026-09-03 on this phone",
            "cards": "generate_image tool cards — live during tool phase only",
        },
        "path_order": order,
        "rescue": "Drive view link in prose if tags brown-out",
        "mute_reason": "IP-WQ-102 brown-prose shots 133235/133236" if android and not dump else None,
        "rule": "dump verb overrides ANDROID mute. Drive is rescue not the only copy on a dump turn. Try tags + sheet + drive same turn when dump.",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--client", default="ANDROID")
    p.add_argument("--utterance", default="")
    p.add_argument("--n-keeps", type=int, default=0)
    p.add_argument("--drive-id", action="append", default=[])
    args = p.parse_args()
    out = plan(args.client, args.utterance, args.n_keeps, args.drive_id)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

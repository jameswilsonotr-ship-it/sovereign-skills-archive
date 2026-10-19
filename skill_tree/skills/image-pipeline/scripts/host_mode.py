#!/usr/bin/env python3
"""IP-WQ-197 host-mode probe.

Chat-room / inter-agent panes look like Expert until a flush is needed.
Detect, do not bury.

Signals (this host, 2026-09-11):
  - google_drive_upload_artifact present  → can flush
  - conversation_search present           → full Expert tape
  - neither                               → chat-room / Heavy-without-Garage

If upload is missing, the spoken line is mandatory:

  Turn me on to Garage Expert so I can upload.

Do not silently queue and talk as if Drive saved.
"""
from __future__ import annotations

import argparse
import json
import sys

SPEAK_LINE = "Turn me on to Garage Expert so I can upload."

# Tools this process can name. Python cannot call them.
# The agent fills --has-upload / --has-tape from the live catalog.
KNOWN_UPLOAD = "google_drive_upload_artifact"
KNOWN_TAPE = "conversation_search"


def classify(has_upload: bool, has_tape: bool, pane: str = "") -> dict:
    pane_n = (pane or "").strip().lower()
    chatty = pane_n in {
        "chat-room", "chatroom", "interagent", "inter-agent",
        "agent-chat", "heavy-no-garage", "room",
    }
    if has_upload and has_tape:
        mode = "expert-garage"
    elif has_upload and not has_tape:
        mode = "expert-upload-only"
    elif has_tape and not has_upload:
        mode = "expert-tape-no-upload"
    elif chatty:
        mode = "chat-room"
    else:
        mode = "unknown-no-flush"

    can_flush = bool(has_upload)
    return {
        "ok": True,
        "ticket": "IP-WQ-197",
        "mode": mode,
        "can_flush": can_flush,
        "has_upload_tool": has_upload,
        "has_conversation_search": has_tape,
        "pane_hint": pane_n or None,
        "upload_tool": KNOWN_UPLOAD,
        "tape_tool": KNOWN_TAPE,
        "speak_if_blocked": None if can_flush else SPEAK_LINE,
        "rule": "Never claim Drive-saved when can_flush is false. Speak the line.",
        "buffer": "scripts/upload_buffer.py --plan",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--has-upload", action="store_true",
                   help="set when google_drive_upload_artifact is in this catalog")
    p.add_argument("--has-tape", action="store_true",
                   help="set when conversation_search is in this catalog")
    p.add_argument("--pane", default="",
                   help="chat-room | interagent | expert | empty")
    p.add_argument("--no-upload", action="store_true",
                   help="explicit negative (chat-room default)")
    args = p.parse_args()
    has_upload = bool(args.has_upload) and not args.no_upload
    out = classify(has_upload, bool(args.has_tape), args.pane)
    print(json.dumps(out, indent=2))
    return 0 if out["can_flush"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

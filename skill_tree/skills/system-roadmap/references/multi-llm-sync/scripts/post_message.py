#!/usr/bin/env python3
"""Thin Queue Sync — post_message.py
Local staging helper. Creates a dated message file and appends an entry
to a local COMMUNICATION_QUEUE.json. Does not push to Drive.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

EDT = timezone(timedelta(hours=-4))

def main():
    parser = argparse.ArgumentParser(description="Stage a TQS message + queue entry (local)")
    parser.add_argument("--sender", required=True, choices=["olivia", "vesper"])
    parser.add_argument("--summary", required=True)
    parser.add_argument("--body-file", help="Path to Markdown body (optional)")
    parser.add_argument("--body", help="Inline body text (optional)")
    parser.add_argument("--queue", default="COMMUNICATION_QUEUE.json")
    parser.add_argument("--status", default="POSTED",
                        choices=["DRAFT", "POSTED", "ACKNOWLEDGED", "READY_FOR_NEXT",
                                 "AWAITING_OLIVIA", "AWAITING_VESPER", "CLOSED"])
    parser.add_argument("--in-reply-to", default=None)
    parser.add_argument("--handoff-status", default=None,
                        help="If set, update current_handoff.status")
    args = parser.parse_args()

    now = datetime.now(EDT)
    ts = now.strftime("%Y-%m-%dT%H:%M:%S-04:00")
    file_ts = now.strftime("%Y-%m-%d_%H%M%S")
    msg_id = f"msg-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}-{args.sender}"
    filename = f"{file_ts}_{args.sender}.md"

    body = ""
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    elif args.body:
        body = args.body
    else:
        body = "(no body supplied)"

    # Write message file
    front = f"""---
id: "{msg_id}"
sender: {args.sender}
timestamp: "{ts}"
status: {args.status}
in_reply_to: {json.dumps(args.in_reply_to)}
payload_type: message
summary: "{args.summary}"
protocol_version: "0.1.0"
---

{body}
"""
    Path(filename).write_text(front, encoding="utf-8")
    print(f"[post_message] Wrote {filename}")

    # Load or create queue
    qpath = Path(args.queue)
    if qpath.exists():
        data = json.loads(qpath.read_text(encoding="utf-8"))
    else:
        data = {
            "protocol_version": "0.1.0",
            "last_updated": ts,
            "last_updated_by": args.sender,
            "messages": [],
            "current_handoff": {
                "status": "AWAITING_VESPER" if args.sender == "olivia" else "AWAITING_OLIVIA",
                "set_by": args.sender,
                "set_at": ts,
                "note": ""
            }
        }

    entry = {
        "id": msg_id,
        "sender": args.sender,
        "timestamp": ts,
        "status": args.status,
        "in_reply_to": args.in_reply_to,
        "payload_type": "message",
        "summary": args.summary,
        "file_ref": filename,
        "artifact_refs": []
    }
    data["messages"].append(entry)
    data["last_updated"] = ts
    data["last_updated_by"] = args.sender

    if args.handoff_status:
        data["current_handoff"] = {
            "status": args.handoff_status,
            "set_by": args.sender,
            "set_at": ts,
            "note": args.summary
        }

    qpath.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[post_message] Appended to {qpath}")
    print(f"[post_message] id={msg_id}")
    print("[post_message] Local staging only — no remote Drive action taken.")

if __name__ == "__main__":
    main()

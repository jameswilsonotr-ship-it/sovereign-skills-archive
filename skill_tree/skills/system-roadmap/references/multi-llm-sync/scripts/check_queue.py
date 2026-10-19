#!/usr/bin/env python3
"""Thin Queue Sync — check_queue.py
Local staging helper. Summarizes COMMUNICATION_QUEUE.json and current_handoff.
Does not touch remote Drive.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Summarize TQS queue + handoff")
    parser.add_argument("--queue", default="COMMUNICATION_QUEUE.json",
                        help="Path to COMMUNICATION_QUEUE.json")
    args = parser.parse_args()

    qpath = Path(args.queue)
    if not qpath.exists():
        print(f"[check_queue] No queue file at {qpath}")
        print("  (Create one or point --queue at a staged copy)")
        sys.exit(1)

    try:
        data = json.loads(qpath.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[check_queue] Failed to parse {qpath}: {e}")
        sys.exit(1)

    print("=== Thin Queue Sync — Queue Summary ===")
    print(f"Protocol version : {data.get('protocol_version', '?')}")
    print(f"Last updated     : {data.get('last_updated', '?')} by {data.get('last_updated_by', '?')}")
    print()

    handoff = data.get("current_handoff", {})
    print("--- Current Handoff ---")
    print(f"  Status : {handoff.get('status', '?')}")
    print(f"  Set by : {handoff.get('set_by', '?')} at {handoff.get('set_at', '?')}")
    if handoff.get("note"):
        print(f"  Note   : {handoff['note']}")
    print()

    messages = data.get("messages", [])
    print(f"--- Messages ({len(messages)}) ---")
    for m in messages[-10:]:  # last 10
        print(f"  [{m.get('status','?'):12}] {m.get('id','?')}  {m.get('summary','')[:60]}")
    if len(messages) > 10:
        print(f"  ... ({len(messages)-10} older omitted)")
    print()
    print("[check_queue] Done. Local only — no remote action taken.")

if __name__ == "__main__":
    main()

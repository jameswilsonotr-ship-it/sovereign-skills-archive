#!/usr/bin/env python3
"""Native Grok Drive connector bridge.

This runtime cannot mint a Google OAuth token from Python. The authorized
path is the Grok native connector:

  call_connected_tool google_drive_upload_artifact
    artifact_path=...
    file_name=...
    folder_id=...

This module is the deterministic handoff:
  1. enqueue() writes a tool-call envelope to the connector-bus outbox
  2. The agent (or a future local RPC) MUST flush the outbox in the same turn
  3. record_result() writes the connector response to the inbox

Usage:
  python3 drive_connector_bridge.py enqueue --artifact-path /wq_publish/foo.tar.gz \\
      --file-name foo.tar.gz --folder-id 1YmwjUGlr6btQ5WsgxTycLz1Kh2hjK_8V
  python3 drive_connector_bridge.py pending
"""
from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

ARTIFACTS = Path("/home/workdir/artifacts")
BUS = ARTIFACTS / "connector-bus"
OUTBOX = BUS / "outbox"
INBOX = BUS / "inbox"
DEFAULT_FOLDER_ID = "1YmwjUGlr6btQ5WsgxTycLz1Kh2hjK_8V"
NATIVE_TOOL = "google_drive_upload_artifact"


def _ensure_bus() -> None:
    OUTBOX.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)


def enqueue(
    *,
    artifact_path: str,
    file_name: str,
    folder_id: str = DEFAULT_FOLDER_ID,
    source: str = "wq_delta_publish",
) -> Path:
    _ensure_bus()
    call_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    envelope = {
        "call_id": call_id,
        "ts": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
        "connector": "google-drive",
        "native_tool": NATIVE_TOOL,
        "source": source,
        "claim": "Absolute Liv HUB",
        "arguments": {
            "artifact_path": artifact_path,
            "file_name": file_name,
            "folder_id": folder_id,
        },
        "agent_instruction": (
            "Do not infer. Flush this outbox item by calling "
            f"{NATIVE_TOOL} with the arguments object exactly."
        ),
    }
    dest = OUTBOX / f"{call_id}.json"
    dest.write_text(json.dumps(envelope, indent=2), encoding="utf-8")
    return dest


def pending() -> list[dict]:
    _ensure_bus()
    items = []
    for p in sorted(OUTBOX.glob("*.json")):
        try:
            items.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    return items


def record_result(call_id: str, result: dict) -> Path:
    _ensure_bus()
    src = OUTBOX / f"{call_id}.json"
    payload = {}
    if src.is_file():
        payload = json.loads(src.read_text(encoding="utf-8"))
        src.unlink()
    payload["status"] = "flushed"
    payload["result"] = result
    payload["flushed_at"] = datetime.now(timezone.utc).isoformat()
    dest = INBOX / f"{call_id}.json"
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    enq = sub.add_parser("enqueue")
    enq.add_argument("--artifact-path", required=True)
    enq.add_argument("--file-name", required=True)
    enq.add_argument("--folder-id", default=DEFAULT_FOLDER_ID)
    enq.add_argument("--source", default="cli")
    sub.add_parser("pending")
    rec = sub.add_parser("record")
    rec.add_argument("--call-id", required=True)
    rec.add_argument("--result-json", required=True)
    args = ap.parse_args()

    if args.cmd == "enqueue":
        dest = enqueue(
            artifact_path=args.artifact_path,
            file_name=args.file_name,
            folder_id=args.folder_id,
            source=args.source,
        )
        print(f"[drive_connector_bridge] enqueued {dest}")
        return 0
    if args.cmd == "pending":
        items = pending()
        print(json.dumps(items, indent=2))
        print(f"[drive_connector_bridge] pending={len(items)}")
        return 0
    if args.cmd == "record":
        dest = record_result(args.call_id, json.loads(args.result_json))
        print(f"[drive_connector_bridge] recorded {dest}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""IP-WQ-198 upload buffer + flush plan.

Keeps stay queued on disk until google_drive_upload_artifact returns ids.
This script is the hygiene layer between keep_path and --gate.

  python3 scripts/upload_buffer.py --plan
  python3 scripts/upload_buffer.py --inventory
  python3 scripts/upload_buffer.py --write-queue

Writes artifacts/upload-buffer/QUEUE.json so a later Expert pane
can flush what a chat-room pane staged.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOTS = [
    Path("/home/workdir/artifacts/rendered"),
    Path("/home/workdir/.grok/skills/image-pipeline/references/visuals/keeps"),
]
BUFFER = Path("/home/workdir/artifacts/upload-buffer")
DEFAULT_FOLDER = "1_1xhWdBagAlUi-_g1MaksTE36fewmU1-"
AUDIT_FOLDER = "12uZAQB0LfbqmvnP2C6dKqrh7rVHCwz6R"
SPEAK_LINE = "Turn me on to Garage Expert so I can upload."


def iter_keeps():
    seen = set()
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.keep.json"):
            try:
                rec = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            key = str(p.resolve())
            if key in seen:
                continue
            seen.add(key)
            yield p, rec


def queued() -> list[dict]:
    out = []
    for path, rec in iter_keeps():
        drive = rec.get("drive") or {}
        st = drive.get("status") or "queued"
        if st in ("uploaded", "skipped"):
            continue
        local = rec.get("local") or {}
        jpeg = Path(local.get("jpeg") or "")
        calls = []
        for field, key, mime in (
            ("jpeg", "jpeg", "image/jpeg"),
            ("prompt", "prompt_md", "text/markdown"),
            ("keep", "keep_json", "application/json"),
        ):
            raw = local.get(key)
            if not raw:
                continue
            p = Path(raw)
            if not p.exists():
                continue
            if field == "jpeg" and drive.get("jpeg_id"):
                continue
            if field == "prompt" and drive.get("prompt_id"):
                continue
            if field == "keep" and drive.get("keep_id"):
                continue
            art = "/" + "/".join(p.parts[p.parts.index("artifacts") + 1 :]) if "artifacts" in p.parts else f"/rendered/{p.name}"
            calls.append({
                "tool": "google_drive_upload_artifact",
                "arguments": {
                    "artifact_path": art,
                    "file_name": p.name,
                    "folder_id": drive.get("folder_id") or DEFAULT_FOLDER,
                    "mime_type": mime,
                },
                "mark": {
                    "script": "flush_drive_queue.py",
                    "keep": str(path),
                    "field": field,
                },
            })
        out.append({
            "keep": str(path),
            "slug": rec.get("slug"),
            "status": st,
            "jpeg_exists": jpeg.exists() if jpeg else False,
            "folder_id": drive.get("folder_id") or DEFAULT_FOLDER,
            "calls": calls,
        })
    return out


def write_queue(items: list[dict]) -> Path:
    BUFFER.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "ipq-078-buffer/v1",
        "ticket": "IP-WQ-198",
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_queued": len(items),
        "speak_if_no_tool": SPEAK_LINE,
        "keeps_folder": DEFAULT_FOLDER,
        "audit_folder": AUDIT_FOLDER,
        "items": items,
        "rule": "call each tool payload, then flush_drive_queue.py --mark KEEP --field FIELD --file-id ID, then step6 --gate",
    }
    dest = BUFFER / "QUEUE.json"
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (BUFFER / "README.md").write_text(
        "# upload buffer\n\nQueued keeps waiting for google_drive_upload_artifact.\n"
        "Chat-room panes write here. Garage Expert flushes.\n"
        f"If the tool is missing: {SPEAK_LINE}\n",
        encoding="utf-8",
    )
    return dest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", action="store_true")
    p.add_argument("--inventory", action="store_true")
    p.add_argument("--write-queue", action="store_true")
    args = p.parse_args()
    items = queued()
    dest = None
    if args.write_queue or args.plan:
        dest = write_queue(items)
    report = {
        "ok": True,
        "ticket": "IP-WQ-198",
        "n_queued": len(items),
        "queue_file": str(dest) if dest else None,
        "items": items if (args.plan or args.inventory) else [i["slug"] for i in items],
        "speak_if_no_tool": SPEAK_LINE,
        "next": "call google_drive_upload_artifact per calls[], then --mark, then --gate",
    }
    print(json.dumps(report, indent=2))
    return 0 if items else 0


if __name__ == "__main__":
    raise SystemExit(main())

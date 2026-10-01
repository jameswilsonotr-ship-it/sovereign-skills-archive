#!/usr/bin/env python3
"""
IPQ-078 Step 6 — same-turn Drive flush gate.

Python cannot call Drive. This script is the lock that stops the agent
from talking while keeps sit queued.

Usage:
  python3 scripts/step6_drive_flush.py --plan
  python3 scripts/step6_drive_flush.py --from-keep PATH.keep.json
  python3 scripts/step6_drive_flush.py --gate
  python3 scripts/step6_drive_flush.py --gate --stale-minutes 10

Exit:
  0  no queued keeps (uploaded / skipped / empty lake)
  2  queued remains — DO NOT render_file, DO NOT speak picture-saved
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPTS = Path(__file__).resolve().parent
ROOTS = [
    Path("/home/workdir/artifacts/rendered"),
    SCRIPTS.parent / "references" / "visuals" / "keeps",
]
NATIVE = "google_drive_upload_artifact"
PROTOCOL = "IPQ-078-S6"


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
            key = (rec.get("sha256") or {}).get("jpeg") or str(p.resolve())
            if key in seen:
                continue
            seen.add(key)
            yield p, rec


def queued_items(stale_minutes: int = 10) -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    out: List[Dict[str, Any]] = []
    for path, rec in iter_keeps():
        drive = rec.get("drive") or {}
        st = drive.get("status")
        if st in ("uploaded", "skipped"):
            continue
        if st == "uploaded" and drive.get("jpeg_id"):
            continue
        jpeg_raw = (rec.get("local") or {}).get("jpeg") or ""
        jpeg = Path(jpeg_raw) if jpeg_raw else Path()
        uploads = drive.get("uploads") or []
        if not uploads and jpeg_raw and jpeg.exists():
            folder = drive.get("folder_id")
            prompt_name = Path(
                (rec.get("local") or {}).get("prompt_md") or jpeg.with_suffix(".prompt.md")
            ).name
            uploads = [
                {
                    "artifact_path": f"/rendered/{jpeg.name}",
                    "file_name": jpeg.name,
                    "folder_id": folder,
                    "mime_type": "image/jpeg",
                },
                {
                    "artifact_path": f"/rendered/{prompt_name}",
                    "file_name": prompt_name,
                    "folder_id": folder,
                    "mime_type": "text/markdown",
                },
                {
                    "artifact_path": f"/rendered/{path.name}",
                    "file_name": path.name,
                    "folder_id": folder,
                    "mime_type": "application/json",
                },
            ]
        age_min = None
        created = rec.get("created") or ""
        try:
            ts = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            age_min = (now - ts.astimezone(timezone.utc)).total_seconds() / 60.0
        except Exception:
            pass
        calls = []
        for u in uploads:
            calls.append(
                {
                    "tool": NATIVE,
                    "arguments": {
                        "artifact_path": u.get("artifact_path"),
                        "file_name": u.get("file_name"),
                        "folder_id": u.get("folder_id") or drive.get("folder_id"),
                        "mime_type": u.get("mime_type"),
                    },
                    "mark_field": (
                        "jpeg"
                        if str(u.get("mime_type", "")).startswith("image/")
                        else "prompt"
                        if "markdown" in str(u.get("mime_type", ""))
                        or str(u.get("file_name", "")).endswith(".md")
                        else "keep"
                    ),
                    "keep_json": str(path),
                }
            )
        out.append(
            {
                "keep": str(path),
                "slug": rec.get("slug"),
                "status": st or "queued",
                "age_min": None if age_min is None else round(age_min, 1),
                "stale": bool(age_min is not None and age_min >= stale_minutes),
                "local_jpeg": str(jpeg) if jpeg else "",
                "jpeg_exists": jpeg.exists() if jpeg else False,
                "folder_id": drive.get("folder_id"),
                "folder_url": drive.get("folder_url"),
                "calls": calls,
            }
        )
    return out


def plan_one(keep_path: Path, stale_minutes: int = 10) -> Dict[str, Any]:
    rec = json.loads(keep_path.read_text(encoding="utf-8"))
    # reuse scanner by temporarily considering only this file
    items = [i for i in queued_items(stale_minutes) if Path(i["keep"]).resolve() == keep_path.resolve()]
    if not items:
        drive = rec.get("drive") or {}
        return {
            "protocol": PROTOCOL,
            "required": drive.get("status") not in ("uploaded", "skipped"),
            "keep": str(keep_path),
            "status": drive.get("status"),
            "items": [],
            "rule": "already flushed or skipped",
        }
    return {
        "protocol": PROTOCOL,
        "required": True,
        "keep": str(keep_path),
        "status": items[0]["status"],
        "items": items,
        "rule": "call each tool payload, then flush_drive_queue.py --mark KEEP --field jpeg|prompt|keep --file-id ID",
    }


def gate(stale_minutes: int = 10) -> Dict[str, Any]:
    items = queued_items(stale_minutes)
    blocked = len(items) > 0
    return {
        "protocol": PROTOCOL,
        "emit_allowed": not blocked,
        "queued": len(items),
        "stale": sum(1 for i in items if i.get("stale")),
        "stale_minutes": stale_minutes,
        "items": [
            {
                "slug": i.get("slug"),
                "keep": i.get("keep"),
                "status": i.get("status"),
                "age_min": i.get("age_min"),
                "jpeg_exists": i.get("jpeg_exists"),
            }
            for i in items
        ],
        "reason": "ok" if not blocked else "queued keeps remain — flush before speak",
        "action": "proceed" if not blocked else "call_connected_tool google_drive_upload_artifact then --mark",
        "host_upload_tool": NATIVE,
        "host_note": (
            "If google_drive_upload_artifact is missing from this host catalog, "
            "gate stays 2. Do not claim Drive-saved. See IP-WQ-115 / IP-WQ-082 / IP-WQ-122."
        ),
        "claim": "Absolute Liv HUB",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="IPQ-078 Step 6 Drive flush gate")
    ap.add_argument("--plan", action="store_true", help="print connected-tool payloads for all queued keeps")
    ap.add_argument("--from-keep", default="", help="plan a single keep.json")
    ap.add_argument("--gate", action="store_true", help="exit 2 if any keep is still queued")
    ap.add_argument("--stale-minutes", type=int, default=10)
    args = ap.parse_args()
    if args.from_keep:
        out = plan_one(Path(args.from_keep), args.stale_minutes)
        print(json.dumps(out, indent=2))
        return 0 if not out.get("required") else 2
    if args.gate:
        out = gate(args.stale_minutes)
        print(json.dumps(out, indent=2))
        return 0 if out["emit_allowed"] else 2
    # default = plan all
    items = queued_items(args.stale_minutes)
    out = {
        "protocol": PROTOCOL,
        "required": bool(items),
        "queued": len(items),
        "items": items,
        "native_tool": NATIVE,
        "mark": "python3 scripts/flush_drive_queue.py --mark KEEP.json --field jpeg|prompt|keep --file-id ID",
        "gate": "python3 scripts/step6_drive_flush.py --gate",
        "rule": "Same turn. Do not render_file or claim Drive-saved until --gate exits 0.",
        "claim": "Absolute Liv HUB",
    }
    print(json.dumps(out, indent=2))
    return 2 if items else 0


if __name__ == "__main__":
    sys.exit(main())

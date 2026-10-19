#!/usr/bin/env python3
"""
flush_drive_queue.py — IPQ-078 companion mark & inventory engine.

Handles post-upload sidecar stamping for Google Drive artifact synchronization.
Companion tool to step6_drive_flush.py.

Usage:
  # Mark an uploaded artifact ID in a keep.json record:
  python3 scripts/flush_drive_queue.py --mark /path/to/xxx.keep.json --field jpeg --file-id 1AbCd...
  python3 scripts/flush_drive_queue.py --mark /path/to/xxx.keep.json --field prompt --file-id 1EfGh...
  python3 scripts/flush_drive_queue.py --mark /path/to/xxx.keep.json --field keep --file-id 1IjKl...

  # Scan inventory across rendered and skill-tree keeps:
  python3 scripts/flush_drive_queue.py --inventory
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PROTOCOL = "IPQ-078-S6"
SCRIPTS = Path(__file__).resolve().parent
ROOTS = [
    Path("/home/workdir/artifacts/rendered"),
    SCRIPTS.parent / "references" / "visuals" / "keeps",
]
DEFAULT_FOLDER_ID = "1_1xhWdBagAlUi-_g1MaksTE36fewmU1-"


def mark_keep(keep_path_str: str, field: str, file_id: str) -> Dict[str, Any]:
    kp = Path(keep_path_str).resolve()
    if not kp.exists():
        return {"ok": False, "error": f"Keep file not found: {kp}"}

    try:
        data = json.loads(kp.read_text(encoding="utf-8"))
    except Exception as e:
        return {"ok": False, "error": f"Failed to parse JSON: {e}"}

    drive = data.setdefault("drive", {})
    field_lower = field.lower().strip()

    if field_lower in ("jpeg", "jpg", "image"):
        drive["jpeg_id"] = file_id
    elif field_lower in ("prompt", "prompt_md", "md"):
        drive["prompt_id"] = file_id
    elif field_lower in ("keep", "keep_json", "json"):
        drive["keep_id"] = file_id
    else:
        return {"ok": False, "error": f"Unsupported field: {field}. Must be jpeg, prompt, or keep."}

    # If uploads list exists, update the specific entry
    uploads = drive.get("uploads") or []
    for u in uploads:
        mtype = str(u.get("mime_type", ""))
        fname = str(u.get("file_name", ""))
        if field_lower in ("jpeg", "jpg", "image") and (mtype.startswith("image/") or fname.endswith(".jpg")):
            u["file_id"] = file_id
        elif field_lower in ("prompt", "prompt_md", "md") and ("markdown" in mtype or fname.endswith(".md")):
            u["file_id"] = file_id
        elif field_lower in ("keep", "keep_json", "json") and ("json" in mtype or fname.endswith(".json")):
            u["file_id"] = file_id

    # Check completeness
    has_jpeg = bool(drive.get("jpeg_id"))
    has_prompt = bool(drive.get("prompt_id"))
    has_keep = bool(drive.get("keep_id"))

    if has_jpeg and has_prompt and has_keep:
        drive["status"] = "uploaded"
    elif has_jpeg or has_prompt or has_keep:
        drive["status"] = "partial"
    else:
        drive["status"] = "queued"

    drive["last_marked"] = datetime.now(timezone.utc).isoformat()
    kp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    return {
        "ok": True,
        "keep": str(kp),
        "field": field_lower,
        "file_id": file_id,
        "status": drive["status"],
        "complete": bool(has_jpeg and has_prompt and has_keep),
    }


def inventory(stale_minutes: int = 10) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    queued = 0
    uploaded = 0
    partial = 0
    stale = 0
    missing_local = []
    items = []

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

            drive = rec.get("drive") or {}
            st = drive.get("status", "queued")
            has_jpeg_id = bool(drive.get("jpeg_id"))
            has_prompt_id = bool(drive.get("prompt_id"))
            has_keep_id = bool(drive.get("keep_id"))

            jpeg_raw = (rec.get("local") or {}).get("jpeg") or ""
            jpeg = Path(jpeg_raw) if jpeg_raw else Path()
            jpeg_exists = jpeg.exists() if jpeg_raw else False

            if not jpeg_exists and st != "uploaded":
                missing_local.append(str(p))

            created = rec.get("created") or ""
            age_min = None
            try:
                ts = datetime.fromisoformat(created.replace("Z", "+00:00"))
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                age_min = (now - ts.astimezone(timezone.utc)).total_seconds() / 60.0
            except Exception:
                pass

            is_stale = bool(age_min is not None and age_min >= stale_minutes and st not in ("uploaded", "skipped"))
            if is_stale:
                stale += 1

            if st == "uploaded" and has_jpeg_id:
                uploaded += 1
            elif st == "partial" or (has_jpeg_id or has_prompt_id or has_keep_id):
                partial += 1
            else:
                queued += 1
                items.append({
                    "keep": str(p),
                    "slug": rec.get("slug"),
                    "status": st,
                    "age_min": round(age_min, 1) if age_min is not None else None,
                    "stale": is_stale,
                })

    return {
        "queued": queued,
        "uploaded": uploaded,
        "partial": partial,
        "stale": stale,
        "stale_minutes": stale_minutes,
        "missing_local": missing_local,
        "folder_id": DEFAULT_FOLDER_ID,
        "items": items,
        "claim": "Absolute Liv HUB",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="IPQ-078 companion flush & mark queue engine")
    ap.add_argument("--mark", default="", help="Path to .keep.json file to update")
    ap.add_argument("--field", choices=["jpeg", "prompt", "keep"], default="jpeg", help="Sidecar field to record")
    ap.add_argument("--file-id", default="", help="Google Drive File ID returned by upload")
    ap.add_argument("--inventory", action="store_true", help="Print queue inventory status JSON")
    ap.add_argument("--stale-minutes", type=int, default=10)
    args = ap.parse_args()

    if args.mark:
        if not args.file_id:
            print(json.dumps({"ok": False, "error": "--file-id is required with --mark"}))
            return 1
        res = mark_keep(args.mark, args.field, args.file_id)
        print(json.dumps(res, indent=2))
        return 0 if res.get("ok") else 1

    # Default / inventory mode
    res = inventory(args.stale_minutes)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

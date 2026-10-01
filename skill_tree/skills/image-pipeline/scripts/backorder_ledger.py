#!/usr/bin/env python3
"""IP-WQ-122 — serialization backorder ledger.

Walks artifacts/rendered and skill-tree keeps. Emits a markdown + json
ledger of every keep that is not a complete Drive triple.

Does not upload. Does not mark. Read-only.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ROOTS = [
    Path("/home/workdir/artifacts/rendered"),
    Path("/home/workdir/.grok/skills/image-pipeline/references/visuals/keeps"),
]
OUT_DIR = Path("/home/workdir/artifacts/work-queue")


def iter_keeps():
    seen = set()
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.keep.json"):
            try:
                rec = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                yield p, None
                continue
            key = (rec.get("sha256") or {}).get("jpeg") or str(p.resolve())
            if key in seen:
                continue
            seen.add(key)
            yield p, rec


def classify(path: Path, rec: dict | None) -> dict:
    row = {
        "keep": str(path),
        "slug": None,
        "stamp": None,
        "status": "bad-json",
        "action": "orphan-repair",
        "jpeg_exists": False,
        "prompt_exists": False,
        "keep_exists": path.exists(),
        "jpeg_id": None,
        "prompt_id": None,
        "keep_id": None,
    }
    if rec is None:
        return row
    local = rec.get("local") or {}
    drive = rec.get("drive") or {}
    jpeg = Path(local.get("jpeg") or path.with_suffix(".jpg"))
    prompt = Path(local.get("prompt_md") or path.with_name(path.name.replace(".keep.json", ".prompt.md")))
    # also accept sibling names
    if not jpeg.exists():
        sib = path.with_name(path.name.replace(".keep.json", ".jpg"))
        if sib.exists():
            jpeg = sib
    if not prompt.exists():
        sib = path.with_name(path.name.replace(".keep.json", ".prompt.md"))
        if sib.exists():
            prompt = sib
    row.update(
        {
            "slug": rec.get("slug"),
            "stamp": rec.get("stamp") or rec.get("created"),
            "status": drive.get("status") or "unknown",
            "jpeg_exists": jpeg.exists(),
            "prompt_exists": prompt.exists(),
            "jpeg_id": drive.get("jpeg_id"),
            "prompt_id": drive.get("prompt_id"),
            "keep_id": drive.get("keep_id"),
        }
    )
    complete = bool(row["jpeg_id"] and row["prompt_id"] and row["keep_id"])
    if complete and row["status"] == "uploaded":
        row["action"] = "done"
    elif not row["jpeg_exists"]:
        row["action"] = "missing-local"
    elif row["status"] in ("queued", "partial", "unknown") and row["jpeg_exists"]:
        row["action"] = "flush" if row["prompt_exists"] else "orphan-repair"
        if str(path).startswith("/home/workdir/artifacts/rendered"):
            if (rec.get("created") or "").startswith("2026-09-03") or (rec.get("created") or "").startswith(
                "2026-09-04"
            ):
                row["cohort"] = "last-night-local"
                row["action"] = "local-only-until-upload-tool"
    else:
        row["action"] = "review"
    return row


def main() -> int:
    rows = [classify(p, rec) for p, rec in iter_keeps()]
    open_rows = [r for r in rows if r["action"] != "done"]
    counts = {}
    for r in open_rows:
        counts[r["action"]] = counts.get(r["action"], 0) + 1
    stamp = datetime.now(ET).strftime("%Y%m%d-%H%M%S")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "ipq-122-backorder/v1",
        "created": datetime.now(ET).isoformat(timespec="seconds"),
        "ticket": "IP-WQ-122",
        "parent": "IP-WQ-115",
        "host_upload_tool": "google_drive_upload_artifact",
        "host_upload_present": False,
        "folder_id": "1_1xhWdBagAlUi-_g1MaksTE36fewmU1-",
        "total_keeps": len(rows),
        "open": len(open_rows),
        "by_action": counts,
        "rows": open_rows,
    }
    json_path = OUT_DIR / f"BACKORDER_LEDGER_{stamp}.json"
    md_path = OUT_DIR / f"BACKORDER_LEDGER_{stamp}.md"
    latest_json = OUT_DIR / "BACKORDER_LEDGER.json"
    latest_md = OUT_DIR / "BACKORDER_LEDGER.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_json.write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    lines = [
        "# BACKORDER LEDGER — IP-WQ-122",
        "",
        f"Created: {payload['created']}",
        f"Open rows: {payload['open']} / {payload['total_keeps']}",
        f"By action: {counts}",
        "Host upload tool: **missing** this Heavy hop. Do not claim Drive-saved.",
        "",
        "| action | slug | stamp | jpeg | prompt | jpeg_id | status |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in open_rows:
        lines.append(
            f"| {r['action']} | {r.get('slug') or ''} | {r.get('stamp') or ''} | "
            f"{'Y' if r['jpeg_exists'] else 'N'} | {'Y' if r['prompt_exists'] else 'N'} | "
            f"{r.get('jpeg_id') or ''} | {r.get('status')} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    latest_md.write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in payload if k != "rows"}, indent=2))
    print(f"wrote {md_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

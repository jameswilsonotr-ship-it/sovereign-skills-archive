#!/usr/bin/env python3
"""Shared deterministic primitives for grok-conversation-miner.

Stdlib-first. No fifth mouth. No GitHub Contents API for binaries.
"""
from __future__ import annotations

import hashlib
import json
import re
import tarfile
import uuid
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")
CLAIM = "Absolute Liv HUB"
SKILL = "grok-conversation-miner"
BINARY_EXT = {".tar", ".gz", ".tgz", ".zip", ".png", ".jpg", ".jpeg", ".webp", ".mp4", ".webm", ".gif", ".bin"}
MAX_GITHUB_BYTES = 800 * 1024

CENSUS_REQUIRED = (
    "date",
    "slug",
    "keep_or_delta",
    "twin_id",
    "receipt_id",
    "miner_tar_id",
    "global_extract_id",
    "redacted",
    "packed",
    "pointed",
    "status",
)


def now_et(when: datetime | None = None) -> datetime:
    if when is None:
        return datetime.now(TZ)
    if when.tzinfo is None:
        return when.replace(tzinfo=TZ)
    return when.astimezone(TZ)


def stamp_iso(when: datetime | None = None) -> str:
    return now_et(when).strftime("%Y-%m-%dT%H:%M:%S%z")


def stamp_compact(when: datetime | None = None) -> str:
    return now_et(when).strftime("%Y%m%dT%H%M%S")


def run_id(prefix: str = "GCM") -> str:
    return f"{prefix}_{stamp_compact()}_{uuid.uuid4().hex[:8]}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def safety_gate(path: Path) -> dict:
    """Return {ok_for_github: bool, reason: str}."""
    suffix = "".join(path.suffixes).lower()
    size = path.stat().st_size if path.exists() else 0
    binary = any(ext in suffix for ext in BINARY_EXT) or path.suffix.lower() in BINARY_EXT
    if binary or size > MAX_GITHUB_BYTES:
        return {
            "ok_for_github": False,
            "reason": "BINARY_OR_LARGE_PAYLOAD — GitHub Contents API path blocked. Use Google Drive (primary) or Git LFS instead.",
            "size": size,
            "binary": binary,
        }
    return {"ok_for_github": True, "reason": "text-small", "size": size, "binary": False}


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_json(path: Path, obj: Any) -> Path:
    return write_text(path, json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def validate_census_row(row: dict) -> list[str]:
    missing = [k for k in CENSUS_REQUIRED if k not in row]
    return missing


def census_done(row: dict) -> bool:
    redacted_ok = row.get("redacted") in (True, "n/a", "na", "N/A")
    return bool(row.get("packed")) and bool(row.get("pointed")) and redacted_ok


def era_for_date(date_s: str) -> str:
    if date_s < "2026-08-11":
        return "KEEP"
    if date_s <= "2026-09-06":
        return "DELTA"
    return "LIVE"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s[:48] or "untitled"


def make_tar(src_dir: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(dest, "w:gz") as tar:
        tar.add(src_dir, arcname=src_dir.name)
    return dest


def yaml_stamp_block(**fields: Any) -> str:
    lines = ["---"]
    for k in sorted(fields):
        v = fields[k]
        if isinstance(v, bool):
            v = "true" if v else "false"
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def render_mail_filesystem(
    *,
    subject_slug: str,
    run: str,
    verb: str,
    claim: str,
    tree: dict[str, str],
    turns_remaining_estimate: int | str,
    toc: list[str],
    omissions: list[str],
    drive_ids: dict[str, str] | None = None,
    when: datetime | None = None,
) -> EmailMessage:
    """Email body is a directory, not a paragraph. WQ-013."""
    msg = EmailMessage()
    stamp = stamp_iso(when)
    msg["Subject"] = (
        f"[GROKBOT] [CILIA-BUS] [FROM-O-HEAVY] [MCP-EVENT] [PRI-MED] {subject_slug}"
    )
    msg["From"] = "olivia@livhub.local"
    msg["To"] = "vesper@cilia.local"
    msg["X-GCM-Run-Id"] = run
    msg["X-GCM-Verb"] = verb
    msg["X-GCM-Claim"] = claim
    msg["X-GCM-Stamp"] = stamp
    msg["X-GCM-Turns-Remaining-Estimate"] = str(turns_remaining_estimate)
    body = [
        f"/mail/{subject_slug}/",
        f"  00_STAMP.txt            {stamp}",
        f"  01_RUN_ID.txt           {run}",
        f"  02_VERB.txt             {verb}",
        f"  03_CLAIM.txt            {claim}",
        f"  04_TURNS_REMAINING.txt  {turns_remaining_estimate}",
        "  05_TOC.md",
    ]
    for line in toc:
        body.append(f"    - {line}")
    body.append("  06_OMISSIONS.md")
    for line in omissions:
        body.append(f"    - {line}")
    body.append("  07_TREE/")
    for name in sorted(tree):
        body.append(f"    {name}")
        for content_line in tree[name].splitlines()[:8]:
            body.append(f"      {content_line}")
    body.append("  08_DRIVE_ACK/")
    for k, v in sorted((drive_ids or {}).items()):
        body.append(f"    {k}={v}")
    body.append("  09_NOTE.txt")
    body.append("    Drive is ACK. Mail is wake. Time is not the budget.")
    msg.set_content("\n".join(body) + "\n")
    return msg


# --- compatibility aliases used by layout/packers/census/toc/mail/smoke ---
import os
from datetime import timezone

NY = TZ
LAYOUT = (
    "00_HEADER.md",
    "01_TOC.md",
    "02_OMISSIONS.md",
    "03_TURNS.md",
    "04_DECISIONS.md",
    "05_SKILL_DELTA",
    "06_SANDBOX",
    "07_MAIL",
    "08_RECEIPTS",
    "MANIFEST.md",
)
SECRET_HINTS = (
    "cookies",
    "tskey",
    "sftp",
    "youtube-cookies",
    "private_key",
    ".pem",
    "secrets/",
)


def stamps(now: datetime | None = None) -> dict:
    dt = now or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    ny = dt.astimezone(TZ)
    utc = dt.astimezone(timezone.utc)
    return {
        "stamp_utc": utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stamp_ny": ny.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "date_ny": ny.strftime("%Y-%m-%d"),
        "claim": CLAIM,
        "skill": SKILL,
    }


def jsonl_read(path: Path) -> list[dict]:
    return load_jsonl(path)


def jsonl_write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows)
    path.write_text(body, encoding="utf-8")


def jsonl_upsert(path: Path, key: str, row: dict) -> list[dict]:
    rows = jsonl_read(path)
    found = False
    out = []
    for existing in rows:
        if existing.get(key) == row.get(key):
            merged = dict(existing)
            merged.update(row)
            out.append(merged)
            found = True
        else:
            out.append(existing)
    if not found:
        out.append(row)
    jsonl_write(path, out)
    return out


def classify(path: Path) -> str:
    text = str(path).lower()
    if any(h in text for h in SECRET_HINTS):
        return "secret"
    if "imagine" in text or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        if "plate" in text:
            return "plates"
        return "imagine"
    if path.suffix.lower() in {".mp4", ".webm", ".mov"} or "video" in text:
        return "video"
    if "plate" in text:
        return "plates"
    if path.suffix.lower() in {".tar", ".gz"} or text.endswith(".tar.gz"):
        return "archive"
    if path.suffix.lower() in {".jsonl", ".json"}:
        return "index"
    if path.suffix.lower() in {".md", ".txt"}:
        return "markdown"
    return "other"


def walk_files(root: Path) -> list[Path]:
    files = [p for p in root.rglob("*") if p.is_file()]
    return sorted(files, key=lambda p: str(p).replace(os.sep, "/"))


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()

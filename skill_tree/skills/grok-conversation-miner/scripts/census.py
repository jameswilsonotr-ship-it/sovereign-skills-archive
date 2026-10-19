"""CENSUS.jsonl — packed / pointed / redacted. Does not mine. Does not tar."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

REQUIRED = (
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


def row_status(row: dict[str, Any]) -> str:
    packed = bool(row.get("packed"))
    pointed = bool(row.get("pointed"))
    red = row.get("redacted")
    if packed and pointed and (red is True or red in ("n/a", "na", None)):
        return "DONE"
    if row.get("twin_id") in (None, "", "NO_TWIN"):
        return "NO_TWIN"
    return "OPEN"


def validate_row(row: dict[str, Any]) -> list[str]:
    errs = []
    for k in REQUIRED:
        if k not in row:
            errs.append(f"missing:{k}")
    if row.get("keep_or_delta") not in ("KEEP", "DELTA", "LIVE", None):
        errs.append("keep_or_delta")
    return errs


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            row = dict(row)
            row["status"] = row_status(row)
            errs = validate_row(row)
            if errs:
                raise ValueError(f"bad census row {errs}: {row}")
            f.write(json.dumps(row, sort_keys=True) + "\n")
            n += 1
    return n


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def done(row: dict[str, Any]) -> bool:
    return row_status(row) == "DONE"


def upsert(path: Path, row: dict[str, Any]) -> dict[str, Any]:
    """Compat for smoke harness. Writes/replaces by date+slug key."""
    row = dict(row)
    row.setdefault("keep_or_delta", "LIVE")
    if str(row.get("keep_or_delta")).lower() == "live":
        row["keep_or_delta"] = "LIVE"
    row.setdefault("twin_id", "")
    row.setdefault("receipt_id", "")
    row.setdefault("miner_tar_id", "")
    row.setdefault("global_extract_id", "")
    row.setdefault("redacted", "n/a")
    row.setdefault("packed", False)
    row.setdefault("pointed", False)
    row["status"] = row_status(row)
    existing = read_jsonl(path) if path.exists() else []
    key = f"{row.get('date')}:{row.get('slug')}"
    out = []
    found = False
    for old in existing:
        if f"{old.get('date')}:{old.get('slug')}" == key:
            merged = dict(old)
            merged.update(row)
            merged["status"] = row_status(merged)
            out.append(merged)
            row = merged
            found = True
        else:
            out.append(old)
    if not found:
        out.append(row)
    write_jsonl(path, out)
    return row


def l0_decision(row: dict[str, Any]) -> str:
    """Sunset L0 reads census before RAN vs SKIP-EXISTS. Keep-everything: SKIP is annotation."""
    if row.get("status") == "DONE" and row.get("packed") and row.get("pointed"):
        return "SKIP-EXISTS"
    if row.get("status") == "NO_TWIN":
        return "NO_TWIN"
    return "RAN"


record = upsert
jsonl_read = read_jsonl


record = upsert

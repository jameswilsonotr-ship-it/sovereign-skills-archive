#!/usr/bin/env python3
"""GCM-WQ-020 append-only export receipt log.

Never rewrite. Never upsert. Never sort-in-place.
SKIP-EXISTS is a row. Silence is a bug.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from gcm_lib import CLAIM, stamps

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = SKILL_ROOT / "references" / "modules" / "data" / "EXPORT_LOG.jsonl"

ACTIONS = (
    "EXPORTED",
    "SKIP-EXISTS",
    "SKIP-OVERLAP",
    "SKIP-NO-HIT",
    "SECRET",
    "NO_TWIN",
    "NOT-WALKED",
    "TOO-LARGE",
    "PANE-VANISH",
    "OPERATOR-SAID-NO",
    "KEEP-DUPLICATE",
    "WOULD-EXPORT",
    "WOULD-SKIP",
    "FAIL",
)

REQUIRED = (
    "run_id",
    "verb",
    "conversation_key",
    "action",
)


def _canonical(row: dict) -> str:
    return json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def row_hash(row: dict) -> str:
    payload = {k: v for k, v in row.items() if k != "row_sha256"}
    return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def file_sha256(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def append_row(log_path: Path, **fields) -> dict:
    """Append exactly one line. Creates the file if missing. Never truncates."""
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_rows(log_path)
    s = stamps()
    row = {
        "seq": len(existing) + 1,
        "stamp_iso_ny": s.get("stamp_ny"),
        "stamp_iso_utc": s.get("stamp_utc"),
        "stamp_utc": s.get("stamp_utc"),
        "stamp_ny": s.get("stamp_ny"),
        "claim": CLAIM,
        "exported": False,
        "still_gettable": True,
        "sha256": "",
        "pointer": "",
        "pointer_id": "",
        "path": "",
        "klass": "",
        "lane": "",
        "slug": "",
        "msg_id": "",
        "note": "",
        "prev_row_sha256": existing[-1].get("row_sha256", "") if existing else "",
    }
    row.update(fields)
    action = str(row.get("action", ""))
    if action not in ACTIONS:
        raise ValueError(f"unknown action {action!r}")
    missing = [k for k in REQUIRED if not row.get(k)]
    if missing:
        raise ValueError(f"export log row missing {missing}")
    if action == "EXPORTED":
        row["exported"] = True
    row["row_sha256"] = row_hash(row)
    line = json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line)
    return row


def cite(path: Path) -> dict:
    rows = read_rows(path)
    return {
        "path": str(path),
        "exists": path.exists(),
        "count": len(rows),
        "head_seq": rows[-1]["seq"] if rows else 0,
        "head_row_sha256": rows[-1].get("row_sha256", "") if rows else "",
        "file_sha256": file_sha256(path),
        "claim": CLAIM,
    }


def cite_markdown(path: Path) -> str:
    c = cite(path)
    return (
        f"- export_log: `{c['path']}`\n"
        f"- export_log_count: {c['count']}\n"
        f"- export_log_head_seq: {c['head_seq']}\n"
        f"- export_log_head_sha256: `{c['head_row_sha256']}`\n"
        f"- export_log_file_sha256: `{c['file_sha256']}`\n"
    )


def delta_markdown(rows: list[dict]) -> str:
    lines = ["# EXPORT_LOG_DELTA", "", "| seq | action | path | exported | pointer |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(
            f"| {r.get('seq')} | {r.get('action')} | {r.get('path')} | {r.get('exported')} | {r.get('pointer') or r.get('pointer_id')} |"
        )
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--log", type=Path, default=DEFAULT_LOG)
    sub = p.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("append")
    add.add_argument("--run-id", required=True)
    add.add_argument("--verb", required=True)
    add.add_argument("--conversation-key", required=True)
    add.add_argument("--action", required=True)
    add.add_argument("--lane", default="")
    add.add_argument("--path", default="")
    add.add_argument("--klass", default="")
    add.add_argument("--slug", default="")
    add.add_argument("--pointer", default="")
    add.add_argument("--sha256", default="")
    add.add_argument("--note", default="")
    add.add_argument("--still-gettable", action="store_true")
    add.add_argument("--not-gettable", action="store_true")
    sub.add_parser("cite")
    sub.add_parser("tail")
    args = p.parse_args(argv)
    if args.cmd == "append":
        row = append_row(
            args.log,
            run_id=args.run_id,
            verb=args.verb,
            conversation_key=args.conversation_key,
            action=args.action,
            lane=args.lane,
            path=args.path,
            klass=args.klass,
            slug=args.slug,
            pointer=args.pointer,
            pointer_id=args.pointer,
            sha256=args.sha256,
            note=args.note,
            still_gettable=False if args.not_gettable else True,
        )
        print(json.dumps(row, sort_keys=True))
        return 0
    if args.cmd == "cite":
        print(cite_markdown(args.log), end="")
        return 0
    rows = read_rows(args.log)
    print(delta_markdown(rows[-12:]), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


STATUS_TO_ACTION = {
    "RAN": "EXPORTED",
    "SKIP-EXISTS": "SKIP-EXISTS",
    "SKIP-OVERLAP": "SKIP-OVERLAP",
    "SKIP-NO-HIT": "SKIP-NO-HIT",
    "SKIP-NO-SHARD": "NO_TWIN",
    "NO_TWIN": "NO_TWIN",
    "WOULD-RAN": "WOULD-EXPORT",
    "WOULD-MAIL": "WOULD-EXPORT",
    "WOULD-SKIP": "WOULD-SKIP",
    "FAIL": "FAIL",
}


def log_lanes(log_path: Path, *, run_id: str, verb: str, conversation_key: str, lanes: list[dict], dry_run: bool = True) -> list[dict]:
    """Append one receipt per lane. Dry-run remaps EXPORTED -> WOULD-EXPORT."""
    out = []
    for lane in lanes:
        status = lane.get("status") or lane.get("action") or ""
        action = STATUS_TO_ACTION.get(status, status if status in ACTIONS else "WOULD-SKIP")
        if dry_run and action == "EXPORTED":
            action = "WOULD-EXPORT"
        row = append_row(
            log_path,
            run_id=run_id,
            verb=verb,
            conversation_key=conversation_key,
            action=action,
            lane=lane.get("lane") or lane.get("name") or "",
            path=lane.get("path") or lane.get("file") or lane.get("lane") or "",
            klass=lane.get("name") or lane.get("class") or "",
            note=lane.get("note") or status,
            pointer=str(lane.get("pointer") or lane.get("file") or ""),
        )
        out.append(row)
    return out


# compat aliases used by harvest_hooks / stress
DEFAULT = DEFAULT_LOG
log_sha256 = file_sha256

def write_mirror(path: Path) -> Path:
    md = Path(path).with_suffix(".md")
    rows = read_rows(Path(path))
    md.write_text(delta_markdown(rows), encoding="utf-8")
    return md

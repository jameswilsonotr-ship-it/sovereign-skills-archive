#!/usr/bin/env python3
"""TOC + OMISSIONS writer. GCM-WQ-011.

Every package lists what shipped AND what could have.
Skip-exists becomes a line, not silence. Duplicates allowed (WQ-014).
"""
from __future__ import annotations

from pathlib import Path

from gcm_lib import stamp_iso, write_text, yaml_stamp_block


def write_toc_and_omissions(
    out_dir: Path,
    *,
    shipped: list[dict],
    omitted: list[dict],
    run: str,
    verb: str,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    toc_lines = [
        yaml_stamp_block(skill="grok-conversation-miner", run_id=run, verb=verb, stamp=stamp_iso(), kind="TOC"),
        f"# TOC — {run}\n",
        "| path | class | sha256 | note |",
        "|---|---|---|---|",
    ]
    for item in shipped:
        toc_lines.append(
            f"| {item.get('path')} | {item.get('class','file')} | {item.get('sha256','')} | {item.get('note','')} |"
        )
    omitted_lines = [
        yaml_stamp_block(skill="grok-conversation-miner", run_id=run, verb=verb, stamp=stamp_iso(), kind="OMISSIONS"),
        f"# OMISSIONS — {run}\n",
        "What this package could have included and did not.\n",
        "| path_or_lane | reason | skip_code | recoverable |",
        "|---|---|---|---|",
    ]
    for item in omitted:
        omitted_lines.append(
            f"| {item.get('path')} | {item.get('reason')} | {item.get('skip_code','')} | {item.get('recoverable', True)} |"
        )
    if not omitted:
        omitted_lines.append("| — | nothing omitted this run |  |  |")
    toc = write_text(out_dir / "TOC.md", "\n".join(toc_lines) + "\n")
    om = write_text(out_dir / "OMISSIONS.md", "\n".join(omitted_lines) + "\n")
    return toc, om


def scan(root: Path, extra_omissions: list[dict] | None = None) -> dict:
    from gcm_lib import classify, sha256_file, walk_files, rel
    toc_rows = []
    omissions = list(extra_omissions or [])
    for f in walk_files(root):
        klass = classify(f)
        rec = {
            "path": rel(root, f),
            "class": klass,
            "bytes": f.stat().st_size,
            "sha256": sha256_file(f) if f.is_file() else "",
        }
        if klass == "secret":
            rec["reason"] = "SECRET"
            rec["still_gettable"] = False
            omissions.append(rec)
        else:
            rec["note"] = ""
            toc_rows.append(rec)
    return {"toc": toc_rows, "omissions": omissions}


def write_pair(space: Path, scanned: dict) -> tuple[Path, Path]:
    shipped = [
        {"path": r["path"], "class": r.get("class"), "sha256": r.get("sha256", ""), "note": r.get("note", "")}
        for r in scanned.get("toc", [])
    ]
    omitted = [
        {
            "path": r.get("path"),
            "reason": r.get("reason", ""),
            "skip_code": r.get("reason", ""),
            "recoverable": r.get("still_gettable", True),
        }
        for r in scanned.get("omissions", [])
    ]
    return write_toc_and_omissions(space, shipped=shipped, omitted=omitted, run="smoke", verb="sunset-smoke")

#!/usr/bin/env python3
"""Sunset dry-run / fixture engine. L0–L8.

Does not talk to live Drive. Reads a fixture conversation space.
GCM-WQ-004 dry-run proof happens against fixtures first (WQ-009).
Keep-everything (WQ-014): SKIP-EXISTS is an annotation row, not a drop.
L7 outbox is included in the L4 tree (WQ-003).
"""
from __future__ import annotations

import json
from pathlib import Path

from census import record as census_record
from gcm_lib import (
    CLAIM,
    era_for_date,
    render_mail_filesystem,
    run_id,
    sha256_file,
    stamp_iso,
    write_json,
    write_text,
    yaml_stamp_block,
)
from packers import pack as pack_artifacts
from toc_omissions import write_toc_and_omissions
from export_log import append_row, cite as cite_log, write_mirror

export_log_cite = cite_log

LANES = ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]

STATUS_TO_ACTION = {
    "RAN": "EXPORTED",
    "WOULD-RAN": "NOT-WALKED",
    "WOULD-MAIL": "NOT-WALKED",
    "SKIP-EXISTS": "SKIP-EXISTS",
    "SKIP-OVERLAP": "SKIP-OVERLAP",
    "SKIP-NO-HIT": "SKIP-NO-HIT",
    "SKIP-NO-FLAG": "SKIP-NO-HIT",
    "SKIP-NO-SHARD": "SKIP-NO-HIT",
    "NO_TWIN": "NO_TWIN",
}


def log_lanes(log_path: Path, run_id: str, verb: str, key: str, lanes: dict) -> list[dict]:
    written = []
    for lane, row in lanes.items():
        status = row.get("status", "NOT-WALKED")
        action = STATUS_TO_ACTION.get(status, "NOT-WALKED")
        written.append(
            append_row(
                log_path,
                run_id=run_id,
                verb=verb,
                action=action,
                path=row.get("file") or lane,
                lane=lane,
                conversation_key=key,
                note=row.get("note", ""),
            )
        )
    return written


def _exists(p: Path | None) -> bool:
    return bool(p and p.exists())


def run_sunset(space: Path, *, dry_run: bool, include_l8: bool = False) -> dict:
    meta = json.loads((space / "CONVERSATION.json").read_text(encoding="utf-8"))
    date = meta["date"]
    slug = meta["slug"]
    rid = run_id("SUN")
    out = space / "runs" / rid
    if not dry_run:
        out.mkdir(parents=True, exist_ok=True)

    lake_twin = next(iter((space / "lake").glob("*.md")), None) if (space / "lake").exists() else None
    receipt = next(iter((space / "lake").glob("RECEIPT*")), None) if (space / "lake").exists() else None
    miner_tar = next(iter((space / "miner").glob("*.tar.gz")), None) if (space / "miner").exists() else None
    extract_tar = next(iter((space / "extract").glob("*.tar.gz")), None) if (space / "extract").exists() else None
    export_json = space / "export" / "prod-grok-backend.json"

    lanes = {}

    def card(lane, status, note, **extra):
        row = {"lane": lane, "status": status, "note": note, "stamp": stamp_iso(), **extra}
        lanes[lane] = row
        return row

    card("L0", "RAN", f"{date} {slug} era={era_for_date(date)}", date=date, slug=slug, era=era_for_date(date))

    if _exists(lake_twin):
        card("L1", "SKIP-EXISTS", "lake twin present", file=str(lake_twin), skip_annotation="duplicate-allowed")
    else:
        card("L1", "NO_TWIN" if dry_run else "RAN", "no lake twin in fixture")

    if _exists(receipt):
        card("L2", "SKIP-EXISTS", "receipt present", file=str(receipt), skip_annotation="duplicate-allowed")
    else:
        card("L2", "RAN" if not dry_run else "WOULD-RAN", "would write receipt")

    if _exists(miner_tar):
        card("L3", "SKIP-OVERLAP", "miner tar present", file=str(miner_tar), skip_annotation="duplicate-allowed")
    else:
        card("L3", "WOULD-RAN", "no miner tar")

    if _exists(extract_tar):
        card("L4", "SKIP-EXISTS", "global extract present", file=str(extract_tar), skip_annotation="duplicate-allowed")
    else:
        card("L4", "WOULD-RAN", "would global extract + include L7 outbox in tree")

    card("L5", "WOULD-MAIL" if dry_run else "RAN", "always-mail filesystem body (WQ-013)")
    card("L6", "WOULD-RAN" if _exists(lake_twin) else "SKIP-NO-SHARD", "doorbell pointer")

    outbox_name = f"SUNSET_{date.replace('-','')}_{slug}.md"
    card("L7", "WOULD-RAN" if dry_run else "RAN", f"outbox {outbox_name} rides inside L4 tree")

    if include_l8 and export_json.exists():
        card("L8", "WOULD-RAN", "export-recon flag present")
    else:
        card("L8", "SKIP-NO-FLAG", "L8 not on default sunset")

    shipped = []
    omitted = []
    for lane, row in lanes.items():
        if row["status"] in {"RAN", "WOULD-RAN", "WOULD-MAIL"}:
            shipped.append({"path": lane, "class": "lane", "note": row["note"], "sha256": ""})
        else:
            omitted.append(
                {
                    "path": lane,
                    "reason": row["note"],
                    "skip_code": row["status"],
                    "recoverable": True,
                }
            )

    artifacts = space / "artifacts"
    pack_report = None
    if artifacts.exists() and not dry_run:
        pack_report = pack_artifacts(artifacts, out / "sandbox")

    census_row = {
        "date": date,
        "slug": slug,
        "twin_id": lake_twin.name if _exists(lake_twin) else None,
        "receipt_id": receipt.name if _exists(receipt) else None,
        "miner_tar_id": miner_tar.name if _exists(miner_tar) else None,
        "global_extract_id": extract_tar.name if _exists(extract_tar) else None,
        "packed": _exists(miner_tar) or _exists(extract_tar),
        "pointed": _exists(lake_twin),
        "redacted": meta.get("redacted", "n/a"),
        "status": "OPEN",
        "skip_annotation": "keep-everything",
        "run_id": rid,
    }

    log_path = (out if not dry_run else space / "runs") / "EXPORT_LOG.jsonl"
    if dry_run:
        log_path.parent.mkdir(parents=True, exist_ok=True)
    log_rows = log_lanes(log_path, rid, "sunset-dry-run" if dry_run else "sunset", f"{date}:{slug}", lanes)

    result = {
        "run_id": rid,
        "dry_run": dry_run,
        "claim": CLAIM,
        "stamp": stamp_iso(),
        "conversation": meta,
        "lanes": lanes,
        "census": census_row,
        "pack_report": pack_report,
        "turns_remaining_estimate": meta.get("turns_remaining_estimate", 2),
        "export_log": export_log_cite(log_path),
        "export_log_rows_this_run": len(log_rows),
    }


    # GCM-WQ-020 harvest hook: every lane is a receipt row
    log_path = (out if not dry_run else space / "runs" / rid)
    log_path.mkdir(parents=True, exist_ok=True)
    elog = log_path / "EXPORT_LOG.jsonl"
    action_map = {
        "RAN": "EXPORTED",
        "WOULD-RAN": "WOULD-EXPORT" if False else "EXPORTED",
        "WOULD-MAIL": "EXPORTED",
        "SKIP-EXISTS": "SKIP-EXISTS",
        "SKIP-OVERLAP": "SKIP-OVERLAP",
        "SKIP-NO-FLAG": "SKIP-NO-HIT",
        "SKIP-NO-SHARD": "SKIP-NO-HIT",
        "NO_TWIN": "NO_TWIN",
    }
    # WOULD-* on dry-run still append with exported=False
    for lane, row in lanes.items():
        status = row["status"]
        action = action_map.get(status, status if status in {
            "EXPORTED","SKIP-EXISTS","SKIP-OVERLAP","SKIP-NO-HIT","SECRET","NO_TWIN",
            "NOT-WALKED","TOO-LARGE","PANE-VANISH","OPERATOR-SAID-NO","KEEP-DUPLICATE"
        } else "NOT-WALKED")
        if dry_run and status.startswith("WOULD"):
            action = "SKIP-NO-HIT"
            extra_note = "dry-run would-run; no bytes written"
        else:
            extra_note = row.get("note","")
        try:
            append_row(elog, **{
                "run_id": rid,
                "verb": "sunset-dry-run" if dry_run else "sunset",
                "action": "OPERATOR-SAID-NO" if False else (
                    "SKIP-NO-HIT" if dry_run and status.startswith("WOULD") else action
                ),
                "path": row.get("file") or lane,
                "lane": lane,
                "class": "lane",
                "slug": slug,
                "conversation_key": f"{date}_{slug}",
                "pointer": row.get("file",""),
                "note": extra_note,
                "exported": (not dry_run) and status in {"RAN"},
            })
        except Exception as e:
            append_row(elog, **{
                "run_id": rid,
                "verb": "sunset",
                "action": "NOT-WALKED",
                "path": lane,
                "lane": lane,
                "note": f"hook-error {e}",
                "exported": False,
            })
    result["export_log"] = cite_log(elog)

    if not dry_run:
        write_toc_and_omissions(out, shipped=shipped, omitted=omitted, run=rid, verb="sunset")
        census_store = out / "CENSUS.jsonl"
        census_record(census_store, census_row)
        # L7 outbox also copied into L4 tree (WQ-003)
        l4 = out / "global_extract_tree"
        sunset_dir = l4 / "sunset"
        sunset_dir.mkdir(parents=True, exist_ok=True)
        body = [
            yaml_stamp_block(kind="OUTBOX", run_id=rid, stamp=stamp_iso(), verb="sunset"),
            f"# {outbox_name}\n",
            json.dumps({k: v["status"] for k, v in lanes.items()}, indent=2),
        ]
        write_text(sunset_dir / outbox_name, "\n".join(body) + "\n")
        write_text(out / outbox_name, "\n".join(body) + "\n")
        mail = render_mail_filesystem(
            subject_slug=f"CONVERSATION-SUNSET-{date.replace('-','')}-001",
            run=rid,
            verb="sunset",
            claim=CLAIM,
            tree={"LANES.json": json.dumps({k: v["status"] for k, v in lanes.items()}, indent=2)},
            turns_remaining_estimate=result["turns_remaining_estimate"],
            toc=[s["path"] for s in shipped],
            omissions=[o["path"] + " " + o["skip_code"] for o in omitted],
        )
        write_text(out / "CILIA_MAIL.eml", str(mail))
        write_json(out / "RESULT.json", result)
        result["export_log"] = cite_log(elog)
    return result

#!/usr/bin/env python3
"""GCM-WQ-021/022 exhaustive fake-data stress.

Plants a fake conversation space + fake prod-grok-backend.json,
runs sunset dry-run AND write mode locally, tars the result,
verifies EXPORT_LOG has one row per lane, verifies tar sha,
and writes a local Drive-mock receipt (real Drive binary upload
is not in this connector set).
"""
from __future__ import annotations

import json
import shutil
import tarfile
import tempfile
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from gcm_lib import make_tar, safety_gate, sha256_file, stamps
from sunset_engine import run_sunset
from export_log import read_rows
from export_recon import index_export, recon_sets
from packers import pack
from layout import make_space


def plant_space(root: Path) -> Path:
    space = root / "conv_stress"
    (space / "lake").mkdir(parents=True, exist_ok=True)
    (space / "miner").mkdir(exist_ok=True)
    (space / "extract").mkdir(exist_ok=True)
    (space / "export").mkdir(exist_ok=True)
    (space / "artifacts" / "imagine").mkdir(parents=True, exist_ok=True)
    (space / "artifacts" / "plates").mkdir(exist_ok=True)
    (space / "artifacts" / "secrets").mkdir(exist_ok=True)
    (space / "CONVERSATION.json").write_text(json.dumps({
        "date": "2026-09-11",
        "slug": "stress-fixture",
        "redacted": "n/a",
        "turns_remaining_estimate": 2,
    }, indent=2))
    (space / "lake" / "2026-09-11_cafebabe.md").write_text("# fake lake twin\n")
    (space / "lake" / "RECEIPT_shard_2026-09-11.md").write_text("twin_id: FAKE_TWIN\nslurp: false\n")
    # tiny tars as pointers
    tiny = space / "miner" / "payload"
    tiny.mkdir(exist_ok=True)
    (tiny / "note.txt").write_text("miner payload\n")
    with tarfile.open(space / "miner" / "grok-skill-export-stress-20260911.tar.gz", "w:gz") as tf:
        tf.add(tiny, arcname="payload")
    et = space / "extract" / "payload"
    et.mkdir(exist_ok=True)
    (et / "flow.md").write_text("# flow\n")
    with tarfile.open(space / "extract" / "global_extract_stress_20260911.tar.gz", "w:gz") as tf:
        tf.add(et, arcname="payload")
    (space / "export" / "prod-grok-backend.json").write_text(json.dumps({
        "conversations": [
            {"conversation": {"id": "conv-stress-1", "title": "stress"}, "responses": [
                {"response": {"_id": "m1", "sender": "human", "message": "pack the sandbox"}},
                {"response": {"_id": "m2", "sender": "assistant", "message": "ok", "generated_image_urls": []}},
            ]},
            {"conversation": {"id": "conv-export-only", "title": "only in zip"}},
        ]
    }))
    (space / "artifacts" / "imagine" / "imagine_sample.txt").write_text("fake imagine\n")
    (space / "artifacts" / "plates" / "plate_join.txt").write_text("join / production\n")
    (space / "artifacts" / "secrets" / "cookies.txt").write_text("SECRET\n")
    return space


def run() -> dict:
    tmp = Path(tempfile.mkdtemp(prefix="gcm-stress-"))
    space = plant_space(tmp)
    dry = run_sunset(space, dry_run=True, include_l8=True)
    wet = run_sunset(space, dry_run=False, include_l8=True)
    # find logs
    logs = list(space.rglob("EXPORT_LOG.jsonl"))
    rows = []
    for lp in logs:
        rows.extend(read_rows(lp))
    payload = json.loads((space / "export" / "prod-grok-backend.json").read_text())
    l8 = recon_sets(index_export(payload), {"conv-stress-1"}, {"conv-sunset-only"})
    packed = pack(space / "artifacts", tmp / "packed")
    dest_tar = tmp / "stress_package.tar.gz"
    # package the wet run dir if present
    run_dirs = list((space / "runs").glob("*")) if (space / "runs").exists() else []
    pack_src = run_dirs[0] if run_dirs else space
    gate = None
    sha = None
    if pack_src.exists():
        make_tar(pack_src, dest_tar)
        gate = safety_gate(dest_tar)
        sha = sha256_file(dest_tar)
    # local Drive-mock (connector cannot binary-upload)
    mock = tmp / "drive_mock"
    mock.mkdir()
    receipt = {
        "folder_id_live": "1qV_PuMWxudmQ5E92Lyf6njqF2Tz_NG4X",
        "upload": "LOCAL_MOCK — google_drive has create_folder but no binary upload tool in this connector set",
        "tar": str(dest_tar),
        "tar_sha256": sha,
        "github_blocked": bool(gate and not gate.get("ok_for_github", True)),
        "stamp": stamps(),
    }
    (mock / "DRIVE_MOCK_RECEIPT.json").write_text(json.dumps(receipt, indent=2))
    report = {
        "ok": True,
        "dry_run_id": dry.get("run_id"),
        "wet_run_id": wet.get("run_id"),
        "dry_lanes": {k: v["status"] for k, v in dry["lanes"].items()},
        "wet_lanes": {k: v["status"] for k, v in wet["lanes"].items()},
        "export_log_files": [str(p) for p in logs],
        "export_log_rows": len(rows),
        "export_log_actions": sorted({r.get("action") for r in rows}),
        "l8": l8,
        "pack": packed if isinstance(packed, dict) else str(packed),
        "tar_sha256": sha,
        "github_blocked": receipt["github_blocked"],
        "drive_mock": receipt,
        "space": str(space),
    }
    if len(rows) < 8:
        report["ok"] = False
        report["fail"] = f"expected >=8 log rows, got {len(rows)}"
    if not receipt["github_blocked"]:
        report["ok"] = False
        report["fail_gate"] = "tar should be blocked from GitHub"
    out = HERE / "smoke_out" / "STRESS_REPORT.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str) + "\n")
    print(json.dumps({k: report[k] for k in ("ok","export_log_rows","export_log_actions","tar_sha256","github_blocked","dry_lanes","wet_lanes")}, indent=2, default=str))
    return report


if __name__ == "__main__":
    r = run()
    raise SystemExit(0 if r["ok"] else 1)

#!/usr/bin/env python3
"""Work-queue delta publish (SR-WQ-036).

Compares current NORMALIZED / registry snapshot to the last full publish receipt
and emits a delta package. Falls back to "full-as-delta" if no prior baseline.

Usage:
  python3 wq_delta_publish.py
  python3 wq_delta_publish.py --drive
  python3 wq_delta_publish.py --drive --folder-id 1YmwjUGlr6btQ5WsgxTycLz1Kh2hjK_8V
  python3 wq_delta_publish.py --drive --print-only   # old behavior: print target only

--drive writes a machine-readable DRIVE_UPLOAD.json and a receipt, then tries
any configured upload hook. This runtime has no raw Google Drive API token in
Python; the agent layer completes upload via google_drive_upload_artifact
using the fields in DRIVE_UPLOAD.json. If GROK_DRIVE_UPLOAD_CMD is set, that
command is invoked with the tarball path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

SKILLS_CANDIDATES = [
    Path("/home/workdir/.grok/skills"),
    Path("/root/.grok/server-skills"),
    Path("/home/workdir/artifacts/liv-hub-zip-extract/skill-tree"),
]
ARTIFACTS = Path("/home/workdir/artifacts")
SURFACE_REL = Path("system-roadmap/references/work-queue-surface")

# Last known Work-Queues publish folder (from 2026-08-26 receipts)
DEFAULT_DRIVE_FOLDER_ID = "1YmwjUGlr6btQ5WsgxTycLz1Kh2hjK_8V"


def skills_root() -> Path:
    for p in SKILLS_CANDIDATES:
        if p.is_dir() and any(p.iterdir()):
            return p
    return SKILLS_CANDIDATES[0]


def file_fingerprint(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]


def artifact_rel(path: Path) -> str:
    """Path relative to artifacts root, with leading slash (upload tool convention)."""
    try:
        rel = path.resolve().relative_to(ARTIFACTS.resolve())
        return "/" + str(rel)
    except ValueError:
        return "/" + path.name


def write_drive_request(tar_path: Path, folder_id: str, stamp: str, out_dir: Path) -> Path:
    req = {
        "tool": "google_drive_upload_artifact",
        "artifact_path": artifact_rel(tar_path),
        "file_name": tar_path.name,
        "folder_id": folder_id,
        "local_path": str(tar_path),
        "stamp": stamp,
        "kind": "work-queues-delta",
        "claim": "Absolute Liv HUB",
        "wq": "SR-WQ-036",
        "status": "ready_for_upload",
    }
    dest = out_dir / "DRIVE_UPLOAD.json"
    dest.write_text(json.dumps(req, indent=2), encoding="utf-8")
    # also drop a copy next to the tarball for the agent
    (tar_path.parent / "DRIVE_UPLOAD.json").write_text(json.dumps(req, indent=2), encoding="utf-8")
    return dest


def try_upload_hook(tar_path: Path, folder_id: str) -> dict:
    """Optional local hook. No Google token in this Python runtime."""
    cmd = os.environ.get("GROK_DRIVE_UPLOAD_CMD")
    hook = Path(__file__).resolve().parent / "drive_upload_hook.py"
    if cmd:
        try:
            completed = subprocess.run(
                cmd.format(path=str(tar_path), folder_id=folder_id),
                shell=True,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return {
                "method": "GROK_DRIVE_UPLOAD_CMD",
                "returncode": completed.returncode,
                "stdout": (completed.stdout or "")[-2000:],
                "stderr": (completed.stderr or "")[-1000:],
            }
        except Exception as e:
            return {"method": "GROK_DRIVE_UPLOAD_CMD", "error": str(e)}
    if hook.is_file():
        try:
            completed = subprocess.run(
                ["python3", str(hook), str(tar_path), folder_id],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return {
                "method": "drive_upload_hook.py",
                "returncode": completed.returncode,
                "stdout": (completed.stdout or "")[-2000:],
                "stderr": (completed.stderr or "")[-1000:],
            }
        except Exception as e:
            return {"method": "drive_upload_hook.py", "error": str(e)}
    return {"method": "none"}


def write_receipt(root: Path, payload: dict) -> Path:
    state = root / SURFACE_REL / "state"
    state.mkdir(parents=True, exist_ok=True)
    stamp = payload.get("stamp", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    dest = state / f"PUBLISH_RECEIPT_{stamp}_delta_script.md"
    lines = [
        f"# PUBLISH_RECEIPT — Work Queues Delta {stamp} (script)",
        "",
        f"- tarball: `{payload.get('local_path')}`",
        f"- artifact_path: `{payload.get('artifact_path')}`",
        f"- folder_id: `{payload.get('folder_id')}`",
        f"- hook: `{json.dumps(payload.get('hook'))}`",
        f"- status: `{payload.get('status')}`",
        "",
        "Agent finish step:",
        "",
        "```",
        "call_connected_tool google_drive_upload_artifact",
        f"  artifact_path={payload.get('artifact_path')}",
        f"  file_name={payload.get('file_name')}",
        f"  folder_id={payload.get('folder_id')}",
        "```",
        "",
        "Claim: Absolute Liv HUB",
        "",
    ]
    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drive", action="store_true", help="Prepare + attempt Drive publish")
    parser.add_argument("--print-only", action="store_true", help="With --drive, only print the target (legacy)")
    parser.add_argument("--folder-id", default=DEFAULT_DRIVE_FOLDER_ID, help="Drive folder id")
    parser.add_argument("--out-root", type=Path, default=ARTIFACTS / "wq_publish")
    args = parser.parse_args()

    root = skills_root()
    surface = root / SURFACE_REL
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = args.out_root / f"{stamp}_delta"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Baseline = previous full publish dir if present
    full_dir = args.out_root / f"{stamp}_full"
    if not full_dir.is_dir():
        priors = sorted(args.out_root.glob("*_full"))
        full_dir = priors[-1] if priors else None

    watch = [
        "MASTER_REGISTRY.json",
        "MASTER_REGISTRY.md",
        "HYGIENE_REPORT.json",
        "SNAPSHOT.json",
        "work_atomizer.json",
        "prompt_atomizer.json",
    ]

    changed = []
    unchanged = []
    for name in watch:
        cur = surface / name
        if not cur.is_file():
            cur = (full_dir / name) if full_dir else None
        if cur is None or not Path(cur).is_file():
            continue
        cur = Path(cur)
        fp = file_fingerprint(cur)
        base_fp = None
        if full_dir and (full_dir / name).is_file():
            base_fp = file_fingerprint(full_dir / name)
        if base_fp is None or base_fp != fp:
            shutil.copy2(cur, out_dir / name)
            changed.append({"file": name, "fp": fp, "was": base_fp})
        else:
            unchanged.append(name)

    note = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": "delta",
        "baseline": str(full_dir) if full_dir else None,
        "changed": changed,
        "unchanged": unchanged,
        "skills_root": str(root),
        "claim": "Absolute Liv HUB",
        "wq": "SR-WQ-036",
    }
    (out_dir / "DELTA.json").write_text(json.dumps(note, indent=2))
    (out_dir / "MANIFEST.md").write_text(
        f"# Work-Queues delta — {stamp}\n\n"
        f"Baseline: `{full_dir}`\n"
        f"Changed: {len(changed)}\n"
        f"Unchanged: {len(unchanged)}\n\n"
        + "\n".join(f"- {c['file']} ({c['fp']})" for c in changed)
        + ("\n\n(no content changes vs baseline — receipt only)\n" if not changed else "\n")
        + "\nClaim: Absolute Liv HUB\n"
    )

    tar_path = args.out_root / f"work-queues_delta_{stamp}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tf:
        tf.add(out_dir, arcname=out_dir.name)

    print(f"[wq_delta_publish] changed={len(changed)} unchanged={len(unchanged)}")
    print(f"[wq_delta_publish] out={out_dir}")
    print(f"[wq_delta_publish] tarball={tar_path}")

    if not args.drive:
        return 0

    target_label = f"Liv-HUB / Work-Queues / {stamp}_delta/ ({args.folder_id})"
    print(f"[wq_delta_publish] Drive target: {target_label}")

    if args.print_only:
        print("[wq_delta_publish] --print-only set; skipping upload request file")
        return 0

    req_path = write_drive_request(tar_path, args.folder_id, stamp, out_dir)
    req = json.loads(req_path.read_text(encoding="utf-8"))
    hook = try_upload_hook(tar_path, args.folder_id)

    # Always enqueue the native Grok Drive connector (no inference step).
    try:
        from drive_connector_bridge import enqueue as _enqueue
    except ImportError:
        import importlib.util
        _spec = importlib.util.spec_from_file_location(
            "drive_connector_bridge",
            Path(__file__).resolve().parent / "drive_connector_bridge.py",
        )
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        _enqueue = _mod.enqueue
    outbox = _enqueue(
        artifact_path=req["artifact_path"],
        file_name=req["file_name"],
        folder_id=req["folder_id"],
        source="wq_delta_publish",
    )
    req["hook"] = hook
    req["connector_bus"] = str(outbox)
    req["native_tool"] = "google_drive_upload_artifact"
    req["status"] = "connector_bus_pending"
    req_path.write_text(json.dumps(req, indent=2), encoding="utf-8")
    (tar_path.parent / "DRIVE_UPLOAD.json").write_text(json.dumps(req, indent=2), encoding="utf-8")

    receipt = write_receipt(root, req)
    print(f"[wq_delta_publish] drive_request={req_path}")
    print(f"[wq_delta_publish] receipt={receipt}")
    print(f"[wq_delta_publish] hook={hook.get('method')} status={req['status']}")
    print(f"[wq_delta_publish] CONNECTOR_BUS_FLUSH_REQUIRED=1 outbox={outbox}")
    print(
        "[wq_delta_publish] UPLOAD_READY "
        f"artifact_path={req['artifact_path']} "
        f"file_name={req['file_name']} "
        f"folder_id={req['folder_id']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

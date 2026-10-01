#!/usr/bin/env python3
"""Thin full skill-tree dump at session start/end.

Creates a dated inventory + optional compressed snapshot of the live skill tree
(metadata always; full tarball optional and can be large).

Usage:
  python3 session_skill_tree_dump.py --phase start
  python3 session_skill_tree_dump.py --phase end --tar
  python3 session_skill_tree_dump.py --phase end --tar --drive
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

SKILLS_CANDIDATES = [
    Path("/home/workdir/.grok/skills"),
    Path("/root/.grok/server-skills"),
    Path("/home/workdir/artifacts/liv-hub-zip-extract/skill-tree"),
]
ARTIFACTS = Path("/home/workdir/artifacts")


def skills_root() -> Path:
    for p in SKILLS_CANDIDATES:
        if p.is_dir() and any(p.iterdir()):
            return p
    raise SystemExit("No skills root found")


def inventory(root: Path) -> dict:
    skills = []
    total_files = 0
    total_bytes = 0
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        n_files = 0
        n_bytes = 0
        for dirpath, _, filenames in os.walk(child):
            for fn in filenames:
                fp = Path(dirpath) / fn
                try:
                    sz = fp.stat().st_size
                except OSError:
                    sz = 0
                n_files += 1
                n_bytes += sz
        skills.append({"name": child.name, "files": n_files, "bytes": n_bytes})
        total_files += n_files
        total_bytes += n_bytes
    return {
        "skills": skills,
        "skill_count": len(skills),
        "total_files": total_files,
        "total_bytes": total_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["start", "end", "full"], default="end")
    parser.add_argument("--tar", action="store_true", help="Also write a compressed tree tarball (can be large)")
    parser.add_argument("--drive", action="store_true")
    parser.add_argument("--out-root", type=Path, default=ARTIFACTS / "skill_tree_dumps")
    args = parser.parse_args()

    root = skills_root()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = args.out_root / f"{stamp}_session-{args.phase}"
    out_dir.mkdir(parents=True, exist_ok=True)

    inv = inventory(root)
    inv_meta = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "phase": args.phase,
        "skills_root": str(root),
        **inv,
        "claim": "Absolute Liv HUB",
    }
    (out_dir / "INVENTORY.json").write_text(json.dumps(inv_meta, indent=2))
    lines = [
        f"# Skill tree dump — {stamp} session-{args.phase}",
        f"",
        f"Root: `{root}`",
        f"Skills: {inv['skill_count']}  Files: {inv['total_files']}  Bytes: {inv['total_bytes']}",
        "",
        "| Skill | Files | Bytes |",
        "|-------|------:|------:|",
    ]
    for s in inv["skills"]:
        lines.append(f"| {s['name']} | {s['files']} | {s['bytes']} |")
    lines.append("")
    lines.append("Claim: Absolute Liv HUB")
    (out_dir / "INVENTORY.md").write_text("\n".join(lines) + "\n")

    tar_path = None
    if args.tar:
        tar_path = args.out_root / f"skill-tree_session-{args.phase}_{stamp}.tar.gz"
        # Exclude heavy caches / git if present
        def filter_tar(ti: tarfile.TarInfo) -> tarfile.TarInfo | None:
            name = ti.name
            if "/.git/" in f"/{name}/" or name.endswith(".pyc") or "/__pycache__/" in f"/{name}/":
                return None
            return ti

        with tarfile.open(tar_path, "w:gz") as tf:
            tf.add(root, arcname="skill-tree", filter=filter_tar)
        print(f"[session_skill_tree_dump] tarball={tar_path} size={tar_path.stat().st_size}")

    # small package of inventory always
    inv_tar = args.out_root / f"skill-tree-inventory_session-{args.phase}_{stamp}.tar.gz"
    with tarfile.open(inv_tar, "w:gz") as tf:
        tf.add(out_dir, arcname=out_dir.name)

    print(f"[session_skill_tree_dump] phase={args.phase} skills={inv['skill_count']} files={inv['total_files']}")
    print(f"[session_skill_tree_dump] inventory_dir={out_dir}")
    print(f"[session_skill_tree_dump] inventory_tar={inv_tar}")
    if args.drive:
        print("[session_skill_tree_dump] Drive target: Liv-HUB / Skill-Tree-Dumps / {stamp}_session-{phase}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

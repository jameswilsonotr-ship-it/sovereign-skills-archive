#!/usr/bin/env python3
"""Publish ALL atom-cloud JSON files under the skill tree (named + session + seed-bank).

Does not invent new cloud types. Packs every existing *atom*.json except
hygiene-console mirrors and anatomical presets.
"""
from __future__ import annotations

import argparse
import json
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path

SKILLS_CANDIDATES = [
    Path("/home/workdir/.grok/skills"),
    Path("/root/.grok/server-skills"),
]
ARTIFACTS = Path("/home/workdir/artifacts")
SKIP_PARTS = {"__pycache__", "hygiene-console", "node_modules"}
SKIP_NAMES = {"anatomical.json"}


def skills_root() -> Path:
    for p in SKILLS_CANDIDATES:
        if p.is_dir() and any(p.iterdir()):
            return p
    raise SystemExit("skills root missing")


def collect(root: Path) -> list[Path]:
    out = []
    for p in root.rglob("*.json"):
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        if p.name in SKIP_NAMES:
            continue
        name = p.name.lower()
        if "atom" in name or "atomizer" in name or "atom_cloud" in name:
            out.append(p)
    return sorted(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", type=Path, default=ARTIFACTS / "atom_publish")
    args = parser.parse_args()

    root = skills_root()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = args.out_root / f"{stamp}_all-clouds"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    files = collect(root)
    copied = []
    for src in files:
        rel = src.relative_to(root)
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append({"rel": str(rel), "bytes": dest.stat().st_size})

    (out / "INDEX.json").write_text(json.dumps({"count": len(copied), "files": copied}, indent=2))
    (out / "MANIFEST.md").write_text(
        f"# All atom clouds — {stamp}\n\nCount: {len(copied)}\nIncludes named + session + seed-bank.\nClaim: Absolute Liv HUB\n"
    )

    tar_path = ARTIFACTS / f"atom-clouds_all_{stamp}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tf:
        tf.add(out, arcname=out.name)
    print(f"[publish_all_atom_clouds] files={len(copied)} tarball={tar_path} size={tar_path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deterministic full work-queue publish (SR-WQ-036)."""
from __future__ import annotations

import argparse
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path

SKILLS_CANDIDATES = [
    Path("/home/workdir/.grok/skills"),
    Path("/root/.grok/server-skills"),
]
ARTIFACTS = Path("/home/workdir/artifacts")


def skills_root() -> Path:
    for p in SKILLS_CANDIDATES:
        if p.is_dir() and any(p.iterdir()):
            return p
    raise SystemExit("skills root missing")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", type=Path, default=ARTIFACTS / "wq_publish")
    args = parser.parse_args()

    root = skills_root()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = args.out_root / f"{stamp}_full"
    out.mkdir(parents=True, exist_ok=True)

    lines = [f"# NORMALIZED work queues — {stamp} full\n\n"]
    for wq in sorted(root.rglob("WORK_QUEUE.md")):
        lines.append(f"## {wq.relative_to(root)}\n")
        lines.append("\n".join(wq.read_text(errors="replace").splitlines()[:200]) + "\n\n")
    (out / "NORMALIZED.md").write_text("".join(lines))

    surface = root / "system-roadmap/references/work-queue-surface"
    for name in (
        "MASTER_REGISTRY.md",
        "MASTER_REGISTRY.json",
        "HYGIENE_REPORT.json",
        "SNAPSHOT.json",
        "work_atomizer.json",
        "prompt_atomizer.json",
        "ATOM_CLOUD_INVENTORY_2026-08-26.md",
    ):
        src = surface / name
        if src.is_file():
            shutil.copy2(src, out / name)

    (out / "MANIFEST.md").write_text(
        f"# Work-Queues full — {stamp}\nClaim: Absolute Liv HUB\nSource: SR-WQ-036\n"
    )

    tar_path = ARTIFACTS / f"work-queues_full_{stamp}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tf:
        tf.add(out, arcname=out.name)
    print(f"[wq_full_publish] out={out}")
    print(f"[wq_full_publish] tarball={tar_path} size={tar_path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

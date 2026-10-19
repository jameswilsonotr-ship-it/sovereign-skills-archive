#!/usr/bin/env python3
"""Thin session atom-cloud dump (SR-WQ-043).

Copies active atom clouds to a dated local package and optionally uploads to Drive.
Intended for session-start and session-end hooks.

Usage:
  python3 session_atom_dump.py --phase start
  python3 session_atom_dump.py --phase end
  python3 session_atom_dump.py --phase end --drive
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
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
    return SKILLS_CANDIDATES[0]


def collect_atom_sources(root: Path) -> list[tuple[str, Path]]:
    """Return (label, path) for every atom cloud file we can find."""
    found: list[tuple[str, Path]] = []
    candidates = [
        (ARTIFACTS / "memory_atomizer.json", "memory_atomizer"),
        (ARTIFACTS / "skill_surface_atomizer.json", "skill_surface_atomizer"),
        (root / "chaos-bratz-roster/data/atom_clouds/canonical/memory_atomizer.json", "memory_atomizer_canonical"),
        (root / "chaos-bratz-roster/data/atom_clouds/canonical/skill_surface_atomizer.json", "skill_surface_atomizer_canonical"),
        (root / "system-roadmap/references/work-queue-surface/work_atomizer.json", "work_atomizer"),
        (root / "system-roadmap/references/work-queue-surface/prompt_atomizer.json", "prompt_atomizer"),
        (root / "claim-runtime/references/modules/curator/atoms/curator_atom_cloud.json", "curator_atom_cloud"),
    ]
    seen: set[str] = set()
    for path, label in candidates:
        if path.is_file() and label not in seen:
            found.append((label, path))
            seen.add(label)
    # opportunistic: atomizer + atom_cloud JSON anywhere on the skill surface
    if root.is_dir():
        for path in root.rglob("*.json"):
            name = path.name.lower()
            if not path.is_file():
                continue
            if "atomizer" in name or "atom_cloud" in name or "atom-cloud" in name:
                label = path.stem
                key = str(path)
                if key not in seen and label not in seen:
                    found.append((label, path))
                    seen.add(key)
                    seen.add(label)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="Session atom-cloud dump")
    parser.add_argument("--phase", choices=["start", "end", "full"], default="end")
    parser.add_argument("--drive", action="store_true", help="Print Drive upload instructions (connector does actual upload)")
    parser.add_argument("--out-root", type=Path, default=ARTIFACTS / "atom_publish")
    args = parser.parse_args()

    root = skills_root()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    phase = args.phase
    out_dir = args.out_root / f"{stamp}_session-{phase}"
    out_dir.mkdir(parents=True, exist_ok=True)

    sources = collect_atom_sources(root)
    copied = []
    for label, path in sources:
        dest = out_dir / f"{label}.json"
        try:
            shutil.copy2(path, dest)
            copied.append({"label": label, "src": str(path), "bytes": dest.stat().st_size})
        except Exception as e:
            copied.append({"label": label, "src": str(path), "error": str(e)})

    receipt = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "phase": phase,
        "skills_root": str(root),
        "out_dir": str(out_dir),
        "files": copied,
        "claim": "Absolute Liv HUB",
        "wq": "SR-WQ-043",
    }
    (out_dir / "RECEIPT.json").write_text(json.dumps(receipt, indent=2))
    (out_dir / "MANIFEST.md").write_text(
        f"# Atom dump — {stamp} session-{phase}\n\n"
        f"Files: {len(copied)}\n"
        f"Skills root: `{root}`\n\n"
        + "\n".join(f"- {c.get('label')}: {c.get('bytes', c.get('error'))}" for c in copied)
        + "\n\nClaim: Absolute Liv HUB\n"
    )

    # local tarball
    tar_path = args.out_root / f"atom-clouds_session-{phase}_{stamp}.tar.gz"
    import tarfile

    with tarfile.open(tar_path, "w:gz") as tf:
        tf.add(out_dir, arcname=out_dir.name)

    print(f"[session_atom_dump] phase={phase} files={len(copied)} out={out_dir}")
    print(f"[session_atom_dump] tarball={tar_path}")
    if args.drive:
        print("[session_atom_dump] Drive target: Liv-HUB / Atom-Clouds / {stamp}_session-{phase}/")
        print(f"[session_atom_dump] Upload candidate: {tar_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

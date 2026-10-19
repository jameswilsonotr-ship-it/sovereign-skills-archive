#!/usr/bin/env python3
"""workspace_index.py — kill the every-turn `find` + bash inventory.

Writes a JSON index of artifacts + skill scripts so the next agent
does not spend 45s thinking about `ls -la`.

Usage:
  python3 workspace_index.py
  python3 workspace_index.py --print
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

SKILLS = Path("/home/workdir/.grok/skills")
ARTIFACTS = Path("/home/workdir/artifacts")
OUT = ARTIFACTS / "WORKSPACE_INDEX.json"
SKIP = {".git", "__pycache__", "node_modules", ".venv", "venv", "tarballs"}


def walk_files(root: Path, limit_ext: set[str] | None = None) -> list[dict]:
    rows = []
    if not root.exists():
        return rows
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for name in filenames:
            p = Path(dirpath) / name
            if limit_ext and p.suffix.lower() not in limit_ext:
                continue
            try:
                rel = str(p.relative_to(root))
            except ValueError:
                rel = str(p)
            rows.append({"rel": rel.replace("\\", "/"), "bytes": p.stat().st_size, "ext": p.suffix.lower()})
    rows.sort(key=lambda r: r["rel"])
    return rows


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", action="store_true")
    args = ap.parse_args()
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "artifacts": walk_files(ARTIFACTS),
        "skill_scripts": walk_files(SKILLS, {".py", ".sh"}),
        "counts": {},
    }
    payload["counts"] = {
        "artifacts": len(payload["artifacts"]),
        "skill_scripts": len(payload["skill_scripts"]),
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"WROTE {OUT} artifacts={payload['counts']['artifacts']} scripts={payload['counts']['skill_scripts']}")
    if args.print:
        print(json.dumps(payload["counts"], indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""SR-WQ-038c — Work Atom Cloud. Additive index of every work-queue item."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from wq_hygiene_lib import atomize_work, skills_root, surface_dir, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status")
    parser.add_argument("--owner")
    parser.add_argument("--skill")
    parser.add_argument("--query")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = skills_root()
    cloud = atomize_work(root)
    out = surface_dir(root) / "work_atomizer.json"
    write_json(out, cloud)
    artifacts = Path("/home/workdir/artifacts")
    if artifacts.is_dir():
        write_json(artifacts / "work_atomizer.json", cloud)
    atoms = cloud["atoms"]
    if args.status:
        atoms = [a for a in atoms if args.status.lower() in str(a.get("status") or "").lower()]
    if args.owner:
        atoms = [a for a in atoms if args.owner.lower() in str(a.get("owner") or "").lower()]
    if args.skill:
        atoms = [a for a in atoms if args.skill.lower() in str(a.get("skill") or "").lower()]
    if args.query:
        q = args.query.lower()
        atoms = [
            a
            for a in atoms
            if q in json.dumps(a, ensure_ascii=False).lower()
        ]
    print(f"cloud=work count={cloud['count']} filtered={len(atoms)} wrote={out}")
    if args.json:
        print(json.dumps(atoms, indent=2, ensure_ascii=False))
    else:
        for a in atoms[:30]:
            print(f"{a['id']:22}  {(a.get('status') or '')[:18]:18}  {a.get('skill')}  {a.get('title','')[:60]}")
        if len(atoms) > 30:
            print(f"… {len(atoms) - 30} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())

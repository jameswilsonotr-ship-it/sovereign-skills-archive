#!/usr/bin/env python3
"""SR-WQ-038d — System-Prompt Atom Cloud over CURRENT + dated history."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from wq_hygiene_lib import atomize_prompts, skills_root, surface_dir, write_json


def in_range(atom: dict, since: str | None, until: str | None) -> bool:
    start = atom.get("valid_from") or "0000-01-01"
    end = atom.get("valid_until") or "9999-12-31"
    if since and end < since:
        return False
    if until and start > until:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", help="YYYY-MM-DD inclusive")
    parser.add_argument("--until", help="YYYY-MM-DD inclusive")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = skills_root()
    cloud = atomize_prompts(root)
    out = surface_dir(root) / "prompt_atomizer.json"
    write_json(out, cloud)
    artifacts = Path("/home/workdir/artifacts")
    if artifacts.is_dir():
        write_json(artifacts / "prompt_atomizer.json", cloud)
    atoms = cloud["atoms"]
    if args.since or args.until:
        atoms = [a for a in atoms if in_range(a, args.since, args.until)]
    print(f"cloud=system_prompt count={cloud['count']} filtered={len(atoms)} wrote={out}")
    if args.json:
        print(json.dumps(atoms, indent=2, ensure_ascii=False))
    else:
        for a in atoms:
            print(
                f"{a.get('role','?'):8}  {a.get('valid_from') or '—'} → {a.get('valid_until') or 'CURRENT'}  {a.get('path')}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""SR-WQ-038e — deterministic work-queue mutation wrapper.

Every item change should go through this script so a flag is emitted and
the work atom cloud slice is regenerated.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from wq_hygiene_lib import (
    atomize_work,
    dump_frontmatter,
    extract_item_file_meta,
    now_iso,
    parse_frontmatter,
    skills_root,
    surface_dir,
    write_flag,
    write_json,
)


def find_item_file(root: Path, item_id: str) -> Path | None:
    matches = list(root.glob(f"**/work-queue*/items/{item_id}_*.md")) + list(
        root.glob(f"**/work-queue/items/{item_id}_*.md")
    )
    # also exact stem starts
    extra = []
    for p in root.glob("**/work-queue*/items/*.md"):
        if p.name.startswith(item_id + "_") or p.stem == item_id:
            extra.append(p)
    allp = list({*matches, *extra})
    return allp[0] if allp else None


def apply_set(path: Path, key: str, value: str) -> None:
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if not fm:
        meta = extract_item_file_meta(path)
        fm = {
            "id": meta.get("id"),
            "owner": meta.get("owner"),
            "status": meta.get("status"),
            "opened": meta.get("opened") or now_iso()[:10],
            "depends_on": meta.get("depends_on") or [],
            "blocks": meta.get("blocks") or [],
            "active_prompt_version": meta.get("active_prompt_version"),
            "last_touched": now_iso(),
            "parent": meta.get("parent"),
            "claim": "Absolute Liv HUB",
        }
    if key == "depends_on" or key == "blocks":
        fm[key] = [v.strip() for v in value.split(",") if v.strip()]
    else:
        fm[key] = value
    fm["last_touched"] = now_iso()
    path.write_text(dump_frontmatter(fm) + (body if body.endswith("\n") else body + "\n"), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"), action="append", default=[])
    parser.add_argument("--source", default="wq_edit")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    root = skills_root()
    path = find_item_file(root, args.id)
    if path is None:
        print(f"ERROR: no item file for {args.id}")
        return 2
    if not args.set:
        print(f"found {path} (no --set; dry locate)")
        return 0
    for key, value in args.set:
        apply_set(path, key, value)
        print(f"set {args.id}.{key} = {value}")
    flag = write_flag([args.id], source=args.source, notes=args.notes or f"edited {args.id}", root=root)
    cloud = atomize_work(root)
    write_json(surface_dir(root) / "work_atomizer.json", cloud)
    print(f"flag {flag}")
    print(f"regenerated work atom cloud ({cloud['count']} atoms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""SR-WQ-042 — system-wide bidirectional depends_on ↔ blocks hygiene.

Scans every work-queue item across the skill tree, reports:
  - orphan depends_on / blocks (target missing)
  - missing reverse links
  - parent field vs depends_on consistency

Optional --fix writes missing reverse links into item-file frontmatter
(only for items that have a real item file with frontmatter).

Usage:
  python3 wq_bidir.py              # report only
  python3 wq_bidir.py --fix       # repair missing reverse links where possible
  python3 wq_bidir.py --json       # print full JSON report
  python3 wq_bidir.py --strict     # treat link problems as errors (exit 1)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from wq_hygiene_lib import (
    collect_all_items,
    dump_frontmatter,
    merge_items,
    now_iso,
    parse_frontmatter,
    skills_root,
    surface_dir,
    write_json,
)


def _as_list(val: Any) -> list[str]:
    if val is None or val == "" or val == "null":
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    if isinstance(val, str):
        s = val.strip()
        if s.startswith("[") and s.endswith("]"):
            inner = s[1:-1].strip()
            if not inner:
                return []
            return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
        return [s]
    return [str(val)]


def load_item_file(path: Path) -> tuple[dict[str, Any], str] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    fm, body = parse_frontmatter(text)
    if not fm:
        return None
    return fm, body


def write_item_file(path: Path, fm: dict[str, Any], body: str) -> None:
    fm = dict(fm)
    fm["last_touched"] = now_iso()
    # normalize list fields
    for key in ("depends_on", "blocks"):
        if key in fm:
            fm[key] = _as_list(fm.get(key))
    text = dump_frontmatter(fm) + body.lstrip("\n")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def find_item_path(root: Path, item_id: str) -> Path | None:
    matches = list(root.glob(f"**/work-queue*/items/{item_id}_*.md"))
    matches += list(root.glob(f"**/work-queue/items/{item_id}_*.md"))
    matches += list(root.glob(f"**/work-queue*/items/{item_id}.md"))
    # prefer exact id prefix match
    exact = [p for p in matches if p.stem == item_id or p.stem.startswith(item_id + "_")]
    pool = exact or matches
    return pool[0] if pool else None


def scan(root: Path | None = None) -> dict[str, Any]:
    root = root or skills_root()
    table, files = collect_all_items(root)
    merged = merge_items(table, files)
    by_id: dict[str, dict[str, Any]] = {}
    for it in merged:
        iid = it.get("id")
        if not iid:
            continue
        # normalize lists
        it = dict(it)
        it["depends_on"] = _as_list(it.get("depends_on"))
        it["blocks"] = _as_list(it.get("blocks"))
        by_id[iid] = it

    issues: list[dict[str, str]] = []
    edges_depends = 0
    edges_blocks = 0

    for iid, it in sorted(by_id.items()):
        for dep in it["depends_on"]:
            edges_depends += 1
            if dep not in by_id:
                issues.append(
                    {
                        "level": "error",
                        "code": "orphan_depends_on",
                        "from": iid,
                        "to": dep,
                        "msg": f"{iid} depends_on missing {dep}",
                    }
                )
            elif iid not in _as_list(by_id[dep].get("blocks")):
                issues.append(
                    {
                        "level": "warn",
                        "code": "missing_reverse_blocks",
                        "from": iid,
                        "to": dep,
                        "msg": f"{iid} → {dep} has no reverse blocks link",
                    }
                )
        for blk in it["blocks"]:
            edges_blocks += 1
            if blk not in by_id:
                issues.append(
                    {
                        "level": "error",
                        "code": "orphan_blocks",
                        "from": iid,
                        "to": blk,
                        "msg": f"{iid} blocks missing {blk}",
                    }
                )
            elif iid not in _as_list(by_id[blk].get("depends_on")):
                issues.append(
                    {
                        "level": "warn",
                        "code": "missing_reverse_depends_on",
                        "from": iid,
                        "to": blk,
                        "msg": f"{iid} blocks {blk} but {blk} does not list depends_on {iid}",
                    }
                )
        # parent consistency (informational)
        parent = it.get("parent")
        if parent and parent not in ("null", "", None):
            parent = str(parent).strip()
            if parent not in by_id:
                issues.append(
                    {
                        "level": "warn",
                        "code": "orphan_parent",
                        "from": iid,
                        "to": parent,
                        "msg": f"{iid} parent={parent} not found as item",
                    }
                )
            elif parent not in it["depends_on"]:
                issues.append(
                    {
                        "level": "info",
                        "code": "parent_not_in_depends_on",
                        "from": iid,
                        "to": parent,
                        "msg": f"{iid} has parent={parent} but parent not in depends_on",
                    }
                )

    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    infos = [i for i in issues if i["level"] == "info"]

    return {
        "generated": now_iso(),
        "item_count": len(by_id),
        "edges_depends_on": edges_depends,
        "edges_blocks": edges_blocks,
        "ok": len(errors) == 0,
        "error_count": len(errors),
        "warn_count": len(warns),
        "info_count": len(infos),
        "issues": issues,
        "ids_with_links": sorted(
            iid
            for iid, it in by_id.items()
            if it["depends_on"] or it["blocks"]
        ),
    }


def fix_missing_reverses(root: Path, report: dict[str, Any]) -> dict[str, Any]:
    """Add missing reverse links into item-file frontmatter where possible."""
    fixed: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []

    for issue in report["issues"]:
        if issue["code"] not in ("missing_reverse_blocks", "missing_reverse_depends_on"):
            continue
        # missing_reverse_blocks: from depends_on to → need to add from into to.blocks
        # missing_reverse_depends_on: from blocks to → need to add from into to.depends_on
        target_id = issue["to"]
        source_id = issue["from"]
        path = find_item_path(root, target_id)
        if not path:
            skipped.append({"id": target_id, "reason": "no item file", "issue": issue["code"]})
            continue
        loaded = load_item_file(path)
        if not loaded:
            skipped.append({"id": target_id, "reason": "no frontmatter", "issue": issue["code"]})
            continue
        fm, body = loaded
        if issue["code"] == "missing_reverse_blocks":
            blocks = _as_list(fm.get("blocks"))
            if source_id not in blocks:
                blocks.append(source_id)
                fm["blocks"] = blocks
                write_item_file(path, fm, body)
                fixed.append({"id": target_id, "added_blocks": source_id, "path": str(path)})
        else:  # missing_reverse_depends_on
            deps = _as_list(fm.get("depends_on"))
            if source_id not in deps:
                deps.append(source_id)
                fm["depends_on"] = deps
                write_item_file(path, fm, body)
                fixed.append({"id": target_id, "added_depends_on": source_id, "path": str(path)})

    return {"fixed": fixed, "skipped": skipped, "fixed_count": len(fixed), "skipped_count": len(skipped)}


def main() -> int:
    parser = argparse.ArgumentParser(description="System-wide bidirectional link hygiene (SR-WQ-042)")
    parser.add_argument("--fix", action="store_true", help="Write missing reverse links into item files")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any error-level issue")
    args = parser.parse_args()

    root = skills_root()
    report = scan(root)

    fix_result = None
    if args.fix:
        fix_result = fix_missing_reverses(root, report)
        # re-scan after fix
        report = scan(root)
        report["fix"] = fix_result

    out = surface_dir(root) / "BIDIR_REPORT.json"
    write_json(out, report)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(
            f"bidir items={report['item_count']} "
            f"depends_edges={report['edges_depends_on']} blocks_edges={report['edges_blocks']} "
            f"ok={report['ok']} errors={report['error_count']} warns={report['warn_count']} "
            f"info={report['info_count']}"
        )
        if report["ids_with_links"]:
            print(f"ids_with_links ({len(report['ids_with_links'])}): {', '.join(report['ids_with_links'][:20])}"
                  + (" …" if len(report["ids_with_links"]) > 20 else ""))
        for issue in report["issues"][:30]:
            print(f"  [{issue['level']}] {issue['code']}: {issue['msg']}")
        if len(report["issues"]) > 30:
            print(f"  … {len(report['issues']) - 30} more")
        if fix_result is not None:
            print(f"fix: fixed={fix_result['fixed_count']} skipped={fix_result['skipped_count']}")
        print(f"wrote {out}")

    if args.strict and report["error_count"]:
        return 1
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

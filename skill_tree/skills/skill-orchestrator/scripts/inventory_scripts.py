#!/usr/bin/env python3
"""
inventory_scripts.py — Scan the entire skills tree for scripts and maintain
references/inventory/scripts/ (markdown + json + registry).

Usage:
  python3 inventory_scripts.py
  python3 inventory_scripts.py --print
"""
from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
OUT_DIR = Path(__file__).resolve().parents[1] / "references" / "inventory" / "scripts"
SCRIPT_EXTS = {".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".ts", ".rb", ".pl"}
SKIP_DIR_NAMES = {".git", "__pycache__", "node_modules", ".venv", "venv", "tarballs"}


def is_script(path: Path) -> bool:
    if path.suffix.lower() in SCRIPT_EXTS:
        return True
    if path.is_file() and os.access(path, os.X_OK) and path.suffix == "":
        try:
            with path.open("rb") as f:
                return f.read(2) == b"#!"
        except OSError:
            return False
    return False


def scan() -> list[dict]:
    rows = []
    for dirpath, dirnames, filenames in os.walk(SKILLS_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            p = Path(dirpath) / name
            if not is_script(p):
                continue
            try:
                rel = p.relative_to(SKILLS_ROOT)
            except ValueError:
                continue
            parts = rel.parts
            skill = parts[0] if parts else "?"
            module = None
            if "modules" in parts:
                i = parts.index("modules")
                if i + 1 < len(parts):
                    module = parts[i + 1]
            rows.append(
                {
                    "skill": skill,
                    "module": module,
                    "relpath": str(rel).replace("\\", "/"),
                    "name": name,
                    "ext": p.suffix.lower() or "(none)",
                    "bytes": p.stat().st_size,
                    "executable": os.access(p, os.X_OK),
                }
            )
    rows.sort(key=lambda r: (r["skill"], r["module"] or "", r["relpath"]))
    return rows


def write_inventory(rows: list[dict], ts: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_skill: dict[str, list] = defaultdict(list)
    for r in rows:
        by_skill[r["skill"]].append(r)

    md_path = OUT_DIR / "SCRIPTS_INVENTORY.md"
    lines = [
        "---",
        "name: scripts-inventory",
        "type: scripts-inventory",
        f"generated: {ts}",
        "generator: skill-orchestrator/scripts/inventory_scripts.py",
        "version: 1.0.0",
        "---",
        "",
        "# Scripts inventory — entire skills tree",
        f"**Generated**: {ts}",
        f"**Generator**: skill-orchestrator/scripts/inventory_scripts.py",
        f"**Total scripts**: {len(rows)}",
        f"**Skills with scripts**: {len(by_skill)}",
        "",
        "## By skill",
        "",
    ]
    for skill in sorted(by_skill.keys()):
        items = by_skill[skill]
        lines.append(f"### {skill} ({len(items)})")
        lines.append("")
        lines.append("| Path | Ext | Bytes | Exec | Module |")
        lines.append("|------|-----|------:|:----:|--------|")
        for r in items:
            lines.append(
                f"| `{r['relpath']}` | {r['ext']} | {r['bytes']} | "
                f"{'Y' if r['executable'] else ''} | {r['module'] or ''} |"
            )
        lines.append("")
    lines.append("## Flat list")
    lines.append("")
    for r in rows:
        lines.append(f"- `{r['relpath']}`")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    json_path = OUT_DIR / "scripts_inventory.json"
    payload = {
        "generated": ts,
        "skills_root": str(SKILLS_ROOT),
        "total": len(rows),
        "skills_with_scripts": len(by_skill),
        "scripts": rows,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return md_path


def refresh_registry(ts: str) -> Path:
    """Record all entries in inventory/scripts/."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for p in sorted(OUT_DIR.iterdir()):
        if not p.is_file():
            continue
        name = p.name
        if name == "REGISTRY.md":
            typ = "registry"
        elif name == "PROTOCOL.md":
            typ = "protocol"
        elif name == "SCHEMA.md":
            typ = "schema"
        elif name.endswith(".json"):
            typ = "json-companion"
        elif "INVENTORY" in name.upper() or name.startswith("SCRIPTS"):
            typ = "scripts-inventory"
        else:
            typ = "note"
        entries.append(
            {
                "filename": name,
                "type": typ,
                "bytes": p.stat().st_size if name != "REGISTRY.md" else 0,
                "notes": "",
            }
        )

    lines = [
        "---",
        "name: registry",
        "type: registry",
        f"generated: {ts}",
        "generator: skill-orchestrator/scripts/inventory_scripts.py",
        "version: 1.0.0",
        "---",
        "",
        "# Registry — inventory/scripts",
        f"**Generated**: {ts}",
        "",
        "All entries in `skill-orchestrator/references/inventory/scripts/`.",
        "",
        "| Filename | Type | Bytes | Notes |",
        "|----------|------|------:|-------|",
    ]
    for e in entries:
        if e["filename"] == "REGISTRY.md":
            continue
        lines.append(f"| `{e['filename']}` | {e['type']} | {e['bytes']} | {e['notes']} |")
    lines.append("| `REGISTRY.md` | registry | (this file) | Index of folder |")
    lines.append("")
    lines.append("## How to update")
    lines.append("1. `python3 scripts/inventory_scripts.py --print`")
    lines.append("2. Scanner rewrites SCRIPTS_INVENTORY.md, scripts_inventory.json, and this REGISTRY.")
    lines.append("3. Every new file in this folder must appear in this table (re-run scanner).")
    lines.append("")
    reg_path = OUT_DIR / "REGISTRY.md"
    reg_path.write_text("\n".join(lines), encoding="utf-8")

    reg_json = {
        "generated": ts,
        "folder": "skill-orchestrator/references/inventory/scripts",
        "entries": entries,
    }
    # fix REGISTRY bytes after write
    for e in reg_json["entries"]:
        if e["filename"] == "REGISTRY.md":
            e["bytes"] = reg_path.stat().st_size
    (OUT_DIR / "registry.json").write_text(json.dumps(reg_json, indent=2), encoding="utf-8")
    return reg_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", action="store_true")
    args = ap.parse_args()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = scan()
    md_path = write_inventory(rows, ts)
    reg_path = refresh_registry(ts)
    if args.print:
        by = defaultdict(int)
        for r in rows:
            by[r["skill"]] += 1
        print(f"Total scripts: {len(rows)}")
        print(f"Skills with scripts: {len(by)}")
        for skill, n in sorted(by.items(), key=lambda x: -x[1]):
            print(f"  {n:3d}  {skill}")
        print(f"Wrote {md_path}")
        print(f"Wrote {reg_path}")
        print(f"Folder: {OUT_DIR}")
    else:
        print(f"Wrote {md_path} ({len(rows)} scripts)")
        print(f"Registry: {reg_path}")


if __name__ == "__main__":
    main()

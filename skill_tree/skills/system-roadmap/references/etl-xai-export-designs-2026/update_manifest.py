#!/usr/bin/env python3
"""
update_manifest.py — Auto-register files in this package into manifest.json

Designed for the etl-xai-export-designs-2026 capture under system-roadmap.
Scans the directory for .md / .py / .json (except itself and the manifest),
extracts Obsidian-style YAML frontmatter when present (title, keywords, date, status, tags),
and rebuilds manifest.json with full file registry + keyword index.

Usage:
  python3 update_manifest.py
  ./update_manifest.py          # after chmod +x

Idempotent. Safe to re-run after adding new files.
Under absolute Liv HUB claim.
"""

from __future__ import annotations

import json
import os
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = PACKAGE_ROOT / "manifest.json"
SKIP_NAMES = {"update_manifest.py", "manifest.json", "__pycache__"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """Extract simple YAML-like frontmatter keys (title, keywords, date, status, tags, owner)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    data: dict = {}
    current_key = None
    current_list: list = []
    for line in block.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        # list item
        if line.startswith("  - ") or line.startswith("- "):
            item = line.lstrip("- ").strip().strip('"').strip("'")
            if current_key:
                current_list.append(item)
            continue
        # key: value
        if ":" in line:
            if current_key and current_list:
                data[current_key] = current_list
                current_list = []
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val == "" or val == "[]" or val == "|":
                current_key = key
                current_list = []
            else:
                data[key] = val
                current_key = None
        else:
            continue
    if current_key and current_list:
        data[current_key] = current_list
    return data


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def collect_entries() -> list[dict]:
    entries = []
    for p in sorted(PACKAGE_ROOT.iterdir()):
        if not p.is_file():
            continue
        if p.name in SKIP_NAMES or p.name.startswith("."):
            continue
        if p.suffix not in {".md", ".py", ".json", ".txt", ".yaml", ".yml"}:
            continue

        text = ""
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass

        fm = parse_frontmatter(text) if p.suffix == ".md" else {}
        keywords = fm.get("keywords") or fm.get("obsidian_tags") or []
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(",")]
        # also pull from content if no fm keywords
        if not keywords and p.suffix == ".md":
            # light keyword harvest from headings / known terms
            for term in ["ETL", "Marty Set", "nuclear_vacuum", "ChronologyArc", "local-first", "ingestion", "Letta"]:
                if term.lower() in text.lower():
                    keywords.append(term)

        entry = {
            "filename": p.name,
            "path": str(p.relative_to(PACKAGE_ROOT)),
            "size_bytes": p.stat().st_size,
            "sha256_16": file_hash(p),
            "modified_iso": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(),
            "title": fm.get("title") or p.stem.replace("_", " ").title(),
            "status": fm.get("status") or "active",
            "date": fm.get("date") or fm.get("created") or "",
            "owner": fm.get("owner") or "system-roadmap",
            "keywords": sorted(set(str(k).lstrip("#") for k in keywords if k)),
            "frontmatter_present": bool(fm),
        }
        entries.append(entry)
    return entries


def main() -> None:
    entries = collect_entries()
    all_keywords = sorted({k for e in entries for k in e["keywords"]})

    manifest = {
        "package": "etl-xai-export-designs-2026",
        "owner": "system-roadmap",
        "description": "Captured design history of ETL / ingestion / memory-pull pipelines for xAI conversation exports (Jan–Apr 2026 window + Dec 2025 foundation). Auto-registered via update_manifest.py.",
        "created": "2026-08-16",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "liv_hub_claim": True,
        "auto_register": True,
        "script": "update_manifest.py",
        "keyword_index": all_keywords,
        "file_count": len(entries),
        "files": entries,
        "notes": [
            "Re-run update_manifest.py after adding any new .md / .py / .json to this folder.",
            "Frontmatter keywords and obsidian_tags are harvested automatically.",
            "Cross-ref: references/io-normalization-recon-2026-08-16/07_Historical_Local_First_ETL.md",
        ],
    }

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✅ manifest.json updated — {len(entries)} file(s) registered, {len(all_keywords)} unique keywords.")
    for e in entries:
        print(f"   • {e['filename']}  [{e['status']}]  keywords={e['keywords'][:6]}")


if __name__ == "__main__":
    main()

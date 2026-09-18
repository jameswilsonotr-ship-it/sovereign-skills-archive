#!/usr/bin/env python3
"""
promote_to_alpha.py — Olivia Dev → Olivia Dev Alpha promotion tool
=================================================================
Implements the protected promotion protocol.

Theory (do not invert):
  - Olivia Dev      = production / stable face of the development skill
  - Olivia Dev Alpha = living evolution surface where new material is wired

This script only moves material **from approved sources into Alpha**.
It never promotes from Alpha back to Dev (that is a separate, deliberate
stabilization step performed by a human after testing).

Usage:
  python scripts/promote_to_alpha.py [--dry-run] [--verbose]

The approved source → destination mappings live in:
  references/promotion/APPROVED_PROMOTION_LIST.md

Only Olivia Dev (or this script running under its authority) may run promotion.
The APPROVED_PROMOTION_LIST itself is never modified by this script except
for appending a log line.
"""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
DEV_ROOT = SKILLS_ROOT / "olivia-dev"
ALPHA_ROOT = SKILLS_ROOT / "olivia-dev-alpha"
LIST_FILE = DEV_ROOT / "references" / "promotion" / "APPROVED_PROMOTION_LIST.md"
LOG_SECTION = "## Promotion Log (append-only)"


def parse_approved_list(text: str) -> List[Tuple[str, str]]:
    """Extract (source, destination) pairs from the markdown table."""
    pairs = []
    # Look for table rows that contain a pipe and look like source|dest
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or "Source path" in line:
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 2:
            continue
        src, dest = cols[0], cols[1]
        # Skip header-like or empty
        if not src or src.lower().startswith("source"):
            continue
        # Clean backticks
        src = src.strip("`").strip()
        dest = dest.strip("`").strip()
        if src and dest:
            pairs.append((src, dest))
    return pairs


def resolve_source(src: str) -> Path:
    """Resolve a source path that may be relative to skills root or to olivia-dev."""
    # Already absolute-ish under skills
    if src.startswith("olivia-dev/") or src.startswith("skill-orchestrator/"):
        return SKILLS_ROOT / src
    # Relative to olivia-dev
    return DEV_ROOT / src


def resolve_dest(dest: str) -> Path:
    """Destination is always under olivia-dev-alpha."""
    return ALPHA_ROOT / dest


def should_copy(src_file: Path, dest_file: Path) -> bool:
    """Copy if destination missing or source is newer / different size."""
    if not dest_file.exists():
        return True
    try:
        if src_file.stat().st_mtime > dest_file.stat().st_mtime:
            return True
        if src_file.stat().st_size != dest_file.stat().st_size:
            return True
    except OSError:
        return True
    return False


def promote(dry_run: bool = False, verbose: bool = False) -> List[str]:
    if not LIST_FILE.exists():
        raise SystemExit(f"ERROR: approved list not found: {LIST_FILE}")

    text = LIST_FILE.read_text()
    pairs = parse_approved_list(text)
    if not pairs:
        print("No approved entries found in the list.")
        return []

    promoted: List[str] = []
    print(f"promote_to_alpha  dry_run={dry_run}  entries={len(pairs)}")

    for src_pat, dest_pat in pairs:
        if "APPROVED_PROMOTION_LIST" in src_pat:
            if verbose:
                print(f"  skip protected list itself: {src_pat}")
            continue

        src_path = resolve_source(src_pat)
        dest_path = resolve_dest(dest_pat)

        if not src_path.exists():
            if verbose:
                print(f"  missing source: {src_pat}")
            continue

        # Treat each approved entry as a single file mapping for now
        # (keeps destinations exact and avoids double-filename bugs)
        if src_path.is_file():
            dest_file = dest_path
            if dest_path.suffix == "" and not dest_path.exists():
                # destination looks like a directory — place file inside it
                dest_file = dest_path / src_path.name
            if not should_copy(src_path, dest_file):
                if verbose:
                    print(f"  up-to-date: {dest_file}")
                continue
            print(f"  promote: {src_path} → {dest_file}")
            if not dry_run:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest_file)
            promoted.append(str(dest_file.relative_to(ALPHA_ROOT)))
        else:
            # directory: copy contained files while preserving relative structure
            for src_file in src_path.rglob("*"):
                if not src_file.is_file():
                    continue
                rel = src_file.relative_to(src_path)
                dest_file = dest_path / rel
                if not should_copy(src_file, dest_file):
                    if verbose:
                        print(f"  up-to-date: {dest_file}")
                    continue
                print(f"  promote: {src_file} → {dest_file}")
                if not dry_run:
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dest_file)
                promoted.append(str(dest_file.relative_to(ALPHA_ROOT)))

    # Append log line (only when something actually happened and not dry-run)
    if promoted and not dry_run:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        log_line = f"- {ts}: promoted {len(promoted)} file(s): {', '.join(promoted[:5])}{'…' if len(promoted) > 5 else ''}\n"
        # Append after the log section header if present
        if LOG_SECTION in text:
            # Simple append at end of file (safe)
            with LIST_FILE.open("a") as f:
                f.write(log_line)
        else:
            with LIST_FILE.open("a") as f:
                f.write("\n" + LOG_SECTION + "\n" + log_line)

    if not promoted:
        print("Nothing to promote.")
    else:
        print(f"Promoted {len(promoted)} file(s).")
    return promoted


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote approved material into olivia-dev-alpha")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be copied without writing")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    promote(dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()

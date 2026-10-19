#!/usr/bin/env python3
"""
Image Pipeline Pack Migration Helper (starter)
================================================
Owned by skill-orchestrator. Conservative by design.

- Never deletes anything.
- Default mode is --dry-run.
- Real file operations require --execute + explicit confirmation.

Usage examples:
  python migrate_image_pipeline_pack.py --report
  python migrate_image_pipeline_pack.py --dry-run
  python migrate_image_pipeline_pack.py --execute --confirm-migrate

This is a suggestion / scaffold. Expand as the condensation work progresses.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

SKILLS_ROOT = Path("/home/workdir/.grok/skills")

IMAGE_FAMILY = [
    "image-pipeline",
    "image-pipeline-registry",
    "image-style-orchestrator",
    "image-skill-orchestrator",
    "bunny-top-10-image-styles",
    "liv-top-10-image-styles",
    "valerie-top-10-image-styles",
]


def find_skill(slug: str) -> Path | None:
    p = SKILLS_ROOT / slug
    if p.is_dir() and (p / "SKILL.md").exists():
        return p
    return None


def report() -> None:
    print("# Image Pipeline Family — Current Presence Report")
    print(f"# Generated: {datetime.now().isoformat(timespec='seconds')}")
    print()
    for slug in IMAGE_FAMILY:
        path = find_skill(slug)
        if path:
            has_refs = (path / "references").is_dir()
            has_scripts = (path / "scripts").is_dir()
            print(f"- {slug}: PRESENT  ({path})")
            print(f"    references/: {'yes' if has_refs else 'no'}   scripts/: {'yes' if has_scripts else 'no'}")
        else:
            print(f"- {slug}: MISSING")
    print()
    print("See references/migrations/image-pipeline-pack-migration.md for the full plan.")


def dry_run_copy_modules() -> None:
    """Example of a safe, non-destructive operation: report what *would* be copied."""
    print("# Dry-run: candidate modules that could be centralized under image-pipeline-registry/references/")
    print("# (No files are touched)")
    print()

    candidates = [
        ("bunny-top-10-image-styles", "references"),
        ("liv-top-10-image-styles", "references"),
        ("valerie-top-10-image-styles", "references"),
    ]

    target_base = SKILLS_ROOT / "image-pipeline-registry" / "references" / "styles"
    print(f"Target base (would be used): {target_base}")
    print()

    for slug, sub in candidates:
        src = find_skill(slug)
        if not src:
            print(f"  SKIP {slug} (not found)")
            continue
        src_dir = src / sub
        if not src_dir.is_dir():
            print(f"  SKIP {slug}/{sub} (no references/)")
            continue
        print(f"  WOULD COPY contents of {src_dir}  →  {target_base / slug}/")


def main() -> None:
    parser = argparse.ArgumentParser(description="Conservative Image Pipeline Pack migration helper")
    parser.add_argument("--report", action="store_true", help="Show current presence of image family skills")
    parser.add_argument("--dry-run", action="store_true", help="Show what a module centralization would do (no writes)")
    parser.add_argument("--execute", action="store_true", help="Actually perform operations (still requires --confirm-migrate)")
    parser.add_argument("--confirm-migrate", action="store_true", help="Required safety flag for any real writes")
    args = parser.parse_args()

    if args.report or (not args.dry_run and not args.execute):
        report()
        return

    if args.dry_run:
        dry_run_copy_modules()
        return

    if args.execute:
        if not args.confirm_migrate:
            print("ERROR: --execute requires --confirm-migrate. Refusing to touch files.")
            raise SystemExit(2)
        print("EXECUTE mode is intentionally not yet fully implemented.")
        print("Expand this script only after Phase 1 inventory and harnesses are ready.")
        print("See references/migrations/image-pipeline-pack-migration.md")
        raise SystemExit(0)


if __name__ == "__main__":
    main()

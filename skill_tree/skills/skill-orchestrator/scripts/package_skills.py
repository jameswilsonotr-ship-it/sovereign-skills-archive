#!/usr/bin/env python3
"""
package_skills.py — Local packaging backend for skill-orchestrator
=================================================================
Builds versioned .tar.gz packages + MANIFEST for one or more skills.
Does NOT call Google Drive itself (agent layer finishes the publish).

Usage examples:
  python scripts/package_skills.py --skills skill-orchestrator,olivia-dev-alpha \\
      --topic debug-contract-envelope --version 0.2.1

  python scripts/package_skills.py --skills chaos-bratz-roster \\
      --topic olivia-delivery --version 0.5.3 \\
      --paths references/agents/olivia references/mirrors/olivia.md

  python scripts/package_skills.py --skills skill-orchestrator --dry-run

Natural-language triggers (handled by skill-orchestrator):
  "package skills", "package and publish", "publish these skills",
  "export active skills", "make mining packages"
"""

from __future__ import annotations

import argparse
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
ARTIFACTS = Path("/home/workdir/artifacts/mining_packages")
DEFAULT_INCLUDE = [
    "references/",
    "CHANGELOG.md",
    "TODO.md",
    "SKILL.md",
    "README.md",
]


def resolve_skill(slug: str) -> Path:
    p = SKILLS_ROOT / slug
    if not p.is_dir():
        raise SystemExit(f"ERROR: skill not found: {slug}")
    return p


def collect_paths(skill_root: Path, explicit: Optional[List[str]]) -> List[Path]:
    """Return list of paths relative to skill_root to include in the tarball."""
    if explicit:
        paths = []
        for e in explicit:
            cand = skill_root / e
            if cand.exists():
                paths.append(Path(e))
            else:
                print(f"  warning: path not found, skipping: {e}")
        return paths

    # Default: include common high-signal files if they exist
    paths = []
    for pattern in DEFAULT_INCLUDE:
        cand = skill_root / pattern
        if cand.exists():
            paths.append(Path(pattern))
    # Always try to include any debugging_notes if present under references
    for notes in skill_root.glob("references/**/debugging_notes.md"):
        rel = notes.relative_to(skill_root)
        if rel not in paths:
            paths.append(rel)
    return paths


def make_tarball(skill: str, version: str, date: str, topic: str,
                 paths: List[Path], skill_root: Path, dry_run: bool) -> Path:
    name = f"{skill}_{topic}_v{version}_{date}.tar.gz"
    out = ARTIFACTS / name
    if dry_run:
        print(f"  [dry-run] would create {out}")
        return out

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out, "w:gz") as tar:
        for rel in paths:
            full = skill_root / rel
            # arcname keeps the skill/ prefix so restore is clean
            tar.add(full, arcname=f"{skill}/{rel}")
    print(f"  created {out} ({out.stat().st_size} bytes)")
    return out


def write_manifest(packages: List[dict], version: str, date: str, topic: str,
                   dry_run: bool) -> Path:
    man = ARTIFACTS / f"MANIFEST_v{version}_{date}.md"
    lines = [
        f"# MANIFEST — skill-orchestrator package_skills",
        f"**Version**: v{version}",
        f"**Date**: {date}",
        f"**Topic**: {topic}",
        f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "## Packages",
        "",
    ]
    for p in packages:
        lines.append(f"- `{p['name']}` ({p['size']} bytes)")
        lines.append(f"  - Skill: {p['skill']}")
        lines.append(f"  - Paths: {', '.join(str(x) for x in p['paths'])}")
        lines.append("")
    lines += [
        "## Restore example",
        "```bash",
        "cd /home/workdir/.grok/skills",
        f"tar -xzf {packages[0]['name'] if packages else '<package>.tar.gz'}",
        "```",
        "",
        "## Notes",
        "Produced by skill-orchestrator/scripts/package_skills.py.",
        "MANDATORY: agent layer MUST publish to Google Drive AND GitHub. Local artifacts are staging only.",
        "Drive parent: Conversational_Mining_Payloads (1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0)",
        "GitHub: jameswilsonotr-ship-it/sovereign-skills-archive snapshots/YYYY-MM-DD/",
        "See references/packaging/DUAL_PUBLISH.md. Fail-closed if both remotes miss.",
    ]
    content = "\n".join(lines)
    if dry_run:
        print("  [dry-run] MANIFEST would contain:")
        print(content[:400] + "...")
        return man
    man.write_text(content)
    print(f"  wrote {man}")
    return man


def main() -> None:
    parser = argparse.ArgumentParser(description="Package skills into versioned tar.gz + MANIFEST")
    parser.add_argument("--skills", required=True,
                        help="Comma-separated skill slugs (e.g. skill-orchestrator,olivia-dev-alpha)")
    parser.add_argument("--topic", default="package",
                        help="Short topic slug used in filenames")
    parser.add_argument("--version", default="0.1.0",
                        help="Semantic version for this package set")
    parser.add_argument("--paths", nargs="*", default=None,
                        help="Optional explicit relative paths to include (applied to every skill)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    skills = [s.strip() for s in args.skills.split(",") if s.strip()]
    packages = []

    print(f"package_skills  version={args.version}  topic={args.topic}  dry_run={args.dry_run}")
    for slug in skills:
        root = resolve_skill(slug)
        paths = collect_paths(root, args.paths)
        if not paths:
            print(f"  warning: no paths collected for {slug}, skipping")
            continue
        print(f"  {slug}: including {len(paths)} path(s)")
        tarball = make_tarball(slug, args.version, date, args.topic, paths, root, args.dry_run)
        packages.append({
            "name": tarball.name,
            "skill": slug,
            "paths": paths,
            "size": tarball.stat().st_size if tarball.exists() else 0,
            "path": str(tarball),
        })

    if not packages:
        raise SystemExit("ERROR: nothing to package")

    man = write_manifest(packages, args.version, date, args.topic, args.dry_run)

    print("\n=== UPLOAD READY ===")
    print(f"Suggested Drive folder name: v{args.version}_{date}_{args.topic}")
    print(f"Parent folder ID: 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0")
    print("Artifacts:")
    for p in packages:
        print(f"  {p['path']}")
    print(f"  {man}")
    print("\nMANDATORY publish (local is staging only):")
    print("  1. google_drive_create_folder under 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0")
    print("  2. google_drive_upload_artifact for EACH file above")
    print("  3. github___push_files to jameswilsonotr-ship-it/sovereign-skills-archive snapshots/{date}/")
    print("  4. Run is FAILED if Drive has no file_id. PARTIAL if Drive ok and GitHub fails.")
    print("  Ref: skill-orchestrator/references/packaging/DUAL_PUBLISH.md")


if __name__ == "__main__":
    main()

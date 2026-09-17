#!/usr/bin/env python3
"""
library_export.py — Programmatic export of the internal skill library.
Part of skill-orchestrator (no new top-level skill).

Usage:
  python scripts/library_export.py [--format md|json] [--tier 0|1|2|all]
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
TIERS_FILE = Path(__file__).resolve().parent.parent / "references" / "inventory" / "CURRENT_TIERS.md"
OUT_DIR = Path(__file__).resolve().parent.parent / "references" / "inventory"


def load_tier_map():
    """Parse CURRENT_TIERS.md into {slug: tier}."""
    tier_map = {}
    current_tier = None
    if not TIERS_FILE.exists():
        return tier_map
    for line in TIERS_FILE.read_text().splitlines():
        line = line.strip()
        if line.startswith("## Tier 2"):
            current_tier = 2
        elif line.startswith("## Tier 1"):
            current_tier = 1
        elif line.startswith("## Tier 0"):
            current_tier = 0
        elif line.startswith("- ") and current_tier is not None:
            slug = line[2:].split()[0].split("#")[0].strip()
            if slug:
                tier_map[slug] = current_tier
    return tier_map


def scan_skills():
    tier_map = load_tier_map()
    results = []
    for skill_dir in sorted(SKILLS_ROOT.iterdir()):
        if not skill_dir.is_dir():
            continue
        slug = skill_dir.name
        has_skill_md = (skill_dir / "SKILL.md").exists()
        has_readme = any(skill_dir.glob("README*"))
        has_todo = any(skill_dir.glob("TODO*")) or any(skill_dir.glob("todo*"))
        has_changelog = any(skill_dir.glob("CHANGELOG*")) or any(skill_dir.glob("changelog*"))
        has_refs = (skill_dir / "references").is_dir()
        has_scripts = (skill_dir / "scripts").is_dir()
        has_git = (skill_dir / ".git").is_dir()
        richness = "rich" if (has_refs or has_scripts) else "thin"
        tier = tier_map.get(slug, "unassigned")
        results.append({
            "slug": slug,
            "tier": tier,
            "richness": richness,
            "has_skill_md": has_skill_md,
            "has_readme": has_readme,
            "has_todo": has_todo,
            "has_changelog": has_changelog,
            "has_references": has_refs,
            "has_scripts": has_scripts,
            "has_git": has_git,
        })
    return results


def export_md(skills, tier_filter=None):
    lines = [
        f"# Skill Library Export",
        f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Authority**: skill-orchestrator",
        f"**Source plan**: references/plans/TIERED_LIBRARY_ARCHITECTURE.md",
        "",
        f"Total skills scanned: {len(skills)}",
        "",
    ]
    by_tier = {0: [], 1: [], 2: [], "unassigned": []}
    for s in skills:
        t = s["tier"]
        by_tier.get(t, by_tier["unassigned"]).append(s)

    for t in [2, 1, 0, "unassigned"]:
        group = by_tier[t]
        if tier_filter is not None and t != tier_filter:
            continue
        label = f"Tier {t}" if t != "unassigned" else "Unassigned"
        lines.append(f"## {label} ({len(group)})")
        lines.append("")
        lines.append("| Slug | Richness | README | TODO | CHANGELOG | refs/ | scripts/ | git |")
        lines.append("|------|----------|--------|------|-----------|-------|----------|-----|")
        for s in group:
            lines.append(
                f"| {s['slug']} | {s['richness']} | "
                f"{'Y' if s['has_readme'] else '.'} | "
                f"{'Y' if s['has_todo'] else '.'} | "
                f"{'Y' if s['has_changelog'] else '.'} | "
                f"{'Y' if s['has_references'] else '.'} | "
                f"{'Y' if s['has_scripts'] else '.'} | "
                f"{'Y' if s['has_git'] else '.'} |"
            )
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Export internal skill library")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--tier", choices=["0", "1", "2", "all"], default="all")
    args = parser.parse_args()

    skills = scan_skills()
    tier_filter = None if args.tier == "all" else int(args.tier)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

    if args.format == "json":
        out = OUT_DIR / f"export_{stamp}.json"
        data = {"generated": stamp, "skills": skills}
        out.write_text(json.dumps(data, indent=2))
        print(f"Wrote {out}")
    else:
        md = export_md(skills, tier_filter)
        out = OUT_DIR / f"export_{stamp}.md"
        out.write_text(md)
        # also write a latest pointer
        (OUT_DIR / "export_latest.md").write_text(md)
        print(md)
        print(f"\n[also written to {out} and export_latest.md]")


if __name__ == "__main__":
    main()

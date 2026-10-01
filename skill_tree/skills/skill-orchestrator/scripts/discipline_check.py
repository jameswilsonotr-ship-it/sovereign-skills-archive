#!/usr/bin/env python3
"""
discipline_check.py — Check file/folder discipline against tier requirements.
Part of skill-orchestrator (no new top-level skill).

Usage:
  python scripts/discipline_check.py --tier 0|1|2 [--batch slug1,slug2,...]
"""

import argparse
from pathlib import Path
from datetime import datetime, timezone

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
TIERS_FILE = Path(__file__).resolve().parent.parent / "references" / "inventory" / "CURRENT_TIERS.md"
OUT_DIR = Path(__file__).resolve().parent.parent / "references" / "inventory"

# Minimum requirements per tier
REQUIREMENTS = {
    0: ["SKILL.md", "README.md"],
    1: ["SKILL.md", "README.md", "TODO.md", "CHANGELOG.md"],
    2: ["SKILL.md", "README.md", "TODO.md", "CHANGELOG.md"],  # + preferably references/
}


def load_tier_map():
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


def check_skill(slug, required_tier):
    skill_dir = SKILLS_ROOT / slug
    if not skill_dir.is_dir():
        return {"slug": slug, "exists": False, "missing": ["<directory missing>"], "extra_notes": []}

    missing = []
    notes = []
    reqs = REQUIREMENTS.get(required_tier, [])

    for req in reqs:
        # allow README* and TODO* / CHANGELOG* variants
        if req == "README.md":
            if not any(skill_dir.glob("README*")):
                missing.append("README.md")
        elif req == "TODO.md":
            if not (any(skill_dir.glob("TODO*")) or any(skill_dir.glob("todo*"))):
                missing.append("TODO.md")
        elif req == "CHANGELOG.md":
            if not (any(skill_dir.glob("CHANGELOG*")) or any(skill_dir.glob("changelog*"))):
                missing.append("CHANGELOG.md")
        else:
            if not (skill_dir / req).exists():
                missing.append(req)

    if required_tier == 2:
        if not (skill_dir / "references").is_dir():
            notes.append("Tier 2 preference: references/ missing")
        if not (skill_dir / ".git").is_dir():
            notes.append("Tier 2 preference: local git missing")

    return {
        "slug": slug,
        "exists": True,
        "missing": missing,
        "extra_notes": notes,
        "pass": len(missing) == 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", type=int, choices=[0, 1, 2], required=True)
    parser.add_argument("--batch", type=str, default=None, help="Comma-separated slugs. Default: all of that tier")
    args = parser.parse_args()

    tier_map = load_tier_map()
    if args.batch:
        slugs = [s.strip() for s in args.batch.split(",") if s.strip()]
    else:
        slugs = [s for s, t in tier_map.items() if t == args.tier]

    results = [check_skill(s, args.tier) for s in sorted(slugs)]
    passed = sum(1 for r in results if r.get("pass"))
    failed = [r for r in results if not r.get("pass")]

    lines = [
        f"# Discipline Check — Tier {args.tier}",
        f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Checked**: {len(results)} skills | Passed: {passed} | Failed: {len(failed)}",
        "",
    ]

    if failed:
        lines.append("## Failures")
        for r in failed:
            lines.append(f"- **{r['slug']}**: missing {r['missing']}")
            for n in r.get("extra_notes", []):
                lines.append(f"  - note: {n}")
        lines.append("")

    lines.append("## All Results")
    for r in results:
        status = "PASS" if r.get("pass") else "FAIL"
        lines.append(f"- [{status}] {r['slug']}")
        if r.get("extra_notes"):
            for n in r["extra_notes"]:
                lines.append(f"    {n}")

    report = "\n".join(lines)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"discipline_tier{args.tier}_latest.md"
    out.write_text(report)
    print(report)
    print(f"\n[written to {out}]")


if __name__ == "__main__":
    main()

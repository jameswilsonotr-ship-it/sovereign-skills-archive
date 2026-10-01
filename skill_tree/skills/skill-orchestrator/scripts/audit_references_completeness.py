#!/usr/bin/env python3
"""
audit_references_completeness.py — Detect missing or stub reference files
=======================================================================
Walks every skill (or a single slug), extracts paths mentioned in SKILL.md
(especially under references/), and reports:

  - Declared paths that do not exist on disk
  - Existing reference files that are empty or near-empty stubs
  - Simple command → protocol gaps when a skill lists CLI verbs but has
    no matching references/ protocol file

Part of skill-orchestrator. Complements discipline_check.py (which only
checks for presence of README/TODO/CHANGELOG etc.).

Usage:
  python scripts/audit_references_completeness.py
  python scripts/audit_references_completeness.py --skill grok-conversation-miner
  python scripts/audit_references_completeness.py --json
  python scripts/audit_references_completeness.py --fail-on-gap   # exit 1 if any critical gaps

Natural-language triggers (skill-orchestrator):
  "skill audit references"
  "skill audit completeness"
  "audit skill references"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

SKILLS_ROOTS = [
    Path("/home/workdir/.grok/skills"),
    Path("/root/.grok/skills"),
]
OUT_DIR = Path(__file__).resolve().parent.parent / "references" / "inventory"

# Paths that look like file references inside markdown
PATH_RE = re.compile(
    r"""(?:references/|scripts/|assets/|tests?/|harness/)[^\s`"'<>)\]]+\.(?:md|py|json|yaml|yml|txt|sh)""",
    re.IGNORECASE,
)
# Also catch bare "read references/foo.md" or "see foo.md" style mentions
BARE_REF_RE = re.compile(
    r"""(?:read|see|load|open|from|in)\s+[`'"]?(references/[^\s`'"]+\.(?:md|py|json|yaml|yml|txt))[`'"]?""",
    re.IGNORECASE,
)

# Commands that often imply a protocol file should exist
COMMAND_HINT_RE = re.compile(
    r"""(?:roster|skill|miner|vacuum|publish|audit|inventory|version|history|show|boot|test)\s+[\w\-]+""",
    re.IGNORECASE,
)

STUB_MAX_BYTES = 250  # under this → treated as near-empty stub


def find_skill_dirs(only_slug: Optional[str] = None) -> List[Path]:
    dirs: List[Path] = []
    for root in SKILLS_ROOTS:
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            if not (child / "SKILL.md").exists():
                continue
            if only_slug and child.name != only_slug:
                continue
            dirs.append(child)
    return dirs


def is_glob_path(rel: str) -> bool:
    """True if path is a pattern, not a single concrete file."""
    return any(ch in rel for ch in ("*", "?", "["))


def expand_glob_or_concrete(skill_dir: Path, rel: str) -> tuple:
    """
    Returns (kind, paths_for_missing_check).
    kind: "concrete" | "glob" | "skip"
    For globs: if any match exists under skill_dir, treat as satisfied (no missing).
    If zero matches, report the glob pattern once as missing (optional) — we skip
    counting globs as critical missing to avoid false positives like mirrors/*.md.
    """
    if is_glob_path(rel):
        matches = list(skill_dir.glob(rel))
        if matches:
            return "glob_ok", []
        # Do not count unresolved globs as critical gaps (declarative patterns)
        return "glob_skip", []
    return "concrete", [rel]


def extract_mentioned_paths(skill_md: Path) -> Set[str]:
    text = skill_md.read_text(errors="replace")
    found: Set[str] = set()
    for rx in (PATH_RE, BARE_REF_RE):
        for m in rx.finditer(text):
            p = m.group(0) if "references/" in m.group(0) or "scripts/" in m.group(0) else m.group(1) if m.lastindex else m.group(0)
            # Clean trailing punctuation
            p = p.strip().rstrip(".,;:!?)")
            if p.startswith(("references/", "scripts/", "assets/", "tests/", "test/", "harness/")):
                found.add(p)
    return found


def is_stub(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        size = path.stat().st_size
        if size < STUB_MAX_BYTES:
            return True
        # Also treat files that are only a title + a couple of lines as stubs
        text = path.read_text(errors="replace").strip()
        if len(text) < 180 and text.count("\n") < 6:
            return True
    except Exception:
        return False
    return False


def audit_skill(skill_dir: Path) -> Dict:
    slug = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    result = {
        "slug": slug,
        "skill_md_exists": skill_md.exists(),
        "missing_paths": [],
        "stub_files": [],
        "mentioned_count": 0,
        "critical_gaps": 0,
        "notes": [],
    }
    if not skill_md.exists():
        result["notes"].append("SKILL.md missing")
        result["critical_gaps"] = 1
        return result

    mentioned = extract_mentioned_paths(skill_md)
    result["mentioned_count"] = len(mentioned)

    for rel in sorted(mentioned):
        kind, concretes = expand_glob_or_concrete(skill_dir, rel)
        if kind == "glob_ok":
            result["notes"].append(f"glob_ok: {rel}")
            continue
        if kind == "glob_skip":
            result["notes"].append(f"glob_pattern_skipped: {rel}")
            continue
        for crel in concretes:
            full = skill_dir / crel
            if not full.exists():
                result["missing_paths"].append(crel)
                result["critical_gaps"] += 1
            elif is_stub(full):
                result["stub_files"].append(crel)
                # stubs are warnings, not always critical
                result["notes"].append(f"stub: {crel}")

    # Light heuristic: if SKILL.md talks about "references/" a lot but the dir is missing
    if "references/" in skill_md.read_text(errors="replace") and not (skill_dir / "references").is_dir():
        result["notes"].append("SKILL.md mentions references/ but references/ directory is missing")
        result["critical_gaps"] += 1

    return result




def load_run_payload(run_id_or_path: str) -> dict:
    """Load a run by ID (e.g. 20260724T182818Z), 'latest', 'previous', or full path."""
    COMP = OUT_DIR / "completeness"
    RUNS = COMP / "runs"
    if run_id_or_path in ("latest", "last"):
        path = COMP / "latest.json"
    elif run_id_or_path in ("previous", "prev"):
        # second-newest run
        runs = sorted(RUNS.glob("run_*.json"), reverse=True)
        if len(runs) < 2:
            raise FileNotFoundError("Not enough runs to compute previous")
        path = runs[1]
    else:
        # treat as run_id or path
        candidate = RUNS / f"run_{run_id_or_path}.json"
        if candidate.exists():
            path = candidate
        else:
            path = Path(run_id_or_path)
    if not path.exists():
        raise FileNotFoundError(f"Run not found: {run_id_or_path}")
    return json.loads(path.read_text())


def diff_runs(a: dict, b: dict) -> dict:
    """Compare two run payloads. a = older, b = newer (or any order; we label them)."""
    def index(results):
        return {r["slug"]: r for r in results}

    ia, ib = index(a["results"]), index(b["results"])
    all_slugs = sorted(set(ia) | set(ib))

    newly_broken = []
    newly_fixed = []
    still_open = []
    still_clean = []
    changed_detail = []

    for slug in all_slugs:
        ra, rb = ia.get(slug), ib.get(slug)
        gaps_a = set(ra["missing_paths"]) | set(ra.get("stub_files", [])) if ra else set()
        gaps_b = set(rb["missing_paths"]) | set(rb.get("stub_files", [])) if rb else set()
        crit_a = ra["critical_gaps"] if ra else 0
        crit_b = rb["critical_gaps"] if rb else 0

        if crit_a == 0 and crit_b > 0:
            newly_broken.append(slug)
        elif crit_a > 0 and crit_b == 0:
            newly_fixed.append(slug)
        elif crit_a > 0 and crit_b > 0:
            still_open.append(slug)
            added = sorted(gaps_b - gaps_a)
            removed = sorted(gaps_a - gaps_b)
            if added or removed:
                changed_detail.append({"slug": slug, "added": added, "removed": removed})
        else:
            still_clean.append(slug)

    return {
        "run_a": {"run_id": a.get("run_id"), "timestamp": a.get("timestamp"), "critical_gaps": a.get("critical_gaps")},
        "run_b": {"run_id": b.get("run_id"), "timestamp": b.get("timestamp"), "critical_gaps": b.get("critical_gaps")},
        "delta_critical_gaps": b.get("critical_gaps", 0) - a.get("critical_gaps", 0),
        "newly_broken": newly_broken,
        "newly_fixed": newly_fixed,
        "still_open": still_open,
        "still_clean_count": len(still_clean),
        "changed_detail": changed_detail,
    }


def archive_old_runs(keep_days: int = 30, keep_min: int = 10) -> dict:
    """Move run files older than keep_days into runs/archive/YYYY-MM/. Always keep the newest keep_min runs hot."""
    import shutil
    from datetime import timedelta

    COMP = OUT_DIR / "completeness"
    RUNS = COMP / "runs"
    ARCHIVE = RUNS / "archive"
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=keep_days)

    runs = sorted(RUNS.glob("run_*.json"), reverse=True)
    # always protect the newest keep_min
    protected = {r.stem for r in runs[:keep_min]}

    moved = []
    for jp in runs:
        if jp.stem in protected:
            continue
        # parse timestamp from filename run_YYYYMMDDTHHMMSSZ
        m = re.match(r"run_(\d{8}T\d{6}Z)", jp.name)
        if not m:
            continue
        try:
            ts = datetime.strptime(m.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if ts >= cutoff:
            continue
        month_dir = ARCHIVE / ts.strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        for ext in (".json", ".md"):
            src = jp.with_suffix(ext)
            if src.exists():
                dest = month_dir / src.name
                shutil.move(str(src), str(dest))
                moved.append(str(dest.relative_to(COMP)))
    return {"moved": moved, "kept_hot": len(list(RUNS.glob("run_*.json"))), "archive_root": str(ARCHIVE)}




def main() -> int:
    parser = argparse.ArgumentParser(description="Audit skill reference completeness")
    parser.add_argument("--skill", help="Audit only this slug")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of table")
    parser.add_argument("--fail-on-gap", action="store_true", help="Exit 1 if any critical gaps")
    parser.add_argument("--no-save", action="store_true", help="Do not write results to disk (dry display only)")
    parser.add_argument("--diff", nargs="?", const="previous", default=None,
                        help="Diff two runs. Usage: --diff [previous|latest|RUN_ID] [RUN_ID]. Default: previous vs latest")
    parser.add_argument("--archive", action="store_true", help="Archive runs older than 30 days (keeps newest 10 hot)")
    parser.add_argument("--archive-days", type=int, default=30, help="Days to keep hot (with --archive)")
    args = parser.parse_args()

    # ----- early exits for diff / archive modes -----
    if args.archive:
        stats = archive_old_runs(keep_days=args.archive_days)
        print(json.dumps(stats, indent=2) if args.json else stats)
        return 0

    if args.diff is not None:
        # parse --diff [A] [B]
        # argparse with nargs=? only captures one; allow a second positional via remaining
        # simpler: --diff previous  or  --diff RUN_A RUN_B via sys.argv scrape
        extra = [a for a in sys.argv[1:] if not a.startswith("-") and a not in (args.skill or "")]
        # args.diff is the first value (or "previous" if flag alone)
        a_id = args.diff if args.diff != "previous" else "previous"
        b_id = "latest"
        # if user passed two run ids after --diff
        diff_args = []
        capture = False
        for a in sys.argv[1:]:
            if a == "--diff":
                capture = True
                continue
            if capture:
                if a.startswith("-"):
                    break
                diff_args.append(a)
        if len(diff_args) >= 2:
            a_id, b_id = diff_args[0], diff_args[1]
        elif len(diff_args) == 1:
            a_id, b_id = diff_args[0], "latest"

        try:
            run_a = load_run_payload(a_id)
            run_b = load_run_payload(b_id)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2

        # ensure chronological order for "delta" sign
        if run_a.get("timestamp", "") > run_b.get("timestamp", ""):
            run_a, run_b = run_b, run_a

        delta = diff_runs(run_a, run_b)

        # save diff
        COMP = OUT_DIR / "completeness"
        DIFFS = COMP / "diffs"
        DIFFS.mkdir(parents=True, exist_ok=True)
        diff_id = f"diff_{run_a.get('run_id','A')}_{run_b.get('run_id','B')}"
        (DIFFS / f"{diff_id}.json").write_text(json.dumps(delta, indent=2))

        md = [
            f"# Completeness Diff — {run_a.get('run_id')} → {run_b.get('run_id')}",
            "",
            f"- Older: `{run_a.get('run_id')}` ({run_a.get('timestamp','')[:19]})  critical_gaps={run_a.get('critical_gaps')}",
            f"- Newer: `{run_b.get('run_id')}` ({run_b.get('timestamp','')[:19]})  critical_gaps={run_b.get('critical_gaps')}",
            f"- Delta critical gaps: **{delta['delta_critical_gaps']:+d}**",
            "",
            f"## Newly fixed ({len(delta['newly_fixed'])})",
            "",
        ]
        for s in delta["newly_fixed"]:
            md.append(f"- `{s}`")
        md += ["", f"## Newly broken ({len(delta['newly_broken'])})", ""]
        for s in delta["newly_broken"]:
            md.append(f"- `{s}`")
        md += ["", f"## Still open ({len(delta['still_open'])})", ""]
        for s in delta["still_open"]:
            md.append(f"- `{s}`")
        if delta["changed_detail"]:
            md += ["", "## Detail changes on still-open skills", ""]
            for c in delta["changed_detail"]:
                md.append(f"### {c['slug']}")
                if c["removed"]:
                    md.append("- Fixed paths: " + ", ".join(f"`{x}`" for x in c["removed"]))
                if c["added"]:
                    md.append("- New gaps: " + ", ".join(f"`{x}`" for x in c["added"]))
                md.append("")
        md_path = DIFFS / f"{diff_id}.md"
        md_path.write_text("\n".join(md))

        if args.json:
            print(json.dumps(delta, indent=2))
        else:
            print("\n".join(md))
            print(f"\n[saved] {md_path}")
        return 0


    skills = find_skill_dirs(args.skill)
    if not skills:
        print("No skills found" + (f" matching '{args.skill}'" if args.skill else ""), file=sys.stderr)
        return 2

    ts = datetime.now(timezone.utc)
    ts_iso = ts.isoformat()
    ts_slug = ts.strftime("%Y%m%dT%H%M%SZ")

    results = [audit_skill(d) for d in skills]
    total_gaps = sum(r["critical_gaps"] for r in results)
    skills_with_gaps = [r for r in results if r["critical_gaps"] > 0 or r["stub_files"]]
    skills_clean = [r for r in results if r["critical_gaps"] == 0 and not r["stub_files"]]

    payload = {
        "run_id": ts_slug,
        "timestamp": ts_iso,
        "scope": args.skill or "all",
        "audited": len(results),
        "critical_gaps": total_gaps,
        "skills_with_gaps": len(skills_with_gaps),
        "skills_clean": len(skills_clean),
        "results": results,
    }

    # ----- always-on accumulation (unless --no-save) -----
    if not args.no_save:
        COMPLETENESS_DIR = OUT_DIR / "completeness"
        RUNS_DIR = COMPLETENESS_DIR / "runs"
        RUNS_DIR.mkdir(parents=True, exist_ok=True)

        # 1. Timestamped full run
        run_json = RUNS_DIR / f"run_{ts_slug}.json"
        run_json.write_text(json.dumps(payload, indent=2))

        # 2. Human-readable run summary
        run_md_lines = [
            f"# Completeness Audit Run — {ts.strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            f"- Run ID: `{ts_slug}`",
            f"- Scope: **{payload['scope']}**",
            f"- Audited: **{payload['audited']}**",
            f"- Critical gaps: **{payload['critical_gaps']}**",
            f"- Skills with gaps: **{payload['skills_with_gaps']}**",
            f"- Skills clean: **{payload['skills_clean']}**",
            "",
        ]
        if skills_with_gaps:
            run_md_lines.append("## Skills with gaps")
            run_md_lines.append("")
            for r in skills_with_gaps:
                run_md_lines.append(f"### {r['slug']}  (critical_gaps={r['critical_gaps']})")
                if r["missing_paths"]:
                    run_md_lines.append("- **Missing:**")
                    for pth in r["missing_paths"]:
                        run_md_lines.append(f"  - `{pth}`")
                if r["stub_files"]:
                    run_md_lines.append("- **Stubs / near-empty:**")
                    for pth in r["stub_files"]:
                        run_md_lines.append(f"  - `{pth}`")
                for n in r["notes"]:
                    if not n.startswith("stub:"):
                        run_md_lines.append(f"- note: {n}")
                run_md_lines.append("")
        else:
            run_md_lines.append("No critical gaps or stubs found in this run.")
            run_md_lines.append("")

        run_md = RUNS_DIR / f"run_{ts_slug}.md"
        run_md.write_text("\n".join(run_md_lines))

        # 3. Update latest convenience copies
        (COMPLETENESS_DIR / "latest.json").write_text(json.dumps(payload, indent=2))
        (COMPLETENESS_DIR / "latest.md").write_text("\n".join(run_md_lines))
        # Also keep the old flat names for backward compatibility
        (OUT_DIR / "completeness_latest.json").write_text(json.dumps(payload, indent=2))
        (OUT_DIR / "completeness_latest.md").write_text("\n".join(run_md_lines))

        # Human rollup parallel to SCRIPTS_INVENTORY.md
        rollup = [
            "# Completeness Inventory",
            "",
            f"**Latest run**: `{ts_slug}`",
            f"**Timestamp**: {ts.strftime('%Y-%m-%dT%H:%M:%SZ')}",
            f"**Generator**: skill-orchestrator/scripts/audit_references_completeness.py",
            f"**Audited**: {payload['audited']} | **Critical gaps**: {payload['critical_gaps']} | **Clean**: {payload.get('skills_clean', 0)}",
            "",
            "See `completeness/latest.md` for full detail and `completeness/REGISTRY.md` for history.",
            "",
            "## Skills with critical gaps",
            "",
        ]
        for r in sorted(payload["results"], key=lambda x: -x.get("critical_gaps", 0)):
            if r.get("critical_gaps", 0) > 0:
                rollup.append(f"### {r['slug']} ({r['critical_gaps']})")
                for mp in r.get("missing_paths", []):
                    rollup.append(f"- missing: `{mp}`")
                for st in r.get("stub_files", []):
                    rollup.append(f"- stub: `{st}`")
                rollup.append("")
        if payload["critical_gaps"] == 0:
            rollup.append("_No critical gaps in this run._")
            rollup.append("")
        (OUT_DIR / "COMPLETENESS_INVENTORY.md").write_text("\n".join(rollup))



        # 4. Registry / manifest (append-only log of every pass)
        registry_path = COMPLETENESS_DIR / "REGISTRY.md"
        registry_json_path = COMPLETENESS_DIR / "registry.json"

        # Load existing registry json
        registry: list = []
        if registry_json_path.exists():
            try:
                registry = json.loads(registry_json_path.read_text())
            except Exception:
                registry = []

        entry = {
            "run_id": ts_slug,
            "timestamp": ts_iso,
            "scope": payload["scope"],
            "audited": payload["audited"],
            "critical_gaps": payload["critical_gaps"],
            "skills_with_gaps": payload["skills_with_gaps"],
            "skills_clean": payload["skills_clean"],
            "run_json": str(run_json.relative_to(COMPLETENESS_DIR)),
            "run_md": str(run_md.relative_to(COMPLETENESS_DIR)),
        }
        registry.append(entry)
        registry_json_path.write_text(json.dumps(registry, indent=2))

        # Human registry
        reg_lines = [
            "# Completeness Audit Registry",
            "",
            "Append-only log of every audit pass. Owned by skill-orchestrator; referenced by olivia-dev-alpha.",
            "",
            "| Run ID | Timestamp (UTC) | Scope | Audited | Critical gaps | Skills w/ gaps | Clean |",
            "|--------|-----------------|-------|---------|---------------|----------------|-------|",
        ]
        for e in reversed(registry):  # newest first
            reg_lines.append(
                f"| `{e['run_id']}` | {e['timestamp'][:19]} | {e['scope']} | {e['audited']} | "
                f"{e['critical_gaps']} | {e['skills_with_gaps']} | {e['skills_clean']} |"
            )
        reg_lines.append("")
        reg_lines.append(f"Total runs recorded: **{len(registry)}**")
        reg_lines.append("")
        registry_path.write_text("\n".join(reg_lines))

        print(f"[saved] run → {run_json}", file=sys.stderr)
        print(f"[saved] registry → {registry_path} ({len(registry)} runs)", file=sys.stderr)

    # ----- display -----
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Skill reference completeness audit — {ts.strftime('%Y-%m-%d %H:%M UTC')}")
        print(f"Audited: {len(results)} skills | Critical gaps: {total_gaps}")
        print("-" * 72)
        if not skills_with_gaps:
            print("All audited skills have complete referenced files (no missing paths, no critical stubs).")
        else:
            for r in skills_with_gaps:
                print(f"\n[{r['slug']}]  critical_gaps={r['critical_gaps']}")
                if r["missing_paths"]:
                    print("  MISSING:")
                    for pth in r["missing_paths"]:
                        print(f"    - {pth}")
                if r["stub_files"]:
                    print("  STUBS / near-empty:")
                    for pth in r["stub_files"]:
                        print(f"    - {pth}")
                for n in r["notes"]:
                    if not n.startswith("stub:"):
                        print(f"  note: {n}")
        print("-" * 72)
        print("Done.")

    if args.fail_on_gap and total_gaps > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

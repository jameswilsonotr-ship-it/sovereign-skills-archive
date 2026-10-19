#!/usr/bin/env python3
"""
audit_lexicon.py — WQ-029 library lexicon audit (+ optional auto-fix)

Reads SSOT: olivia-dev-alpha/references/lexicon/lexicon_terms.json
Scans skill SKILL.md (+ optional README.md) under /home/workdir/.grok/skills

Usage:
  python3 audit_lexicon.py --print
  python3 audit_lexicon.py --json
  python3 audit_lexicon.py --fix          # apply conservative auto_fix rules
  python3 audit_lexicon.py --skill format-bible
  python3 audit_lexicon.py --fix --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SKILLS = Path("/home/workdir/.grok/skills")
ORCH = SKILLS / "skill-orchestrator"
TERMS = SKILLS / "olivia-dev-alpha" / "references" / "lexicon" / "lexicon_terms.json"
OUT = ORCH / "references" / "inventory" / "lexicon"

SKIP_DIRS = {".git", "__pycache__", "tarballs", "node_modules", ".venv"}


def load_terms() -> dict:
    if not TERMS.is_file():
        raise SystemExit(f"Missing lexicon SSOT: {TERMS}")
    return json.loads(TERMS.read_text(encoding="utf-8"))


def iter_targets(skill: str | None) -> list[Path]:
    roots = [SKILLS / skill] if skill else [d for d in SKILLS.iterdir() if d.is_dir()]
    files: list[Path] = []
    for root in roots:
        if not root.is_dir() or root.name in SKIP_DIRS:
            continue
        for name in ("SKILL.md", "README.md"):
            p = root / name
            if p.is_file():
                files.append(p)
        # light: future_target often only in SKILL.md
    return files


def flags_from(s: str) -> int:
    f = 0
    if "i" in s:
        f |= re.IGNORECASE
    if "m" in s:
        f |= re.MULTILINE
    return f


def scan_file(path: Path, terms: dict) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(SKILLS))
    hits: list[dict] = []

    for rule in terms.get("auto_fix", []):
        pat = rule["pattern"]
        fl = flags_from(rule.get("flags", ""))
        for m in re.finditer(pat, text):
            hits.append(
                {
                    "file": rel,
                    "kind": "auto_fix_candidate",
                    "match": m.group(0),
                    "suggest": re.sub(pat, rule["replace"], m.group(0), flags=fl),
                    "pattern": pat,
                }
            )

    for fp in terms.get("forbidden_phrases", []):
        pat = fp["pattern"]
        # Patterns may include lookarounds; do not force IGNORECASE (avoids "Agent Skills" product false positives)
        if re.search(pat, text):
            hits.append(
                {
                    "file": rel,
                    "kind": "forbidden_phrase",
                    "match": pat,
                    "message": fp.get("message", ""),
                    "id": fp.get("id"),
                }
            )
        elif re.search(pat, text, re.IGNORECASE) and "Agent Skills" not in text:
            hits.append(
                {
                    "file": rel,
                    "kind": "forbidden_phrase",
                    "match": pat,
                    "message": fp.get("message", ""),
                    "id": fp.get("id"),
                }
            )

    # pending rename mentions as warnings when explicit old slug used as future name wrongly
    for old, new in terms.get("pending_rename_slugs", {}).items():
        # warn if future_target still points at -service form of known surface family
        pass

    # deprecated bare "service" in future_target lines
    for m in re.finditer(r"future_target:\s*([^\s]+)", text, re.I):
        val = m.group(1).strip()
        if val.endswith("-service"):
            hits.append(
                {
                    "file": rel,
                    "kind": "deprecated_future_target",
                    "match": m.group(0),
                    "suggest": m.group(0).replace("-service", "-surface"),
                }
            )

    return hits


def apply_fixes(path: Path, terms: dict, dry_run: bool) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text
    actions = []
    for rule in terms.get("auto_fix", []):
        pat = rule["pattern"]
        repl = rule["replace"]
        fl = flags_from(rule.get("flags", ""))
        new_text, n = re.subn(pat, repl, text, flags=fl)
        if n:
            actions.append(f"{path.name}: {n}× /{pat}/ → {repl}")
            text = new_text
    if text != original and not dry_run:
        path.write_text(text, encoding="utf-8")
        actions.append(f"WROTE {path}")
    elif text != original and dry_run:
        actions.append(f"DRY-RUN would write {path}")
    return actions


def main() -> int:
    ap = argparse.ArgumentParser(description="WQ-029 lexicon audit")
    ap.add_argument("--print", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fix", action="store_true", help="apply auto_fix rules")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skill", default="", help="single skill slug")
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    terms = load_terms()
    files = iter_targets(args.skill or None)
    all_hits: list[dict] = []
    fix_log: list[str] = []

    for f in files:
        all_hits.extend(scan_file(f, terms))
        if args.fix:
            fix_log.extend(apply_fixes(f, terms, args.dry_run))

    # re-scan after fix for report
    if args.fix and not args.dry_run:
        all_hits = []
        for f in files:
            all_hits.extend(scan_file(f, terms))

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {
        "ts": ts,
        "lexicon_version": terms.get("version"),
        "files_scanned": len(files),
        "hit_count": len(all_hits),
        "hits": all_hits,
        "fix_log": fix_log,
    }

    if not args.no_save:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "lexicon_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        lines = [
            "# LEXICON_AUDIT",
            f"**Updated**: {ts}",
            f"**Files scanned**: {len(files)} · **Hits**: {len(all_hits)}",
            f"**Lexicon**: {TERMS}",
            "",
            "| File | Kind | Match | Suggest / message |",
            "|------|------|-------|-------------------|",
        ]
        for h in all_hits[:200]:
            lines.append(
                "| {file} | {kind} | {match} | {extra} |".format(
                    file=h.get("file", ""),
                    kind=h.get("kind", ""),
                    match=str(h.get("match", ""))[:60].replace("|", "/"),
                    extra=str(h.get("suggest") or h.get("message") or "")[:60].replace("|", "/"),
                )
            )
        if len(all_hits) > 200:
            lines.append(f"| … | | | {len(all_hits) - 200} more |")
        lines.append("")
        if fix_log:
            lines.append("## Fix log")
            lines.extend(f"- {x}" for x in fix_log)
        (OUT / "LEXICON_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
        (OUT / "REGISTRY.md").write_text(
            f"# lexicon inventory\n\n- SSOT: olivia-dev-alpha/references/lexicon/\n- latest: LEXICON_AUDIT.md\n- updated: {ts}\n",
            encoding="utf-8",
        )

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Lexicon audit — {ts}")
        print(f"Files: {len(files)} | Hits: {len(all_hits)} | fix={args.fix} dry_run={args.dry_run}")
        for h in all_hits[:40]:
            print(f"  [{h.get('kind')}] {h.get('file')}: {h.get('match')!r}")
        if len(all_hits) > 40:
            print(f"  … {len(all_hits) - 40} more")
        for x in fix_log:
            print(f"  FIX: {x}")
        if not args.no_save:
            print(f"[saved] {OUT / 'LEXICON_AUDIT.md'}")

    # exit 1 if unresolved high severity remain after optional fix
    high = [h for h in all_hits if h.get("kind") in ("forbidden_phrase", "deprecated_future_target")]
    return 1 if high else 0


if __name__ == "__main__":
    raise SystemExit(main())

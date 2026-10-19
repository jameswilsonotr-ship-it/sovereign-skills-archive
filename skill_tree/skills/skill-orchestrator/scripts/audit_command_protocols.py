#!/usr/bin/env python3
"""
audit_command_protocols.py — phrase_routes vs live skills/modules

Verifies skill-orchestrator/references/phrase_routes.md:
  - feeder skill directory exists under /home/workdir/.grok/skills
  - optional module path references/modules/<module>/ when module looks like a slug

Outputs:
  references/inventory/commands/COMMANDS_INVENTORY.md
  references/inventory/commands/commands_inventory.json
  references/inventory/commands/REGISTRY.md (pointer)

Usage:
  python3 audit_command_protocols.py
  python3 audit_command_protocols.py --print
  python3 audit_command_protocols.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SKILLS = Path("/home/workdir/.grok/skills")
ORCH = SKILLS / "skill-orchestrator"
PHRASE = ORCH / "references" / "phrase_routes.md"
OUT_DIR = ORCH / "references" / "inventory" / "commands"


def parse_phrase_routes(text: str) -> list[dict]:
    """Parse markdown tables with Phrase | Feeder | Module columns."""
    rows: list[dict] = []
    lines = text.splitlines()
    i = 0
    section = ""
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            section = line[3:].strip()
        # table header
        if re.search(r"\|\s*Phrase", line, re.I) and "Feeder" in line:
            i += 1
            if i < len(lines) and re.match(r"^\|[\s\-|:]+\|", lines[i]):
                i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if len(cells) >= 3 and not cells[0].startswith("---"):
                    phrase, feeder, module = cells[0], cells[1], cells[2]
                    if phrase and feeder and "Phrase" not in phrase:
                        rows.append(
                            {
                                "section": section,
                                "phrase": phrase,
                                "feeder": feeder.strip(),
                                "module": module.strip(),
                            }
                        )
                i += 1
            continue
        i += 1
    return rows


def module_path_ok(feeder: str, module: str) -> tuple[bool | None, str]:
    """
    Returns (ok, detail).
    ok None = not applicable (script path or action text).
    """
    mod = module.strip()
    if not mod or mod.lower() in ("—", "-", "n/a"):
        return None, "no module"
    # script references
    if ".py" in mod or "scripts/" in mod or "see " in mod.lower():
        # try extract path under orchestrator
        m = re.search(r"([\w./-]+\.py)", mod)
        if m:
            p = ORCH / m.group(1) if not m.group(1).startswith("/") else Path(m.group(1))
            if not p.is_file():
                p = ORCH / "scripts" / Path(m.group(1)).name
            return (p.is_file(), str(p))
        return None, "action/script note"
    # pure module slug
    slug = mod.split()[0].strip("`")
    if "/" in slug or " " in mod and "engine" not in mod:
        # still try modules/
        pass
    feeder_dir = SKILLS / feeder
    candidates = [
        feeder_dir / "references" / "modules" / slug,
        feeder_dir / "modules" / slug,
        feeder_dir / "references" / slug,
    ]
    for c in candidates:
        if c.is_dir() or c.is_file():
            return True, str(c.relative_to(SKILLS))
    # module might only be logical name without folder yet
    return False, f"no modules/{slug} under {feeder}"


def audit() -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not PHRASE.is_file():
        return {
            "ts": ts,
            "error": "phrase_routes.md missing",
            "rows": [],
            "gaps": 1,
            "ok": 0,
        }

    rows_in = parse_phrase_routes(PHRASE.read_text(encoding="utf-8"))
    results = []
    gaps = 0
    ok_n = 0
    for r in rows_in:
        feeder = r["feeder"]
        feeder_path = SKILLS / feeder
        feeder_ok = feeder_path.is_dir() and (feeder_path / "SKILL.md").is_file()
        mod_ok, mod_detail = module_path_ok(feeder, r["module"])
        gap = False
        issues = []
        if not feeder_ok:
            gap = True
            issues.append("feeder_missing")
        if mod_ok is False:
            # module missing is warning/gap for structure but not always critical
            issues.append("module_path_missing")
            # treat as gap for inventory honesty
            gap = True
        if gap:
            gaps += 1
        else:
            ok_n += 1
        results.append(
            {
                **r,
                "feeder_ok": feeder_ok,
                "module_ok": mod_ok,
                "module_detail": mod_detail,
                "gap": gap,
                "issues": issues,
            }
        )

    return {
        "ts": ts,
        "phrase_routes": str(PHRASE),
        "row_count": len(results),
        "ok": ok_n,
        "gaps": gaps,
        "rows": results,
    }


def write_outputs(data: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "commands_inventory.json").write_text(
        json.dumps(data, indent=2), encoding="utf-8"
    )
    lines = [
        "# COMMANDS_INVENTORY — phrase_routes audit",
        f"**Updated**: {data['ts']}",
        f"**Rows**: {data.get('row_count', 0)} · **OK**: {data.get('ok', 0)} · **Gaps**: {data.get('gaps', 0)}",
        "",
        "| Section | Feeder | Feeder OK | Module | Module OK | Issues |",
        "|---------|--------|-----------|--------|-----------|--------|",
    ]
    for r in data.get("rows", []):
        lines.append(
            "| {section} | {feeder} | {feeder_ok} | {module} | {module_ok} | {issues} |".format(
                section=r.get("section", "")[:40],
                feeder=r["feeder"],
                feeder_ok="yes" if r["feeder_ok"] else "NO",
                module=(r.get("module") or "")[:40].replace("|", "/"),
                module_ok=(
                    "yes"
                    if r["module_ok"] is True
                    else ("n/a" if r["module_ok"] is None else "NO")
                ),
                issues=",".join(r.get("issues") or []) or "—",
            )
        )
    lines.append("")
    (OUT_DIR / "COMMANDS_INVENTORY.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT_DIR / "REGISTRY.md").write_text(
        f"# commands inventory registry\n\n- latest: COMMANDS_INVENTORY.md\n- json: commands_inventory.json\n- updated: {data['ts']}\n",
        encoding="utf-8",
    )
    (OUT_DIR / "SCHEMA.md").write_text(
        "# commands inventory schema\n\nSource: phrase_routes.md tables.\n"
        "Gap if feeder skill missing or module path missing (when module is a slug).\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit phrase_routes command surface")
    ap.add_argument("--print", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    data = audit()
    if not args.no_save:
        write_outputs(data)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Command protocol audit — {data.get('ts')}")
        print(f"Rows: {data.get('row_count', 0)} | OK: {data.get('ok', 0)} | Gaps: {data.get('gaps', 0)}")
        if data.get("error"):
            print("ERROR:", data["error"])
        gap_rows = [r for r in data.get("rows", []) if r.get("gap")]
        if gap_rows:
            print("Gaps:")
            for r in gap_rows[:30]:
                print(
                    f"  - [{r.get('section','')}] {r['feeder']} / {r.get('module','')}: {','.join(r.get('issues') or [])} ({r.get('module_detail','')})"
                )
            if len(gap_rows) > 30:
                print(f"  ... {len(gap_rows) - 30} more")
        else:
            print("All phrase_routes feeders/modules resolved (or n/a).")
        if not args.no_save:
            print(f"[saved] {OUT_DIR / 'COMMANDS_INVENTORY.md'}")

    return 1 if data.get("gaps", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())

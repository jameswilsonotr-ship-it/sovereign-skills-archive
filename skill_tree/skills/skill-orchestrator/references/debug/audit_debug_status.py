#!/usr/bin/env python3
"""
Orchestrator audit: harvest envelope/DEBUG_STATUS signals and summarize
opted-in skills' debug posture. Optional progress for multi-skill scan.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# Reuse harvest logic if present
_HARVEST = Path(__file__).resolve().parent / "envelope_harvest.py"
if _HARVEST.exists():
    sys.path.insert(0, str(_HARVEST.parent))
    from envelope_harvest import harvest_from_text, render_status_table, empty_row  # type: ignore
else:
    def empty_row(skill_name: str) -> dict:
        return {"skill_name": skill_name, "mode": "idle", "last_outcome": None,
                "last_outcome_at": None, "contract_version": None, "active_item": None}

    def harvest_from_text(text, table=None):
        return table or {}

    def render_status_table(table):
        return "(harvest module missing)"


OPTED_IN = [
    "grok-imagine-generate-engine",
    "grok-imagine-overlay-engine",
    "chaos-bratz-roster",
    "format-bible",
]

SKILLS_ROOT = Path("/home/workdir/.grok/skills")


def progress_bar(i: int, n: int, width: int = 10) -> str:
    pct = (i / n) if n else 1.0
    filled = int(round(pct * width))
    return f"[{'█' * filled}{'░' * (width - filled)}] {int(pct * 100)}% audit"


def read_optional(path: Path, limit: int = 8000) -> str:
    try:
        return path.read_text()[:limit]
    except Exception:
        return ""


def audit(skills_root: Path = SKILLS_ROOT) -> str:
    table: Dict[str, dict] = {}
    n = len(OPTED_IN)
    lines_out: List[str] = []

    # Only harvest live signals from debugging_notes / TODO / explicit status files.
    # Do NOT feed schema/docs that contain example front-matter syntax.
    for i, name in enumerate(OPTED_IN, start=1):
        lines_out.append(progress_bar(i, n) + f"  {name}")
        root = skills_root / name
        row = empty_row(name)
        candidates = [
            root / "references/dual-engine-test/debugging_notes.md",
            root / "references/debugging_notes.md",
            root / "debugging_notes.md",
            root / "TODO.md",
            root / "debug_status.yaml",
        ]
        blob = ""
        for c in candidates:
            if c.exists():
                blob += "\n" + read_optional(c)
                if "debugging_notes" in str(c):
                    try:
                        row["notes_path"] = str(c.relative_to(root))
                    except ValueError:
                        row["notes_path"] = str(c)
        if blob:
            table = harvest_from_text(blob, table)
        if name not in table:
            table[name] = row
        # Presence-based mode defaults (only if still the empty default)
        cur_mode = table[name].get("mode")
        if cur_mode in (None, "idle"):
            if name == "format-bible":
                table[name]["mode"] = "envelope-owner"
            elif name == "chaos-bratz-roster":
                table[name]["mode"] = "boot-emitter"
            else:
                table[name]["mode"] = "idle"
        table[name]["contract_version"] = table[name].get("contract_version") or "0.2.0"
        if name in ("grok-imagine-generate-engine", "grok-imagine-overlay-engine"):
            if (root / "references/dual-engine-test/debugging_notes.md").exists():
                table[name]["notes_path"] = table[name].get("notes_path") or "references/dual-engine-test/debugging_notes.md"

    # Persist the table for natural-language "debug status"
    status_path = Path(__file__).resolve().parent / "status_table.md"
    table_md = render_status_table(table)
    status_path.write_text(
        f"# Debug Status Table (auto-updated by audit)\n"
        f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f"**Contract**: olivia-dev-alpha DEBUG_MODE_CONTRACT 0.2.0\n"
        f"**Envelope**: format-bible ENVELOPE_SCHEMA 1.1.0\n\n"
        f"{table_md}\n"
    )

    lines_out.append("")
    lines_out.append("## Debug status table")
    lines_out.append(table_md)
    lines_out.append("")
    lines_out.append(f"Audit time: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines_out.append("Contract: olivia-dev-alpha DEBUG_MODE_CONTRACT 0.2.0; Envelope: format-bible ENVELOPE_SCHEMA 1.1.0")
    lines_out.append(f"Persisted: {status_path}")
    return "\n".join(lines_out)


if __name__ == "__main__":
    print(audit())

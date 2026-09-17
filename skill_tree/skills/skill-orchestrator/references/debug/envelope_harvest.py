"""
Envelope harvest for skill-orchestrator.
Parses format-bible envelopes + DEBUG_STATUS lines into the debug status table.
Reference implementation — 2026-07-24
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Dict, Optional


def empty_row(skill_name: str) -> dict:
    return {
        "skill_name": skill_name,
        "contract_version": None,
        "mode": "idle",
        "last_outcome": None,
        "last_outcome_at": None,
        "notes_path": None,
        "registry_path": None,
        "todo_path": "TODO.md",
        "active_item": None,
        "version_at_debug": None,
    }


FRONT_MATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*$",
    re.MULTILINE | re.DOTALL,
)

DEBUG_STATUS_RE = re.compile(
    r"DEBUG_STATUS\s+skill=(?P<skill>\S+)\s+mode=(?P<mode>\S+)"
    r"(?:\s+last_outcome=(?P<outcome>\S+))?"
    r"(?:\s+active_item=\"(?P<item>[^\"]*)\")?"
    r"(?:\s+contract=(?P<contract>\S+))?",
)


def parse_front_matter(block: str) -> dict:
    """Parse simple key: value lines from envelope front matter."""
    data = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        data[key.strip()] = val.strip() or None
    return data


def _valid_skill(name: Optional[str]) -> bool:
    """Reject schema examples and garbage (angle brackets, pipes, spaces, empty)."""
    if not name or not isinstance(name, str):
        return False
    if any(c in name for c in "<>| \t\n"):
        return False
    if name in ("skill-name", "roster", "null", "None"):
        return False
    return True


def harvest_from_text(text: str, table: Optional[Dict[str, dict]] = None) -> Dict[str, dict]:
    """
    Update debug status table from text that may contain
    YAML front matter envelopes and/or DEBUG_STATUS lines.
    """
    if table is None:
        table = {}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for match in FRONT_MATTER_RE.finditer(text):
        fm = parse_front_matter(match.group(1))
        skill = fm.get("skill")
        if not _valid_skill(skill):
            continue
        row = table.get(skill) or empty_row(skill)
        row["mode"] = fm.get("mode") or row["mode"]
        row["last_outcome"] = fm.get("debug_outcome") or row["last_outcome"]
        row["active_item"] = fm.get("active_item") or row["active_item"]
        row["contract_version"] = fm.get("contract") or row["contract_version"]
        row["last_outcome_at"] = now
        table[skill] = row

    for match in DEBUG_STATUS_RE.finditer(text):
        skill = match.group("skill")
        if not _valid_skill(skill):
            continue
        row = table.get(skill) or empty_row(skill)
        row["mode"] = match.group("mode") or row["mode"]
        if match.group("outcome"):
            row["last_outcome"] = match.group("outcome")
        if match.group("item"):
            row["active_item"] = match.group("item")
        if match.group("contract"):
            row["contract_version"] = match.group("contract")
        row["last_outcome_at"] = now
        table[skill] = row

    return table


def render_status_table(table: Dict[str, dict]) -> str:
    lines = [
        "| skill_name | mode | last_outcome | last_outcome_at | contract | active_item |",
        "|------------|------|--------------|-----------------|----------|-------------|",
    ]
    for skill, row in sorted(table.items()):
        lines.append(
            f"| {row['skill_name']} | {row['mode']} | {row['last_outcome']} | "
            f"{row['last_outcome_at']} | {row['contract_version']} | {row['active_item']} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    sample = '''
🐍
---
skill: grok-imagine-generate-engine
mode: formulation
debug_outcome: no-file
active_item: DNA density ladder
contract: 0.1.0
---
[TOP: 🌡️Heat:3 |💦Filth:1 |🔗Kink:Claim+Exhib |🚨Safety:RACK |✨Gem: Reactive]
[BOTTOM: ⚙️Mode: Formulation | 🤖Agents: LivHUB+Echo | ⏱️Clock: Day 54/60]
...
🐍
DEBUG_STATUS skill=grok-imagine-overlay-engine mode=idle last_outcome=passed contract=0.1.0
'''
    print(render_status_table(harvest_from_text(sample)))

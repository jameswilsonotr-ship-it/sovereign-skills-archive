# Envelope Harvest — Orchestration Code Example
**Version**: 0.1.0 — 2026-07-24  
**Owner**: skill-orchestrator  
**Depends on**: format-bible `ENVELOPE_SCHEMA.md`, `DEBUG_STATUS_SCHEMA.md`

This is reference logic for how the orchestrator observes speaking skills. Not a mandatory runtime binary — it documents the intended harvest path so future sessions implement the same behavior.

## Example envelope emitted by a speaking skill

```text
🐍
---
skill: grok-imagine-generate-engine
mode: formulation
heat: 3
filth: 1
clock: Day 54/60
debug_outcome: no-file
active_item: DNA density ladder
contract: 0.1.0
---
[TOP: 🌡️Heat:3 |💦Filth:1 |🔗Kink:Claim+Exhib |🚨Safety:RACK |✨Gem: Reactive]
[BOTTOM: ⚙️Mode: Formulation | 🤖Agents: LivHUB+Echo | ⏱️Clock: Day 54/60]

... body ...

🐍
```

## Example one-liner status (optional parallel signal)

```text
DEBUG_STATUS skill=grok-imagine-generate-engine mode=formulation last_outcome=no-file active_item="DNA density ladder" contract=0.1.0
```

## Harvest pseudocode (orchestrator)

```python
import re
from datetime import datetime, timezone

# Global table row shape (see DEBUG_STATUS_SCHEMA.md)
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
    """Parse simple key: value YAML-ish front matter from an envelope."""
    data = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        data[key.strip()] = val.strip() or None
    return data

def harvest_from_text(text: str, table: dict[str, dict]) -> dict[str, dict]:
    """
    Update debug status table from assistant text that may contain
    envelopes and/or DEBUG_STATUS lines.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1) Front matter envelopes
    for match in FRONT_MATTER_RE.finditer(text):
        fm = parse_front_matter(match.group(1))
        skill = fm.get("skill")
        if not skill:
            continue
        row = table.get(skill) or empty_row(skill)
        row["mode"] = fm.get("mode") or row["mode"]
        row["last_outcome"] = fm.get("debug_outcome") or row["last_outcome"]
        row["active_item"] = fm.get("active_item") or row["active_item"]
        row["contract_version"] = fm.get("contract") or row["contract_version"]
        row["last_outcome_at"] = now
        table[skill] = row

    # 2) One-liner DEBUG_STATUS
    for match in DEBUG_STATUS_RE.finditer(text):
        skill = match.group("skill")
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

def render_status_table(table: dict[str, dict]) -> str:
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


# --- Example usage during `debug status` / audit ---
if __name__ == "__main__":
    table = {}
    sample_turn = '''
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
    table = harvest_from_text(sample_turn, table)
    print(render_status_table(table))
```

## Expected example output

```text
| skill_name | mode | last_outcome | last_outcome_at | contract | active_item |
|------------|------|--------------|-----------------|----------|-------------|
| grok-imagine-generate-engine | formulation | no-file | 2026-07-24T... | 0.1.0 | DNA density ladder |
| grok-imagine-overlay-engine | idle | passed | 2026-07-24T... | 0.1.0 | None |
```

## Integration notes
- On natural language `debug status` / `who is debugging` / inventory audit: run harvest over recent relevant turns (or over any `debug_status.yaml` files skills elect to write).
- Persist the table under skill-orchestrator references (e.g. `references/debug/status_table.md`) if durable state is needed across sessions.
- Do not re-implement per-skill debug logic here — only observe the envelope.

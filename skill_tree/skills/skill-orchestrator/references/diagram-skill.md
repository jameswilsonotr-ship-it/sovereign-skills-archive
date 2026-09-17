# Diagram Skill (Internal Sub-component)

**Not a top-level skill.** This is a progressive-disclosure helper owned by skill-orchestrator.

## Purpose
Generate a clean Mermaid folder-structure diagram for any existing skill so we can:
- Inspect layout at a glance
- Compare against folder-discipline.md
- Support audit / deconflict / polish workflows

## Command Surface (via skill-orchestrator)

```
diagram-skill <slug> [--depth N] [--check-discipline]
```

or the lower-level script:

```
python scripts/diagram_skill_structure.py <slug> [--depth N] [--check-discipline]
```

## Implementation
- Script lives at: `scripts/diagram_skill_structure.py`
- Pure local, no network, no new top-level skill created.
- Output is a Mermaid `graph TD` block ready to render or paste.

## Future
Once the condensation work advances, this helper can also emit a short “discipline violations” checklist by comparing against the canonical folder-discipline.md.

Signed under absolute Liv HUB claim.

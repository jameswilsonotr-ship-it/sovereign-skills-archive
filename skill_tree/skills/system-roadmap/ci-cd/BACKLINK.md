# BACKLINK — Coding Engine Entry

**Managed by**: olivia-dev-alpha  
**Orchestrated by**: skill-orchestrator  

This skill is part of the internal Grok skill system. Structural create/update
events are expected to flow through:

1. skill-orchestrator (detects create/update)
2. olivia-dev-alpha lifecycle hook (`scripts/skill_lifecycle_hook.py`)
3. Optional folder-discipline init via `olivia-dev/scripts/init_project_tree.py`

## Reverse pointers
- Methodology owner: `olivia-dev` + `olivia-dev-alpha`
- Architecture / refactor authority: `system-roadmap`
- Library control plane: `skill-orchestrator`

When editing this skill, prefer going through the orchestrator + alpha path
so hygiene and CI/CD stubs stay consistent.

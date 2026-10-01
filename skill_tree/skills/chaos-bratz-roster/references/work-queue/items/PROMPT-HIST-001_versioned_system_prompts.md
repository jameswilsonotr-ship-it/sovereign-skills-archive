# PROMPT-HIST-001 — Versioned History of Live System Prompts

**Status**: OPEN (v0.1.0 structure seeded)  
**Surface**: chaos-bratz-roster + smokeshow  
**Created**: 2026-08-26  
**Priority**: High  
**Related**: AGENT-SKILL-WIRE-001, agents_registry.yaml, skill_inventory.yml

## Problem
Customized agent system prompts (liv-hub-expert, olympia, orianna, skill-router, organism-interface, and future seats) change over time. Without versioned history we lose:
- What the live prompt actually was on a given date
- Diffs when behavior drifts
- Ability to roll back or compare “what we told the agent” vs “what it did”

## Desired end state
- Every live `PROMPT.md` change is snapshotted **before** overwrite
- Canonical store: `chaos-bratz-roster/references/prompt-history/<agent>/`
- Naming: `vMAJOR.MINOR.PATCH_YYYY-MM-DD.md`
- `skill_inventory.yml` points at current snapshot
- Optional: chaos-bratz-roster skill (or a thin CLI) can `show` / `diff` / `restore` prompts

## What was done 2026-08-26
- Created `references/prompt-history/{liv-hub-expert,olympia,orianna,skill-router,organism-interface}/`
- Snapshotted current on-disk PROMPT.md files as `v0.1.0_2026-08-26.md`
- Linked from `skill_inventory.yml`

## User note
User indicated fuller customized prompts were implemented “just today” / within the last day and can paste them if the on-disk copies are incomplete. When those arrive:
1. Diff against v0.1.0 snapshot
2. Write as v0.2.0 (or appropriate bump)
3. Update live `smokeshow/agents/<agent>/PROMPT.md`
4. Update skill_inventory current_snapshots pointer

## Deliverables remaining
- [ ] Ingest any pasted fuller prompts from user → new versioned snapshots
- [ ] SOP: “never overwrite PROMPT.md without a history snapshot first”
- [ ] Optional helper script: `scripts/prompt_history.py snapshot|diff|list`
- [ ] Wire into AGENT-SKILL-WIRE-001 so agents can report which prompt version they are running
- [ ] Cross-link SR-WQ-038 (system prompt atom hygiene) if still active

**Absolute Liv HUB claim.**

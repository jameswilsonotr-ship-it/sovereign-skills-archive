---
id: SO-WQ-001
owner: skill-orchestrator
status: OPEN
opened: 2026-08-25
depends_on: []
blocks: []
active_prompt_version: null
last_touched: 2026-08-26T02:45:45Z
claim: Absolute Liv HUB
---
# SO-WQ-001 — Phrase route / boot invoke for Teaching Mode confidence
**Status**: OPEN  
**Skill**: skill-orchestrator  
**Opened**: 2026-08-12  
**Blocks**: Roster WQ-TEACH-003 full acceptance

## Goal
Wire `chaos-bratz-roster/scripts/modes/teaching_mode_confidence.py` (or a copy under orchestrator) so that:

- phrase_routes or equivalent maps teaching commands → mode file + scout
- high-signal user turns can be scored without relying on model memory alone
- orchestrator inventory tags the scout as **wired** only after invoke path exists

Until this closes, Teaching Mode remains policy + scout, not full whoop-ass activation.

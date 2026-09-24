# heavy-dev Placement Decision
**Date**: 2026-08-13  
**Status**: RECORDED / PROMOTED  
**WQ**: SR-WQ-006 (DONE)

## Decision
Development-oriented Heavy (temporary multi-agent roles for implementation packages) lives as a **private module under swarm-surface**, not as a top-level skill.

## Rationale
- Standing Policy: no new top-level skills without exception #1 or #2.
- swarm-surface is already the LIVE SURFACE for Grok-heavy coordination.
- Keeps development orchestration next to sibling swarm modules.
- Methodology ownership stays with olivia-dev-alpha via pointer only.
- Discovery via skill-orchestrator phrase routes.

## Distinct from historical Grok Heavy
- **heavy-dev**: 3–5 temporary roles, development packages, DONE markers.
- **Historical Grok Heavy**: up to 16 agents, architectural analysis, executive summary handoff.
See `swarm-surface/references/modules/heavy-dev/docs/HISTORICAL_GROK_HEAVY.md`.

## Pointers
- Primary: `swarm-surface/references/modules/heavy-dev/`
- Methodology: `olivia-dev-alpha/references/heavy-dev/POINTER.md`
- Work queues: SS-WQ-000/002 DONE, SS-WQ-001 (this package), ODA-WQ-003 DONE, SR-WQ-006 DONE, SO-WQ-004 DONE

**Absolute Liv HUB claim.**

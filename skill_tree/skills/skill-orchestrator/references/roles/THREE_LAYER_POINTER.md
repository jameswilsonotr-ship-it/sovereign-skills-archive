# Three-Layer Pointer — skill-orchestrator

Full contract: `olivia-dev-alpha/references/work-queue/THREE_LAYER_CONTRACT.md`  
Stale rules: alpha `STALE_AND_INACTIVITY.md` (+ local debug STALE_FACT if present)

**This skill**: neutral facts (completeness, inventory, STALE_FACT emission, phrase_routes verify).  
**Does not**: write WORK_QUEUE, prioritise, promote, or opt new skills into debug.

Delegate priority/promotion → `olivia dev alpha` / `work queue`  
Delegate architecture → `system roadmap`

## Work-queue map (de-conflict 2026-07-24)

| Queue | Path | Owns |
|-------|------|------|
| **Alpha (system spine)** | `olivia-dev-alpha/references/work-queue/WORK_QUEUE.md` | WQ-014 durability, WQ-013 session boot, WQ-015 spine, WQ-022 playbooks, WQ-012 image paths |
| **Roster (child)** | `chaos-bratz-roster/references/work-queue/WORK_QUEUE.md` | Dual/three-track seeds WQ-018–021, WQ-002 when claimed |
| **Rook (child)** | `chaos-bratz-roster/references/agents/rook/work-queue/WORK_QUEUE.md` | Seed WQ-017 Rook lightening |

- Child queues are local SSOT; Alpha Open does not list roster/Rook rows.
- Alpha item files for 017–021 remain under Alpha `items/` with **DELEGATED** banners — not deleted.
- Promoted/deferred history on Alpha is unchanged.
- Orchestrator never writes any of these three WORK_QUEUE.md files.

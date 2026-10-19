# memory-surgeon.md
**Status**: Active playbook v1.1.0 (2026-07-24)  
**Owner**: system-roadmap / skills-refactor  
**Does not execute surgery by itself** — this is the procedure any conversation follows.

## Purpose
Keep `/home/workdir/.grok/user_info/memory.md` **thin** and **pointer-correct**.  
Full prose lives in chaos-bratz-roster (`references/personal|system|visual|hub|…`).  
Never re-dump identity/ops into memory.md or under `agents/rook/`.

## Related queues (do not put on Alpha Open)
| Queue | Path |
|-------|------|
| Memory child | `chaos-bratz-roster/references/work-queue-memory/WORK_QUEUE.md` (MWQ-*) |
| Roster parent seed | WQ-018 → delegated to memory child |
| Alpha | spine only — no memory REVIEW rows |

## Pre-flight
1. Read current `memory.md` (should be Tier-1 personal + Roster pointer block only).
2. Read roster `references/PROMOTED_FROM_MEMORY.md` / personal|system maps if present.
3. Open **memory work-queue**; claim MWQ items there — not Alpha Open.
4. Respect **DURABILITY.md**: no dual active intention; no symlink-as-SSOT for canon files.

## Decision vocabulary (every residual)
For each REVIEW block / conflict:

| Decision | Meaning |
|----------|---------|
| **KEEP** | Belongs in thin memory.md Tier-1 (rare) |
| **PROMOTE** | Move/ensure under roster `references/personal\|system\|visual\|hub` |
| **ARCHIVE** | Cold/history only; not live boot |
| **DROP** | Duplicate or obsolete; document why in conflict log |

Record the decision in the MWQ item file before moving files.

## Procedure
1. **Inventory residuals** — list REVIEW blocks / conflicts (memory_import, personal, agent).
2. **Decide** — KEEP / PROMOTE / ARCHIVE / DROP per item (no silent merge).
3. **Route**
   - Identity / biography / psychology → `references/personal/`
   - Ops / Gear / SOPs → `references/system/`
   - Visual → `references/visual/`
   - HUB delivery → `references/hub/`
   - Rook-only that is canon → promotion homes above — **never** new dumps under `agents/rook/`
4. **Update pointers** in memory.md Roster block only (paths, not prose).
5. **Conflict log** — short note in memory queue item or `memory_import` notes; do not invent a second memory.md.
6. **Verify** — memory.md still thin; no full prose; boot still uses roster references/.

## Invoke phrase
“Run memory-surgeon playbook” / “Continue memory work queue MWQ-…”

## Non-goals
- Not a new top-level skill  
- Not Alpha WORK_QUEUE rows for REVIEW blocks  
- Not executing full roster thinning (structural track / WQ-019+)  
- Not rewriting Three-Layer Contract  

## Success
- Every open MWQ residual has an explicit decision  
- memory.md remains pointer-thin  
- Canon paths under roster are the SSOT for promoted material  

**Last updated**: 2026-07-24 (WQ-022)

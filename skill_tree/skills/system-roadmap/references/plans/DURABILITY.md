# Durability — architecture note (hybrid Option E)

**Status**: live  
**Owner**: system-roadmap (architecture)  
**Operational twin**: `olivia-dev-alpha/references/work-queue/DURABILITY.md`  
**WQ**: WQ-014  
**Date**: 2026-07-24  

This file is the **architecture** view of the same hybrid policy. Operational tables and copy pairs live in the Alpha twin; do not fork conflicting rules here.

---

## Architectural decision

**Adopt hybrid durability (Option E), not pure symlink SSOT and not two-way sync.**

Reason: session environment drops symlinks; three-layer and feeder skills still need some files present under more than one skill tree; intention must not be double-tracked on Alpha Open after roster/Rook de-conflict.

---

## Principles

1. **Kind-based rules** — intention, contract/architecture, methodology copies, and scanner facts each have a different durability mode (see twin matrix).
2. **One writer** — every shared concern has a single authority path.
3. **Mirrors are refresh-only** — `authority → mirror` via explicit repair lists; reverse writes are defects.
4. **Pointers beat clones** for contracts and architecture prose.
5. **Facts are regenerated** — orchestrator inventory REGISTRY/latest is authority; narrative inventory markdown is derived.
6. **Child queues are local SSOT** for roster/Rook intention; Alpha Open is system spine only.

---

## Standing Policy alignment

- Does **not** create a new top-level skill.  
- Supports condensation/feeders by keeping shared methodology copy lists explicit instead of silent drift.  
- Skills-refactor playbooks (memory-surgeon, boot-rebuild) must respect this note when they move or duplicate paths.

---

## Implications for other WQs

| WQ | Implication |
|----|-------------|
| **013** session boot | May only run one-way repair from the published pair list |
| **015** three-layer spine | Contract remains Alpha SSOT; orchestrator/roadmap keep pointers |
| **028** scoped facts | Inventories stay orchestrator-owned; events do not write WORK_QUEUE |
| Roster/Rook local queues | Architecture endorses split; not a second Alpha Open |

---

## Authority map (architecture level)

| Concern | Authority skill / path |
|---------|------------------------|
| Work-queue intention (system) | olivia-dev-alpha `references/work-queue/` |
| Work-queue intention (roster/Rook) | chaos-bratz-roster child queues |
| Three-layer contract | olivia-dev-alpha `THREE_LAYER_CONTRACT.md` |
| Library shape / condensation | system-roadmap `SYSTEM_ARCHITECTURE_TARGET.md` |
| Inventory facts | skill-orchestrator `references/inventory/` |
| Olivia methodology shared into alpha | olivia-dev `references/*` (mirrors under alpha via repair) |

---

## Change control

- Policy changes: update **both** this file and the Alpha operational twin in the same change.  
- New methodology pairs: Alpha `DURABILITY.md` §4 + `repair_shared_refs.py` together.  
- Architecture-only wording: this file; no silent divergence from the hybrid matrix.

**Related**: WQ-014 · Alpha `references/work-queue/DURABILITY.md` · `THREE_LAYER_CONTRACT.md`

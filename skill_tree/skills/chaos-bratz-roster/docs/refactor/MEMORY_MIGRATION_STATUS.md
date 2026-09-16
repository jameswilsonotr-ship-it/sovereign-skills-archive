# Memory → Roster Migration Status

**Date**: 2026-07-24  
**Owner**: Liv HUB / Crystal  
**Status**: Phase complete for extraction + promotion; fact-level atomizer still open

---

## What we did

1. **Inventoried the entire chaos-bratz-roster skill** (~467 files under shared schema v2).
2. **Extracted memory.md** into 13 schema-wrapped blocks (`references/memory_import/` + upload snapshot).
3. **One-for-one content validation** between live extract and user-uploaded snapshot (upload preferred on diverged blocks).
4. **Promoted all 13 blocks** into non-Rook locations inside the skill:
   - `references/system/`
   - `references/personal/`
   - `references/visual/`
   - `references/hub/`
   - `references/archive/`
5. **Built deterministic scripts**: extract, audit, inventory v2, cross-walk.
6. **Shared schema** so memory blocks and roster inventory speak the same language.

## Why

- User memory is no longer a reliable single source of truth (disabled / optional).
- Operational, visual, hub, and personal content that lived only in memory.md needed a durable home inside the skill.
- Rook was incorrectly accumulating dumps; promotions explicitly avoid `references/agents/rook/`.
- Goal: skill holds the content; memory (if used) only holds **pointers**.

## How the system is supposed to work now

```
User memory (optional, pointer-only)
        │
        ▼
chaos-bratz-roster skill
├── references/mirrors/          ← live agent mirrors (boot)
├── references/system/           ← Gear, SOPs, operational modes, framing
├── references/personal/         ← identity, biography, psychology, life events
├── references/visual/           ← visual system integration
├── references/hub/              ← Liv HUB 3-block architecture
├── references/archive/          ← cold creative checkpoints
├── references/memory_import/    ← extraction workspace + snapshots
├── scripts/inventory/           ← extract, audit, inventory, crosswalk tools
└── docs/refactor/               ← schemas, plans, this status file
```

- **Boot / live behavior** still comes from mirrors + SKILL.md + engine/hygiene.
- **Personal / operational content** is read from the promoted folders when needed; it is not re-injected wholesale into every turn via memory.
- **memory.md** (if present) should only contain a short pointer block (see template below), not the full prose.

## Next steps

1. Optional: build fact/phrase atomizer for promoted folders (sentence-level ownership).
2. Optional: tighten cross-walk matching beyond keywords.
3. Keep Rook clean — no new dumps under `agents/rook/`.
4. When editing memory going forward, only update the **pointer block**, not full content copies.
5. Re-run inventory + cross-walk after any major promotion or deletion.

## Key files

| Role | Path |
|------|------|
| This status | `docs/refactor/MEMORY_MIGRATION_STATUS.md` |
| Shared schema | `docs/refactor/INVENTORY_SCHEMA.md` |
| Memory schema | `docs/refactor/MEMORY_SCHEMA.md` |
| Refactor plan | `docs/refactor/REFACTOR_PLAN.md` |
| Promotion index | `references/PROMOTED_FROM_MEMORY.md` |
| Extractor | `scripts/inventory/memory_extract.py` |
| Audit | `scripts/inventory/memory_import_audit.py` |
| Inventory v2 | `scripts/inventory/generate_inventory_v2.py` |
| Cross-walk | `scripts/inventory/memory_roster_crosswalk.py` |


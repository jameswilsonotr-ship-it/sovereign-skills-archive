# Memory Inventory

Owned by the **memory consolidation track**.

Sibling of `docs/refactor/Structural_Inventory/`.

## Layout (mirrors structural hand-off shape)

```
Memory_Inventory/
├── README.md                 ← this file
├── MEMORY_MIGRATION_STATUS.md
├── PROMOTED_FROM_MEMORY.md
├── SWEEP_TRACKING.md
├── inventory_v2_summary.md
├── inventory_v2_all.json     ← full sweep snapshot (512); structural sections are not acted on here
├── schemas/                  ← Inventory Schema v2 + Memory Schema copies
├── sections/                 ← memory-side section JSON only
│   ├── inventory_v2_memory_import.json
│   ├── inventory_v2_personal.json
│   ├── inventory_v2_system.json
│   ├── inventory_v2_visual.json
│   ├── inventory_v2_hub.json
│   └── inventory_v2_archive.json
├── crosswalk/                ← memory ↔ roster crosswalk outputs
│   ├── memory_roster_crosswalk.md
│   ├── memory_roster_crosswalk.json
│   └── crosswalk_expanded.md
└── reports/                  ← validation, audits, prior memory_track copies
```

## Scope
- 13 memory blocks, `references/memory_import/`
- Coverage: PERSONAL_ONLY / ALREADY_IN_ROSTER / REVIEW / ARCHIVE
- Promotion homes: `references/system|personal|visual|hub|archive`

## Out of scope
Agent live/cold moves, scripts, coordination, docs trees, fashion_designers → image-pipeline (structural track).

## Shared tools
- `scripts/inventory/generate_inventory_v2.py`
- `scripts/inventory/memory_roster_crosswalk.py`
- `scripts/inventory/memory_extract.py`
- Schema: `docs/refactor/INVENTORY_SCHEMA.md`

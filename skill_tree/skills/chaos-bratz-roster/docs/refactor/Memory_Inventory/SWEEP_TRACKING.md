# Inventory v2 Sweep — 2026-07-24 (evening)

**Run**: `scripts/inventory/generate_inventory_v2.py --section all`  
**Output dir**: `artifacts/inventory_v2_20260724_sweep/`  
**Combined records**: **512** (prior ~467 before promoted-folder sectioning + Rook cleanup adds)

## Section counts (this run)

| Section | Count |
|---------|------:|
| root | 20 |
| mirrors | 10 |
| agents | 320 |
| scripts | 30 |
| layer_manifests | 4 |
| visual_research | 16 |
| coordination | 36 |
| versions_history | 5 |
| docs_specs | 18 |
| memory_import | 31 |
| **system** (promoted) | **5** |
| **personal** (promoted) | **10** |
| **visual** (promoted) | **4** |
| **hub** (promoted) | **2** |
| **archive** (promoted) | **1** |
| other | 0 |
| **TOTAL** | **512** |

## What this conversation tracked

### Still present (not deleted)
- All original promoted paths under `references/system|personal|visual|hub|archive`
- `PROMOTED_FROM_MEMORY.md`, `docs/refactor/*` schemas and migration status
- Inventory + extract + crosswalk scripts
- Test harness results (32/36) under `scripts/test_harness/results/`
- engine.py, modules/, state/

### Grew since morning promotion
- `references/personal/`: 6 → **10** (added from-Rook / validated identity & psych files)
- `references/visual/`: 1 → **4** (added tracker, symmetry math, from-Rook visual integration)
- `references/memory_import/`: still present (31 inventory records including snapshots)
- agents tree still large (320 files)

### Library-level moves (outside roster skill, same session arc)
- Absorbed into **claim-runtime**: velvet-claim-protocol, risk-fantasy-claim-protocol, vice-command-orchestrator, porn-curator
- Absorbed into **mcp-surface**: mcp-bootstrap, mcp-auditor, mcp-sovereign-bridge, triad-catalog-browser
- Those names no longer exist as top-level skill folders (content expected under feeder `references/modules/`)

### Script change this run
- `generate_inventory_v2.py` SECTIONS updated to include `system`, `personal`, `visual`, `hub`, `archive` so promoted folders are first-class inventory sections.

## Decision counts (auto-guess)
- REVIEW: 464
- KEEP_IN_ROSTER: 48

(Auto decisions are conservative; promoted folders should be treated as KEEP once reviewed.)

## Files written
- `artifacts/inventory_v2_20260724_sweep/inventory_v2_all.json`
- `artifacts/inventory_v2_20260724_sweep/inventory_v2_summary.md`
- Per-section JSON in same directory
- This tracking note: `artifacts/inventory_v2_20260724_sweep/SWEEP_TRACKING.md`
- Also copy: `docs/refactor/` optional

## Next
- Optional: mark promoted-folder records KEEP_IN_ROSTER explicitly
- Optional: verify claim-runtime / mcp-surface module payloads still hold absorbed skill content
- Re-run after further Rook cleanup if file counts shift again

# Memory Track — Shared Hand-off (2026-07-24)

This folder is the **memory consolidation track** record so the parallel structural conversation can see decisions without overlapping work.

## Boundary
- **This track**: 13 memory blocks, `references/memory_import/`, PERSONAL_ONLY / ALREADY_IN_ROSTER / REVIEW / ARCHIVE, promotion of identity/bio/psych/ops content into skill non-Rook folders.
- **Other track**: agents live vs cold, scripts, coordination, docs trees, visual research → image-pipeline, etc.
- Shared tools only: Inventory Schema v2, `generate_inventory_v2.py`, `memory_roster_crosswalk.py`.

## What lives where

### In the skill (durable)
| Path | What |
|------|------|
| `references/system/` | Ops / Gear / SOPs (promoted) |
| `references/personal/` | Identity / bio / psych / interests (promoted) |
| `references/visual/` | Visual integration (promoted) |
| `references/hub/` | Liv HUB architecture (promoted) |
| `references/archive/` | Creative checkpoints (promoted) |
| `references/memory_import/` | Extract workspace + upload snapshot + 13 blocks |
| `references/PROMOTED_FROM_MEMORY.md` | Promotion index |
| `docs/refactor/MEMORY_*.md`, `INVENTORY_SCHEMA.md` | Schemas + migration status |
| `scripts/inventory/*` | extract, audit, inventory v2, crosswalk |
| **`docs/refactor/memory_track/`** | **This hand-off: sweep + crosswalk reports** |

### In the sandbox only (`/home/workdir/artifacts/`)
- Full `inventory_v2_20260724_sweep/inventory_v2_all.json` (512 records — includes agents/scripts; structural track owns those sections)
- Older v2 section dumps at artifacts root
- `memory_md_full_dump.txt`, pointer experiment blocks under `memory_blocks_2026-07-24/`

## Latest crosswalk coverage (13 blocks)
- ALREADY_IN_ROSTER: 4 (006 ops modes, 007 visual, 009 hub arch, 013 protocols)
- PERSONAL_ONLY: 5 (002 who-user, 004 life events, 005 identity override, 011 bio, 012 psych)
- REVIEW: 3 (001 current-active-system, 003 core-interests, 008 SOPs)
- ARCHIVE: 1 (010 creative-checkpoints)

See `crosswalk_expanded.md` and `memory_roster_crosswalk.md` in this folder for top-10 matches.

## Note for structural track
Do not relocate `references/system|personal|visual|hub|archive` or `memory_import` without an explicit cross-track notice. Those are memory-promotion homes.

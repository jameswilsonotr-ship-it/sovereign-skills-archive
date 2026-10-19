# Skill Surface Crosswalk — Analysis of 40 pairs
**Date**: 2026-07-25  
**Source**: `skill_surface_crosswalk.json` (min Jaccard 0.32, limit 40, include-memory requested)

## Headline
All 40 returned pairs were **skill_vs_skill**. No skill_vs_memory pair cleared the threshold inside the limited result set. Conflicts are almost entirely **process/root prose copied into coordination docs, agent file_manifests, and layer_manifest IN_PROGRESS notes**.

## Owner-pair clusters (count)
| A owner | B owner | Count | Reading |
|---------|---------|-------|---------|
| root | queue | 7 | SKILL/TODO/CHANGELOG text also in coordination / to-do |
| queue | agent:bunny | 6 | Queue notes mirrored into bunny agent surface |
| other | docs | 5 | Wishlist/backlog prose vs docs/refactor notes |
| other | queue | 4 | Backlog ↔ coordination |
| queue | layer_manifests | 4 | Coordination hygiene notes ↔ layer_manifest IN_PROGRESS |
| root | docs | 2 | Root TODO vs structure sweep observation docs |
| queue | agent:crystal/echo/mira | 2 each | Queue text in specialist file_manifests |
| root | agent:rook / agent:echo | 1 each | SKILL boilerplate in agent history / versions |

## Hottest paths
**A-side (sources of duplicated claims)**  
- `backlog-wishlist/README.md` (11)  
- `coordination/COORDINATION_PROTOCOL.md` (9)  
- `coordination/IN_PROGRESS_Advanced_Architecture_…` (9)  
- `TODO.md` / `SKILL.md`

**B-side (receivers)**  
- coordination IN_PROGRESS files, to-do handoffs  
- `references/agents/{crystal,echo,mira}/file_manifest.md`  
- `references/layer_manifests/IN_PROGRESS_*`

## Interpretation
1. **Not identity leakage** — these are process / boot boilerplate / coordination sentences, not personal/psych dumps into Rook.
2. **Expected duplication** — SKILL.md and coordination notes are intentionally referenced in multiple places; score 1.0 often means identical short sentences.
3. **Actionable subset** — worth cleaning later:
   - Agent `file_manifest.md` files that paste queue hygiene paragraphs (crystal/echo/mira)
   - Layer_manifest IN_PROGRESS notes that duplicate coordination protocol text
4. **Non-action** — root SKILL ↔ agent history “Gutter Mode and C-64 borders enforced” style lines can stay; they are intentional consistency anchors.

## Recommendation
- No emergency merge.
- Optional follow-up (Structural or Roster, not Memory residual): thin agent file_manifests and layer_manifest IN_PROGRESS files so they *point* at coordination sources instead of pasting them.
- Memory track does **not** own that cleanup; dual-track boundary holds.

## Dual-cloud awareness
Both clouds are now documented at equal specificity in:
- `docs/refactor/Memory_Inventory/ATOM_CLOUDS.md`
- `scripts/inventory/README.md`

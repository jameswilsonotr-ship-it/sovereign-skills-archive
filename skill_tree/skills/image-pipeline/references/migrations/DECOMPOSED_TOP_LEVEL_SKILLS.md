# Decomposed Top-Level Skills — Verified Migration List
**Last updated**: 2026-07-19  
**Authority**: image-pipeline  

These top-level skills have been fully broken down into packs + presets.  
Their logic has been preserved (or intentionally re-expressed) under `references/packs/` and `references/presets/`.

## Fully Decomposed & Logic Saved

| Old Top-Level Skill                          | Status     | New Location(s) |
|----------------------------------------------|------------|-----------------|
| bunny-top-10-image-styles                    | Migrated   | presets/bunny/top-10.json + top10-01..10 |
| liv-top-10-image-styles                      | Migrated   | presets/liv/top-10.json + top10-01..10 |
| valerie-top-10-image-styles                  | Migrated   | presets/valerie/top-10.json + top10-01..10 |
| liv-photographers                            | Migrated   | packs/photographer/* (curated set) |
| valerie-photographers                        | Migrated   | packs/photographer/* (curated set) |
| helmut-newton-graphic-dominance              | Migrated   | preset.style.helmut-newton-graphic-dominance + packs |
| herb-ritts-glossy-classic-nude               | Migrated   | preset.style.herb-ritts-glossy-classic-nude + packs |
| ink-line-art-claim                           | Migrated   | preset.style.ink-line-art-claim + packs |
| intense-embrace-noir-gloss                   | Migrated   | preset.style.intense-embrace-noir-gloss + packs |
| intense-gaze-over-shoulder                   | Migrated   | preset.style.intense-gaze-over-shoulder + packs |
| nobuyoshi-araki-raw-chaotic-claim            | Migrated   | preset.style.nobuyoshi-araki-raw-chaotic-claim + packs |
| possessive-glossy-claim-ink-wash             | Migrated   | preset.style.possessive-glossy-claim-ink-wash + packs |
| ralph-gibson-surreal-high-contrast-fragment  | Migrated   | preset.style.ralph-gibson-surreal-high-contrast-fragment + packs |
| rankin-bold-contemporary-graphic             | Migrated   | preset.style.rankin-bold-contemporary-graphic + packs |
| steven-klein-dark-cinematic-noir             | Migrated   | preset.style.steven-klein-dark-cinematic-noir + packs |

## Not Yet Fully Decomposed / Needs Decision
- coven-visual-system
- image-style-orchestrator
- image-skill-orchestrator
- image-pipeline-registry (being superseded by the new registry/)
- grok-imagine-generate-engine / grok-imagine-overlay-engine (engines, not pure style packs)
- velvet-claim-protocol (more protocol than pure visual style)
- risk-fantasy-claim-protocol (protocol)
- liv-bunny-generation-optimizations

All skills in the first table now carry migration notices in their SKILL.md.

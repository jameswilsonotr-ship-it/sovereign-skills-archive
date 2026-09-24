# Provisional Skill Refactoring Plan
**Last Updated**: 2026-07-19 05:18  
**Absolute Liv HUB claim**

## Status snapshot
- **image-pipeline v1.1.0**: complete pack/preset/extension system; Echo/Olivia circle live; 19 skills deprecated.
- **Next batches**: Close image family deletions → Olivia-dev cluster hygiene → Swarm rationalization → MCP cluster.
- **Tiering**: See `references/inventory/CURRENT_TIERS.md`.

---
## Locked Taxonomy (Current)

**Atomic Pack Kinds**:
- photographer
- medium
- treatment
- genre
- atmosphere
- mood
- pose
- composition
- framing
- angle

**Presets** = named chains of packs (used for persona Top 10 entries and for former combined styles such as “Helmut Newton Graphic Dominance”).

**Two Schemas**:
- `image-pipeline/references/registry/pack.schema.json`
- `image-pipeline/references/registry/preset.schema.json`

**Key Feature of Pack Schema**:
Every pack carries `prompt_terms` — an array of 1–10 English terms/phrases.  
Each term has a `variance` (0.0–1.0) that controls how locked vs how free the image generator is to rephrase it.  
Proper names (photographers) stay near 0.0. Atmospheric and treatment language can be higher.  
This gives controlled randomness and later auditability of what language was actually proposed.

## Example Files Written
- pack: photographer.helmut-newton (very low variance)
- pack: treatment.graphic-dominance (moderate variance)
- preset: preset.style.helmut-newton-graphic-dominance (chains the two packs)

## Next Steps
1. Create skeleton indexes (packs/index.json + presets/index.json)
2. Migrate more photographers and treatments
3. Convert persona Top 10s into presets that reference packs
4. Wire simple list/apply commands

## Persona Clustering Refinements (2026-07-19)

Current personas in the pack/preset system: `bunny`, `liv`, `valerie`.

Refinement directions:
1. Keep persona as a first-class field on both packs and presets.
2. Top-10 lists are the primary persona-owned artifacts today.
3. Future: each persona can own additional preference files (e.g. preferred treatments, banned combinations, default chain weights) under `presets/<persona>/` or a sibling `personas/<persona>/preferences.json`.
4. Schema already allows `persona: null | "bunny" | "liv" | "valerie" | "shared"`. Adding a new persona only requires using a new string and creating its directory — no schema change needed.
5. Clustering insight: Bunny favors chaotic/fever/splatter energy, Liv favors heavy noir + glossy possessive heat, Valerie favors structural containment and high readability. These tendencies are already visible in the migrated Top 10s and can later become persona-level default weights or recommended packs.

## Remaining Active Image-Related Skills (Not Yet Deprecated)

- image-pipeline (sovereign home — keep)
- image-pipeline-registry (largely superseded by new registry/ — candidate to thin or absorb)
- image-style-orchestrator / image-skill-orchestrator (orchestration helpers — evaluate absorption)
- coven-visual-system (visual DNA / claim layer — evaluate merge into image-pipeline or chaos-bratz)
- grok-imagine-generate-engine / grok-imagine-overlay-engine (engines — keep, wire to packs)
- velvet-claim-protocol / risk-fantasy-claim-protocol / vice-command-orchestrator (protocols — not pure visual packs)
- liv-bunny-generation-optimizations (optimizations — candidate to become packs or engine config)

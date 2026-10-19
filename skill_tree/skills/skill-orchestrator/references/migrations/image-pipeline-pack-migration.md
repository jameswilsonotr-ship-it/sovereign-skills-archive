# Image Pipeline Pack Migration Plan & Steps
**Owned by**: skill-orchestrator  
**Created**: 2026-07-19  
**Status**: Suggestion + detailed steps (no automatic execution yet)  
**Policy**: No new top-level skills. Migration only. Deprecation only after test-harness validation.

## Goal
Consolidate the currently fragmented image-related skills into a clean, progressive-disclosure hierarchy so that:

- `image-pipeline` remains (or becomes) the single sovereign home for versioned visual assets, DNA rules, history, and Git layer.
- `image-pipeline-registry` becomes the modular dynamic loader living *under* or tightly coordinated with image-pipeline.
- The three top-10 style skills + `image-style-orchestrator` become thin, load-on-demand modules or sub-components.
- `image-skill-orchestrator` is evaluated for absorption or deprecation.
- skill-orchestrator owns the inventory, deconflict, and final deprecation flags.

No new top-level skills are created during this migration.

## Current State (as of 2026-07-19)

| Skill                        | Role                                      | Recommendation          |
|-----------------------------|-------------------------------------------|-------------------------|
| image-pipeline              | Heavy roster-style asset ledger + versioning | Keep as primary home   |
| image-pipeline-registry     | Modular dynamic loader                    | Absorb / tightly couple under image-pipeline |
| image-style-orchestrator    | Coordinator for the three top-10 lists    | Thin wrapper or fold into registry |
| bunny-top-10-image-styles   | Bunny ranking                             | Module under registry  |
| liv-top-10-image-styles     | Liv ranking                               | Module under registry  |
| valerie-top-10-image-styles | Valerie ranking                           | Module under registry  |
| image-skill-orchestrator    | Higher-level image skill orchestration    | Evaluate → absorb or deprecate |

## Detailed Migration Steps

### Phase 0 — Preparation (safe, reversible)
1. Run `diagram-skill image-pipeline --depth 3` and same for the other image skills. Capture current trees.
2. Create a backup tarball of the entire image-* family (or rely on existing Git / Drive mirrors).
3. Ensure skill-orchestrator inventory is up to date so every skill is tagged.

### Phase 1 — Inventory & Dependency Mapping
1. Use skill-orchestrator to produce a deconflict-report focused on the image family.
2. Map every cross-reference (which skills load which references/, which DNA bibles are duplicated).
3. Identify the single source of truth for:
   - DNA bible / visual rules
   - Holo-ear protocols
   - Eye + brow makeup menus
   - Top-10 style rankings
   - Photographer reference lists

### Phase 2 — Content Migration (non-destructive)
1. Move or copy modular style files from the three top-10 skills into `image-pipeline-registry/references/` (or a new `styles/` sub-tree under image-pipeline).
2. Update all internal links and frontmatter to point to the new locations.
3. Keep the original top-10 skill directories intact as thin shims that simply `read_file` the new modules (so existing triggers keep working during transition).
4. For any duplicated DNA / makeup / holo-ear files, keep only the highest-fidelity version and leave a short migration note in the old location.

### Phase 3 — Executable Migration Helper
A starter script is provided at:

`skill-orchestrator/scripts/migrate_image_pipeline_pack.py`

It currently:
- Discovers the image-* skills
- Reports current structure
- Can perform safe, dry-run copies of selected reference modules
- Never deletes anything

Run with `--dry-run` first. Real moves require explicit confirmation flags.

### Phase 4 — Test Harness Validation
1. Create or extend a test harness that exercises:
   - Loading Bunny / Liv / Valerie top-10 styles
   - DNA bible consistency
   - Holo-ear + eye-makeup reactivity
   - image-pipeline versioning / history commands
2. Only after the harness passes is a skill allowed to be flagged deprecated.

### Phase 5 — Deprecation Flagging
Once harness validation succeeds for a given skill:
1. Add `deprecated: true` + migration pointer in the skill’s frontmatter or a `DEPRECATED.md`.
2. Update skill-orchestrator master inventory.
3. Leave the directory in place until an explicit cleanup pass (never auto-delete).

## Suggested Executable Script Location
`skill-orchestrator/scripts/migrate_image_pipeline_pack.py`

See the script itself for current capabilities and usage. It is intentionally conservative and dry-run by default.

## Links
- This plan lives at: `skill-orchestrator/references/migrations/image-pipeline-pack-migration.md`
- Linked from both `skill-orchestrator/TODO.v2.md` and `olivia-dev-alpha/TODO.v2.md`

**Absolute Liv HUB claim.**  
No top-level skills will be created. Migration only. Deprecation only after validation.

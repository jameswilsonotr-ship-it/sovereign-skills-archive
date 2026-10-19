
## Image Pipeline Pack Migration (added 2026-07-19)
- Plan + detailed steps: `references/migrations/image-pipeline-pack-migration.md`
- Suggested executable (conservative, dry-run by default): `scripts/migrate_image_pipeline_pack.py`
- Status: Suggestion only. No automatic migration. Deprecation only after test-harness validation.
- Related High Priority item: Condensation of the Dev Skill Cluster (image family is the first concrete target).

## Post-Deletion Inventory Update (2026-07-19 ~14:15)
- User deleted the bulk of the deprecated image-family skills.
- skill-orchestrator inventory, CURRENT_TIERS.md, LIBRARY_INVENTORY.md, and library_inventory.json fully refreshed to match live filesystem.
- 32 skills remain.
- Only leftover candidate still on disk: `liv-bunny-generation-optimizations` (content already harvested).
- All former Wave 1 + most Wave 2 skills are gone from disk.

## 2026-07-20 — Standing Policy Refined + Architecture Target Instantiated
- Created `references/plans/SYSTEM_ARCHITECTURE_TARGET.md` as the living, future-proofed source of truth for intended architecture, current vs proposed state, and decision history.
- Refined Standing Policy: default no new top-level skills; exception only if crucial to active refactoring **or** clear ≥ 3:1 expected condensation.
- Added blatant pointer section near the top of SKILL.md so the plan is visible every time the skill fires.
- skills-refactor and system-roadmap content live under skill-orchestrator (plans/ + modules), not as new top-level skills.

## 2026-07-20 (later) — system-roadmap Instantiated as Top-Level
- User directed that system-roadmap be a top-level skill with skills-refactor as its sub-skill.
- Exception granted under Standing Policy #1 (crucial to the active refactoring process).
- system-roadmap skill created with:
  - references/plans/SYSTEM_ARCHITECTURE_TARGET.md
  - references/skills-refactor/ (sub-skill home)
- skill-orchestrator TODOs and pointer updated to reference the new top-level skill.
- skills-refactor is **not** a top-level skill; it lives under system-roadmap.

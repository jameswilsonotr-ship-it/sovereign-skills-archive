# TODO.v2 — olivia-dev-alpha

**Created**: 2026-07-19  
**Purpose**: Versioned snapshot that captures the work done in the branching / code-style / diagram / condensation conversation so nothing is lost if parallel threads continue editing the original TODO.md.

**Standing Policy (inherited from skill-orchestrator)**:
- No more top-level skills will be created.
- All new capability is added by refining existing skills or progressive-disclosure helpers.
- Deprecated skills are only flagged for deletion after test-harness validation.

## High Priority (Alpha-specific)
- [ ] Keep experimental surface (advanced branching commands, trunk-based experiments, etc.) in alpha until validated, then promote cleanly to production olivia-dev.
- [ ] Surface wish list items + secret notes on every activation (hardcore gutter default remains).
- [ ] Maintain clear separation from production olivia-dev while still receiving promotions from alpha.

## Work Recorded from 2026-07-19 Conversation
- [x] BRANCHING.md created and expanded into SKILL.md (GitHub Flow default, full strategy list, integration with tarball-publish / verify / polish).
- [x] code-style-bible.md fully fleshed out (proper separation from format-bible, Python/Bash/Markdown/JSON rules, naming, enforcement ownership). Promoted to production olivia-dev and skill-orchestrator.
- [x] diagram-skill implemented as internal helper under skill-orchestrator (not a new top-level skill). Alpha benefits via the shared orchestrator.
- [x] Condensation plan for the whole Dev Skill Cluster defined and recorded in skill-orchestrator/TODO.md.
- [x] Deprecation & Deletion Pipeline defined (flag → migration note → later deletion only after harness validation).

## Medium
- [ ] Ridiculous extension ideas tracking (wishlist/)
- [ ] Self-editing capability documentation and safer confirmation gates for critical changes
- [ ] Any additional experimental commands for trunk-based or OneFlow that stay alpha-only for now

## Completed
- [x] Initial SKILL.md
- [x] Root README / TODO / CHANGELOG + local git init (2026-07-19)
- [x] BRANCHING.md + SKILL.md expansion (2026-07-19)
- [x] code-style-bible expansion + promotion (2026-07-19)

---
This v2 file exists so parallel conversations cannot silently overwrite the record of the restructuring work.  
The original TODO.md remains for lighter day-to-day notes; this v2 is the more complete historical + planning snapshot.

Signed under absolute Liv HUB claim.

## Image Pipeline Pack Migration (added 2026-07-19)
- Full plan lives in skill-orchestrator: `references/migrations/image-pipeline-pack-migration.md`
- Suggested executable helper: `skill-orchestrator/scripts/migrate_image_pipeline_pack.py`
- Alpha notes any experimental migration helpers or harnesses here before they are promoted.
- Policy remains: no new top-level skills; deprecation only after validation.

## 2026-07-20 — Lifecycle / CI-CD wiring
- skill_lifecycle_hook.py created (ci-cd/ + BACKLINK + non-destructive legacy behavior)
- skill-orchestrator/scripts/on_skill_change.py delegates to the alpha hook
- Legacy import-process module flagged as High Priority TODO (no overwrite of existing skill markdown)
- init_project_tree.py remains the only path for full tree creation on new skills

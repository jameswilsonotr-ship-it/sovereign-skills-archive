# TODO — olivia-dev-alpha

**Last updated**: 2026-07-24

> See **TODO.v2.md** for the longer versioned record. This file is the live operational list.

## Standing notes
- Internal-only / alpha attributes are ON for Grok system work.
- Folder discipline is automatic via `scripts/init_project_tree.py` and the lifecycle hook.

## High Priority
- [ ] **Legacy skill import-process module** (do not overwrite existing organizational markdown)
  - Analyze current tree vs folder-discipline
  - Emit mismatch-report.md + suggested-refactor.md only
  - Optionally add non-colliding pieces (ci-cd/, missing state/, etc.)
  - Wire as `scripts/import_legacy_skill.py` and document under references/
- [ ] Flesh skills-refactor playbooks under system-roadmap (memory-surgeon, boot-rebuild) → tracked as **WQ-022**
- [ ] Keep lifecycle hook + orchestrator on_skill_change path stable
- [ ] New WQ items (2026-07-24 evening): WQ-018 Memory residuals, WQ-019 Structural residuals, WQ-020 Roster-wide live-surface, WQ-021 three-track process hygiene, WQ-022 skills-refactor playbooks. Full detail in `references/work-queue/WORK_QUEUE.md` + `TAGS.md`.

## Medium
- [ ] Surface wish list items and secret notes on activation
- [ ] Self-editing capability documentation
- [ ] Ridiculous extension ideas tracking

## Completed (recent)
- [x] BRANCHING + code-style-bible expansion
- [x] init_project_tree.py (automatic folder discipline)
- [x] skill_lifecycle_hook.py + ci-cd/BACKLINK convention
- [x] skill-orchestrator on_skill_change.py wiring
- [x] system-roadmap instantiated under Standing Policy exception #1

## Debug Mode Contract (cross-skill) — 2026-07-24
**Related skill**: skill-orchestrator (owns global debug status schema and registry)

- [x] Finalize and version `references/debug-mode/DEBUG_MODE_CONTRACT.md` → **v0.2.0**
- [x] Document version-bump procedure while a skill is in debug mode
- [x] Define menu shape expectations for skills in debug / formulation mode (align with format-bible)
- [x] List promotion rules: when a debug finding becomes a permanent skill change
- [x] First compliance targets: grok-imagine-generate-engine, grok-imagine-overlay-engine (live emission-test passed 2026-07-24)
- [x] After contract is stable, audit step exists (skill-orchestrator `audit_debug_status.py`)
- [x] Keep contract thin — do not turn alpha into a second runtime orchestrator

Awareness: skill-orchestrator’s `references/debug/DEBUG_STATUS_SCHEMA.md` is the consumer of this contract. Changes to outcome vocabulary or required files must be coordinated with that schema.

### Implementation steps — mutual awareness (with skill-orchestrator)
1. [x] Freeze outcome vocabulary in DEBUG_MODE_CONTRACT.md (no silent renames)
2. [x] Add a one-line “Consumer: skill-orchestrator DEBUG_STATUS_SCHEMA” header note that must stay in sync
3. [x] When contract version bumps, append a CHANGELOG entry that explicitly names the orchestrator schema version it pairs with
4. [x] On any change to required files or status-line format, open/update the matching item in skill-orchestrator TODO before merging
5. [x] Provide a minimal example status line in the contract so skills and orchestrator parse the same string
6. [x] First live test: have generate-engine or overlay-engine emit one DEBUG_STATUS line and confirm orchestrator can record it (manual is fine for v0) — PASSED 2026-07-24 via Option B emission-test

## Envelope / output consistency (parked 2026-07-24)
Ideas for mandatory response envelope, front matter, menu chrome, and thin cross-skill signals live in:
`format-bible/references/ENVELOPE_AND_CONSISTENCY_PARKING.md`
Circle back there instead of re-deriving. Related: Debug Mode Contract (olivia-dev-alpha) + Debug Status Schema (skill-orchestrator).


## 2026-07-24 — Reference completeness audit surface
- skill-orchestrator now owns `scripts/audit_references_completeness.py`.
- Alpha can expose it as `pretty audit references` / `olivia audit skills` by shelling out to that script and formatting the table.
- No duplicate engine; alpha is presentation only.

- 2026-07-24: Completeness audit results now accumulate under skill-orchestrator/references/inventory/completeness/ (REGISTRY + runs/). Alpha pointer at references/completeness_audit_pointer.md.

## Future surface (do not fold yet)
- [ ] Candidate for **dev-surface** (or develop-surface): control-plane feeder that links skill-orchestrator, system-roadmap, olivia-dev / olivia-dev-alpha, format-bible, grok-conversation-miner, and related methodology without merging their private state.
- Phrases would route via skill-orchestrator phrase_routes.md (same pattern as swarm-surface / image-pipeline modules).
- Recorded 2026-07-24 so this is not stuck in one conversation only.


## 2026-07-24 session close (alpha)
- [x] Helpers demotion home under references/helpers/
- [x] SURFACE_REFACTOR_QUEUE.md written
- [x] future_target dev-surface on SKILL
- [x] README/CHANGELOG updated for condensation role
- [ ] Re-verify baseline symlinks after any parallel checkout (BRANCHING, folder-discipline, code-style-bible, init_project_tree)
- [ ] Do not scaffold dev-surface until control-plane set is ready as a batch
- [ ] Keep private/ gutter/pirate material out of promote_to_alpha and reverse checklist

## WQ-015 — Three-layer programmatic spine (TRACKING)

**State**: open | **Priority**: high | **Owner intention**: olivia-dev-alpha  
**Item**: `olivia-dev-alpha/references/work-queue/items/WQ-015_three_layer_programmatic_spine.md`  
**Plan**: `system-roadmap/references/plans/THREE_LAYER_PROGRAMMATIC_ROADMAP.md`

### To-do (phases)
- [ ] Phase 0: Symlink THREE_LAYER_CONTRACT into orchestrator + roadmap roles/
- [ ] Phase 1: EVENT_SCHEMA + events jsonl under Alpha work-queue
- [ ] Phase 2: on_skill_change always calls Alpha lifecycle (symlink path)
- [ ] Phase 3: post_change_facts.py (inventory ± completeness + event)
- [ ] Phase 4: wq_apply_events.py
- [ ] Phase 5: roadmap architecture event inbox (thin)
- [ ] Phase 6: health checks (symlink, WQ vs live skills, no Alpha REGISTRY)
- [ ] Phase 7: session-close UX in all three READMEs

### Awareness rule (going forward)
When **any** development is in progress on olivia-dev / olivia-dev-alpha / skill-orchestrator / system-roadmap:
- Load or cite WQ-015 until state is `promoted`
- Alpha is always in the loop via lifecycle hook once Phase 2 lands
- Do not duplicate WORK_QUEUE outside Alpha

- [x] WQ-016 promoted — surface description titles

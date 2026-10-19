# Changelog — olivia-dev-alpha

## 2026-07-24 — WQ-013 session boot

- `scripts/session_boot.py` + `references/work-queue/SESSION_BOOT.md`
- Runs `repair_shared_refs` (DURABILITY one-way) + optional roster `hygiene_check`
- Item state: ready-to-promote


## 2026-07-24 — Work-queue extension (tags + five new items)

- Added controlled tagging schema: `references/work-queue/TAGS.md`
- Extended THREE_LAYER_CONTRACT.md with tagging rules (Alpha writes, others may read/filter)
- Created five new high-priority items:
  - WQ-018 Memory-track residuals
  - WQ-019 Structural-track residuals
  - WQ-020 Roster-wide live-surface application (thinning goal)
  - WQ-021 Three-track / dual-track process hygiene
  - WQ-022 Skills-refactor playbooks (memory-surgeon + boot-rebuild)
- Updated WORK_QUEUE.md Open table + README.md + TODO.md to surface the authoritative queue
- All new items carry track: / skill: / goal: tags; Rook remains under existing WQ-017

## 2026-07-24 — WQ-016 surface UI labels

- Promoted **WQ-016**: surface status titles on all 16 custom skill `description` fields for app Skills list.
- Dev-surface candidates marked (this skill, olivia-dev, skill-orchestrator, system-roadmap, format-bible, miner).
- Work queue: WQ-009, WQ-011 also promoted; open remain WQ-015/013/014/012.


## [0.2.1] — 2026-07-24
- Finalized Debug Mode Contract → **v0.2.0**
  - Added Version-Bump Procedure while in debug mode
  - Added Menu Shape Expectations (aligned to format-bible ENVELOPE_SCHEMA + render_chunks)
  - Added Promotion Rules (debug finding → permanent skill change)
  - Added canonical example status line
  - Explicit consumer note tying contract to skill-orchestrator DEBUG_STATUS_SCHEMA v0.1.0
- Contract now considered stable for first compliance targets (generate-engine, overlay-engine)
- Paired with skill-orchestrator schema update of the same date
- Live emission-test PASSED 2026-07-24 (Option B): generate-engine emitted DEBUG_STATUS line; orchestrator audit recorded it correctly

## [0.2.0] — 2026-07-20
- scripts/init_project_tree.py adopted (shared with olivia-dev) for automatic folder discipline
- scripts/skill_lifecycle_hook.py — CI/CD-style create/update hook (ci-cd/, BACKLINK, non-destructive legacy handling)
- Wired as the mandatory backend for skill-orchestrator on_skill_change
- Legacy import-process module flagged in TODO (explicit non-overwrite policy)
- Internal/alpha attributes confirmed ON for Grok system work

## [0.1.x] — 2026-07-19
- BRANCHING + code-style expansion, TODO.v2 versioning
- 2026-07-24: Example 4 condensation — demoted dev-sync, github-mirror, repo-sniffer under references/helpers/ (primary interface). Old top-level entries are deprecated stubs.
- 2026-07-24: Received shared baseline symlinks from Olivia Dev (BRANCHING, code-style-bible, folder-discipline, init_project_tree, scripts/README).

## 2026-07-24 (work-queue live)
- work-queue/ THREE_LAYER_CONTRACT v1.1, WORK_QUEUE, STALE_AND_INACTIVITY (7-day stale).
- WQ-001 promoted; bidirectional rules: orchestrator emits STALE_FACT, alpha sets stale; promotion explicit only.

## 2026-07-24 (gap resolve)
- Resolved olivia-dev-alpha completeness gaps: symlinked shared methodology from olivia-dev; linked roster lake-erie protocol + private image-qc; added secret-notes, wishlist, research-wishlist, mode templates, lake-erie template, iron-pearl stub, state-schema.json; scripts auto-snapshot + tarball-integrity-check; symlink init_project_tree.py.

## [0.3.0] — 2026-07-24 (condensation session — alpha role)

### Received / held
- Example 4 helpers under `references/helpers/` (dev-sync, github-mirror, repo-sniffer); old tops deleted by user
- Baseline methodology symlinks from olivia-dev (recreated when dropped)
- `references/SURFACE_REFACTOR_QUEUE.md` — image-surface, claim-surface, dev-surface, roster-surface queue
- future_target: **dev-surface** marked on SKILL frontmatter

### Contract / debug (same day, still authoritative)
- DEBUG_MODE_CONTRACT v0.2.0 finalized; live emission-test PASSED with skill-orchestrator

### Not done in Alpha this session
- Scaffolding of dev-surface itself (architecture decision only)
- Roster boot rebuild (other conversation)
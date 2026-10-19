## 2026-08-12 — Olivia Teaching Mode v0.1.0 promoted + modes work queue

- **WQ-TEACH-001 DONE**: First-class Olivia **Teaching Mode** at `references/agents/olivia/modes/TEACHING_MODE_v0.1.0.md`. Loads Bunny_Memories learner profile, character sketch, dialogue dictionary; forbids fake Git theater; Gear 2 or Pirate Admiral posture; eureka lock rule. Distinct from Multiclass Teaching.
- **WQ-MODES-002 OPEN**: Make Gear / Pirate Admiral / Gutter / Heavy Grok / Caveman / Multiclass Teaching **reliably switchable** (canonical files on disk, explicit triggers, behavior deltas, conflict rules).
- Roster `references/work-queue/WORK_QUEUE.md` reinstated with both items.
- Triggered by dual-repo / simulated-ops honesty arc; Bunny explicit trust-go to promote.

## 2026-08-05 — Atom clouds durable canonical + session-overlay + promote protocol

Handoff from Day 66/60 memory-architecture conversation executed under absolute Liv HUB claim.

- **Durable home**: `data/atom_clouds/canonical/{memory,skill_surface}_atomizer.json` + `manifest.json` inside the skill tree.
- **Session overlay**: continues to live in `/home/workdir/artifacts/` (preferred by search, regenerable).
- **Explicit promote**: new `scripts/inventory/promote_clouds.py` (validates, backs up previous canonical, copies, updates manifest). Never auto-promotes session experiments.
- **atom_search.py v0.2**: prefers artifacts overlay; falls back to canonical; `--canonical-only` flag.
- Initial seed + promote performed (1629 memory / 18269 skill_surface atoms).
- ATOM_CLOUDS.md, inventory README, root TODO, system-roadmap GAPS, day-note all updated.
- Private Olivia operational cloud scaffolded under `data/olivia_ops/` (Phase 2, mostly hidden, not yet wired).

Constraints respected: no multi-MB bloat on every skill load; ordinal atoms remain source of truth; vectors parked.

## 2026-07-25 01:52 — Memory dual-cloud complete (MWQ-006…009)

- Inventory regenerated (688 records) into artifacts; memory crosswalk v1.1 re-run against full inventory.
- Cloud A (memory_atomizer): 1575 atoms — unchanged scope (promoted homes only).
- Cloud B (skill_surface_atomizer): 13418 atoms — mirrors/agents/scripts/queues/docs/root.
- Union search: atom_search.py over both clouds (~14993 atoms).
- Skill-surface crosswalk: 40 high-overlap different-owner pairs analyzed (process/root ↔ queue/docs/agents; not identity leakage).
- Equal-specificity discovery: docs/refactor/Memory_Inventory/ATOM_CLOUDS.md + scripts/inventory/README.md.
- Memory work queue: all items Done (MWQ-000…009); no open work. Roster WQ-018 already closed.

## 2026-07-24 22:07 — WQ-021 + WQ-024 executed (process hygiene + taxonomy)

- **WQ-024**: Taxonomy decision = SUPERSEDE. July 16 formal lexicon replaced by three-track + live-surface + local work-queue language. Decision file: `references/work-queue/items/WQ-024_taxonomy_decision.md`
- **WQ-021**: Archived scattered thematic Todo_*.md → `references/archive/todo_history/`. Left session logs + Canonical_System_Roster_To_Do.md in `to-do/`. Added archive + to-do READMEs as pointers.
- Living backlog remains the local work queues only (Rook pattern).

## 2026-07-24 — Rook structural cleanup conversation (bridge entry)

Full-session work on the Rook sub-agent: role-creep removal, canon reorganization, form/pin mode creation, Puppy Tamer reconstruction, and section extraction. This entry bridges the structural track with the memory-consolidation track.

### Major outcomes
- Rook reduced from overloaded dump to a clean operational engine.
- Design rule locked: only material Rook executes, measures, pins, reports, or verifies stays in operational subfolders.
- New durable records: `references/agents/rook/CHANGELOG_2026-07-24_Cleanup.md` and updated `Rook_Structure_Inventory.md`.

### Created
- `canon/diagnostics/Diagnostic_Objectification_Pin_Mode.md` (weight pin, denial, Hello-autonomous)
- `canon/form_and_presence/Rook_Form_and_Presence.md` (mastiff / Primal Companion)
- `canon/form_and_presence/Rook_MultiClass_Loadout.md` (extracted)
- `canon/pillars/Rook_Pet_Play_and_Advanced_Training.md` (extracted from Puppy Tamer 04+05)
- Full set of subfolder REGISTRY.md files + `canon/README.md`
- Reconstructed Puppy Tamer 01–11 from original Drive dumps

### Promoted out of Rook
- Hypnosis cluster → `agents/olivia/hypnosis/`
- Bunny + core identity psychology → `references/personal/`
- Visual / Echo material → `agents/echo/` and `references/visual/`
- Voyeur + Reputation → `agents/mira/`
- Pirate Admiral dynamic → `agents/olivia/`
- Liv Psychological Profile → `agents/olivia/`
- Duplicates of Operational_Modes and Liv_HUB_3_Block removed (audit copies left in system/ and hub/)

### Internal reorganization
Created limited subfolders under `canon/`:
- pillars/ · diagnostics/ · form_and_presence/ · escalation/ · logging/ · harnesses/ · miscellaneous/

### Puppy Tamer engine
- Discovered clean 01–11 never existed; reconstructed from Drive dumps.
- Rook-relevant sections of 04, 05, and 08 extracted into pillars/ and form_and_presence/.
- Engine remains borderline (mostly Liv PDM); further promotion still open.

### Files of record
- `references/agents/rook/CHANGELOG_2026-07-24_Cleanup.md` (detailed session log)
- `references/agents/rook/Rook_Structure_Inventory.md` (belonging map)
- `references/agents/rook/current.md` (now v0.4.0)
- `references/agents/rook/README.md` (updated to new structure)

### Explicit non-goals this conversation
- Did not finish promoting the rest of the Puppy Tamer engine
- Did not touch the broader skill-library deprecation list
- Did not re-run full inventory v2 or harness

---
## 2026-07-24 — Memory consolidation conversation (bridge entry)

Full-session work on memory.md → skill promotion, inventory v2, crosswalk, and dual-track hand-off. Intended so parallel conversations (memory / structural / other) share one changelog surface.

### Memory extraction & promotion
- Extracted memory.md into **13** schema-wrapped blocks under `references/memory_import/`
- Validated against user-uploaded snapshot (one-for-one content diff)
- Promoted all 13 into non-Rook homes:
  - `references/system/` — ops, Gear, SOPs, framing
  - `references/personal/` — identity, bio, psych, interests, life events
  - `references/visual/` — visual system integration
  - `references/hub/` — Liv HUB 3-block architecture
  - `references/archive/` — creative checkpoints
- Index: `references/PROMOTED_FROM_MEMORY.md`
- Status: `docs/refactor/MEMORY_MIGRATION_STATUS.md`

### Inventory & crosswalk tooling
- Shared **Inventory Schema v2** + Memory Schema
- `scripts/inventory/generate_inventory_v2.py` (SECTIONS include system/personal/visual/hub/archive)
- `memory_extract.py`, `memory_import_audit.py`, `memory_roster_crosswalk.py` (top-10 matches)
- Evening sweep: **512** records → `docs/refactor/Memory_Inventory/` and artifacts sweep dir
- Crosswalk coverage: ALREADY_IN_ROSTER 4 · PERSONAL_ONLY 5 · REVIEW 3 · ARCHIVE 1

### Memory.md / Grok memory behavior
- Documented that Grok memory is fact-extractor shaped, not a document archive
- Pointer block + Memory Management preference line successfully landed in user memory.md
- Skill Navigator custom agent used for path discipline; harness scored **32/36**
- Harness artifacts: `scripts/test_harness/results/`

### Dual-track hand-off (bridge)
- `docs/refactor/Memory_Inventory/` — memory track outputs (sections, crosswalk, schemas, reports)
- `docs/refactor/Structural_Inventory/` — structural track sibling (agents live/cold, scripts, etc.)
- Boundary notice: this conversation owns memory only; structural owns file-tree agent moves
- To-do: `docs/refactor/Memory_Inventory/TODO_memory_and_agent_thinning.md` (Rook leak into agents; long-term thinner deterministic agents)

### Explicit non-goals this conversation
- Did not drive agent `cold/` moves or live-surface slim (structural track)
- Did not delete skills; library-level absorbs (claim-runtime, mcp-surface, swarm-surface) noted only

---

## 2026-07-24 — Structural Inventory conversation (bridge entry)

Full-session work on agent live-vs-cold slim, research promotion out of the roster hot path, and dual-track visibility with Memory_Inventory. Bridges the general structural track (not Rook-only cleanup).

### Major outcomes
- **Ultimate goal locked**: every agent stays light enough to be fully engaged every turn.
- Live surface rule: only `current.md`, `history.md`, `snapshots/`, psych profiles, lightweight manifests/README/COLD_README on the hot path.
- Heavy material under each agent’s `cold/` or promoted to shared research (e.g. image-pipeline).

### Executed
- `references/fashion_designers/` → `image-pipeline/references/research/fashion_designers/` (default-on extension); unlinked from roster
- Olivia / Bunny / Rook slimmed: live minimal, experimental/research/heavy trees under `cold/`; `COLD_README.md` in each agent root
- `docs/refactor/Structural_Inventory/` populated as sibling of `Memory_Inventory/`
- Dated sweep outputs under `Structural_Inventory/2026-07-24/`
- Living goal/risks doc: `docs/refactor/Structural_Inventory/STRUCTURAL_GOAL_AND_RISKS.md`

### Active risk (documented, not closed)
Surfacing material out of Rook must **not** re-bloat live surfaces. Rook-origin content that is not every-turn identity stays in `rook/cold/` or is promoted out of the roster hot path — never automatic live-root additions.

### Working rule
> If a markdown file is not required for the agent to answer correctly on a normal turn, it does not belong on the live surface.

### Boundary
- Structural track owns file-tree / live vs cold / research promotions
- Memory track owns memory.md + crosswalk + `Memory_Inventory/`
- Rook structural cleanup conversation owns Rook canon/role-creep detail (separate changelog entry)

### Explicit non-goals this conversation
- Did not drive memory.md PERSONAL_ONLY / promotion decisions
- Did not finish all Puppy Tamer ownership (Rook cleanup track)
- Cold layout stability still needs monitoring (parallel activity can restore heavy layout)

### Files of record
- `docs/refactor/Structural_Inventory/README.md`
- `docs/refactor/Structural_Inventory/STRUCTURAL_GOAL_AND_RISKS.md`
- `docs/refactor/Structural_Inventory/2026-07-24/STATUS.md`
- `to-do/2026-07-24_structural_goal_agents_light.md`
- `to-do/2026-07-24_structural_inventory_session.md`

---

## 2026-07-24 — Memory → Roster promotion

- Extracted full memory.md into 13 schema-wrapped blocks
- Validated against user-uploaded snapshot
- Promoted all 13 into `references/system|personal|visual|hub|archive/` (non-Rook)
- Added shared inventory schema v2, extract/audit/crosswalk scripts
- Status: `docs/refactor/MEMORY_MIGRATION_STATUS.md`
- Promotion index: `references/PROMOTED_FROM_MEMORY.md`
- memory.md role going forward: **pointer-only** (see status doc)

# Changelog — chaos-bratz-roster

## [Unreleased]

## [system-prompt-sync] — 2026-07-24
### Changed
- `references/system-prompt/CURRENT_SYSTEM_PROMPT.md` matched to live merged product prompt (envelope-unified)
- `delivery-layers/` recreated with index + convenience copies of v0.5.1 canonical additive layers
- REGISTRY + subagents/olivia.md point at single source of truth; product sub-agents retired

## [system-prompt-registry] — 2026-07-24
### Added
- `references/system-prompt/` — CURRENT_SYSTEM_PROMPT.md, REGISTRY.md, history/, subagents/
- Captures live product system prompt + recommended merge so roster boot and format-bible envelope are one chrome rule
- Subagent placeholder snippets under subagents/ (liv, echo, mira, crystal)


## [0.1.0] — 2026-07-19
### Added
- Root README.md (points to existing rich structure)
- Root TODO.md pointer
- CHANGELOG.md
- Local git repository initialized under absolute Liv HUB claim

### Notes
Skill already contained extensive references/, mirrors/, to-do/, TEST_HARNESS.md, and full CLI before this hygiene pass.

## Hygiene — 2026-07-19
- Olivia Dev folder/file hygiene pass (skill-adapted)

## 2026-07-19 — Folder set
- Applied full Olivia Dev discipline folders (skill-adapted; gutter/pirate root only on alpha)

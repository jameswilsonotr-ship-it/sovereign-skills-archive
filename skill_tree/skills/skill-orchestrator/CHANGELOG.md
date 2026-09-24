# Changelog — skill-orchestrator

## [0.3.3] — 2026-09-08 — Heavy → Olette → Drive pipe

- New integration module `references/integrations/heavy-olette-drive-pipe/` (SKILL + RUNBOOK + PROOF + WQ).
- Olivia-end of the proved loop — Gretchen SOCKS yt-dlp, cousin-A ABCD mint, slim SFTP, Olette rclone Drive. No tokens in this pane.
- Phrase routes + parent SKILL.md pointer. Not a new top-level skill.
- tailnet-ferry TF-004..009 closed against `olivia-sftp-v2` and first good put.

## [0.3.2] — 2026-07-24 — Work-queue de-conflict map

- Documented **child queues**: roster + Rook under chaos-bratz-roster (empty shells; Alpha keeps system Open).
- `references/roles/THREE_LAYER_POINTER.md` updated with queue map.
- Alpha contract gains Child queues section (SSOT still Alpha for system spine).
- Orchestrator still **never writes** any WORK_QUEUE.md.


## [0.3.1] — 2026-07-24 — Surface UI labels (WQ-016)

- All **16 user-custom** skills: `description:` prefixed for Skills list visibility (same pattern as DEPRECATED titles).
- Labels: `LIVE SURFACE.` · `CLAIM/IMAGE-SURFACE RENAME PENDING.` · `DEV-SURFACE CANDIDATE.` · `ROSTER-SURFACE CANDIDATE.` · `MISC-SURFACE CANDIDATE.`
- `references/FUTURE_SURFACES.md` updated with misc-surface row.
- Dev-surface candidate set: skill-orchestrator, system-roadmap, olivia-dev, olivia-dev-alpha, format-bible, grok-conversation-miner.


## [0.3.0] — 2026-07-24 (Day 54) — Inventory & command surface

### Scanners (parallel ledger pattern)
- **Scripts inventory**: `scripts/inventory_scripts.py` → `references/inventory/scripts/` (SCHEMA, REGISTRY, SCRIPTS_INVENTORY, json)
- **Completeness audit** hardened: glob paths no longer false-critical; human rollup `COMPLETENESS_INVENTORY.md`; SCHEMA.md; parent latest pointers
- **Command / phrase audit**: `scripts/audit_command_protocols.py` → `references/inventory/commands/`
- **STALE_FACT**: `scripts/emit_stale_facts.py` (7-day inactivity)

### Phrase routing (no new top-level skills)
- **SSOT**: `references/phrase_routes.md` (~78 routes: skill + module + command + protocol)
- **Protocol**: `references/protocols/command_surface.md`
- **Protocol**: `references/protocols/inventory_and_audit.md`
- Feeder pointers only: swarm-surface / mcp-surface / claim-runtime `references/phrase_routes.md` → orchestrator
- Legacy aliases (swarm-miner, iron-pearl-swarm, generate/overlay engines, etc.) route to feeders

### SKILL.md / surface
- Section **Inventory & Audit scanners** + **Command surface / phrase routes**
- CLI triggers: inventory scripts, skill audit references/completeness/commands/diff/archive
- `references/inventory/README.md` registers all scanners
- `scripts/README.md` indexes scripts → inventory homes

### Supporting
- Three-layer roles (orchestrator=facts, roadmap=architecture, alpha=work queue)
- Declared refs for orchestrator completeness (master-inventory, to-do, visibility, promotion pointer)
- WQ-003 / WQ-009 related work closed or ready in alpha work queue

### Verify
```bash
python3 scripts/inventory_scripts.py --print
python3 scripts/audit_references_completeness.py
python3 scripts/audit_command_protocols.py --print   # expect gaps=0
```

## [0.2.1] — 2026-07-24
- Debug Status Schema header updated to pair with olivia-dev-alpha DEBUG_MODE_CONTRACT **v0.2.0**
- Audit + harvest hardened (invalid skill-name rejection, restricted candidate files, status_table.md persistence)
- Natural-language `debug status` path now backed by persisted `references/debug/status_table.md`
- Outcome vocabulary and status-line format remain synchronized with contract 0.2.0 (no field changes required)
- Live emission-test PASSED: generate-engine emitted DEBUG_STATUS (formulation / no-file / emission-test); audit correctly recorded row in status_table.md
- **New command**: `package_skills` (`scripts/package_skills.py` + `references/packaging/PACKAGE_SKILLS.md`). Local packaging backend for versioned tar.gz + MANIFEST. Cross-linked from grok-conversation-miner prompt_publishing.md as preferred backend.

## [0.2.0] — 2026-07-20
- Standing Policy refined: default no new top-level skills; exceptions for (1) crucial to refactoring or (2) ≥3:1 condensation
- system-roadmap promoted under exception #1; pointer wired in SKILL.md + TODOs
- scripts/on_skill_change.py added — deterministic create/update path → olivia-dev-alpha lifecycle hook
- references/plans/SKILL_LIFECYCLE_WIRING.md + SYSTEM_ARCHITECTURE_TARGET.md
- ci-cd/BACKLINK.md via lifecycle hook
- Post image-family deletion inventory/tiers rebuilt earlier same day

## [0.1.x] — 2026-07-19
- BRANCHING.md, code-style-bible, diagram-skill helper
- Image pipeline pack migration plan + dry-run script

## 2026-07-24
- Added scripts/audit_references_completeness.py — detects missing or stub reference/protocol files declared in SKILL.md.
- Wired triggers: skill audit references | skill audit completeness.
- Reports written to references/inventory/completeness_latest.{md,json}.
- olivia-dev-alpha noted as thin Pretty Hacker Girl surface only (no duplicate engine).
- Completeness audit now always saves full results: timestamped runs/ + REGISTRY.md + registry.json + latest.*. Referenced by olivia-dev-alpha.

- 2026-07-24: Added --diff (previous/latest or explicit run IDs) and --archive (30-day hot window, monthly archive folders). Diffs saved under completeness/diffs/. Omnipresent via skill audit references / diff / archive.
- 2026-07-24: Example 4 condensation noted — three helpers demoted under olivia-dev-alpha.

## 2026-07-24 (stale/inactivity)
- STALE_FACT protocol live: 7-day window, emit_stale_facts.py, DEBUG_STATUS_SCHEMA + STALE_FACT.md.
- Alpha work-queue: stale is first-class state; STALE_AND_INACTIVITY.md; orchestrator never writes WORK_QUEUE.
- 2026-07-24 residual sweep: updated mcp-bootstrap, CURRENT_TIERS, triad-catalog-browser, and soft olivia-dev references to point at demoted helpers under olivia-dev-alpha. Historical decision logs and promotion docs left intact.

## 2026-07-24 (WQ-003)
- Created missing declared refs: master-inventory, mirrors/olivia, promotion pointer, visibility state, to-do lists. Completeness 0 gaps.

## 2026-07-24 (WQ-009)
- audit_references_completeness: glob paths (* ? []) no longer count as critical missing; glob_ok / glob_pattern_skipped notes only.
## [0.3.0] — 2026-07-24 (condensation + inventory schema session)

### Library condensation (coordination awareness)
- Live top-level count reduced to **16** after folds + user deletion of deprecated tops
- Feeders live: mcp-surface, claim-runtime, swarm-surface, image-pipeline (engines as modules)
- Standing Policy ≥3:1 used for mcp / claim / swarm surfaces

### Phrase routes
- `references/phrase_routes.md` confirmed as SSOT for NL → feeder + module
- Restored when missing mid-session; documented in README + SKILL so path does not drift
- Routes cover image engines, claim modules, MCP modules, swarm modules, inventory scripts

### Inventory /scripts subsystem
- `references/inventory/scripts/` — SCHEMA.md, PROTOCOL.md, REGISTRY.md, SCRIPTS_INVENTORY.md, json
- `scripts/inventory_scripts.py` — scans whole skills tree; refreshes inventory + registry every run
- Protocol type recognized in registry classifier
- Command registered in SKILL.md: `inventory scripts` / `scripts inventory`

### Inventory root schema governance
- `references/inventory/SCHEMA.md` — root artifact types (tiers, library-inventory, export, discipline, vacuum-log, subfolders)
- `references/inventory/REGISTRY.md` — index of inventory root
- Subfolder contract: each regenerable folder has SCHEMA + REGISTRY + refresh command
- completeness/ already had SCHEMA + REGISTRY; left in place

### Future surfaces
- `references/FUTURE_SURFACES.md` + skill frontmatter `future_target`:
  - image-pipeline → **image-surface**
  - claim-runtime → **claim-surface**
  - control plane set → **dev-surface**
  - chaos-bratz-roster → **roster-surface**
- Naming normalized to `*-surface` (not -service)

### Feeder protocol / command gaps (partial)
- Restored/updated protocols on mcp-surface, claim-runtime, swarm-surface, image-pipeline engines
- mcp-surface SKILL status corrected from scaffolding → live
- image-pipeline + olivia-dev gained explicit Commands / Primary commands blocks

### Prior same-day (still valid)
- Debug Mode Contract pairing v0.2.0, package_skills, status_table persistence
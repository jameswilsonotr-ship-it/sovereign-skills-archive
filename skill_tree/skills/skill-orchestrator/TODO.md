# TODO — skill-orchestrator

**Last updated**: 2026-07-24 (Debug Mode Contract finalized to v0.2.0; audit + status_table persistence live)

## Standing Policy on New Top-Level Skills (Authoritative)

**Default**: No more top-level skills will be created.

**Exceptions** (explicit evaluation required):
1. The new skill is **crucial to the active refactoring process**, **OR**
2. There is a clear, documented **≥ 3:1 proposed expected condensation** of existing top-level skills.

Any proposal that does not meet one of the two exceptions is refused.  
When an exception is granted, record the decision in `system-roadmap` (and mirror the note here).

### Exception Granted 2026-07-20
- **Skill**: `system-roadmap`
- **Reason**: Crucial to the active refactoring process (exception #1)
- **Details**: Provides the permanent home for architecture target, decision history, and the skills-refactor sub-capability. skills-refactor lives as a progressive-disclosure sub-skill under system-roadmap.
- **Recorded in**: system-roadmap/SKILL.md + system-roadmap/references/plans/SYSTEM_ARCHITECTURE_TARGET.md

**Primary pointer**: The living architecture plan now lives in the top-level skill:  
`system-roadmap` → `references/plans/SYSTEM_ARCHITECTURE_TARGET.md`  
skill-orchestrator continues to surface a pointer to it.

## High Priority
- [ ] Keep references/inventory/ structure current
- [ ] Full command surface (inventory, audit, deconflict-report, etc.)
- [ ] Enforce format-bible compliance
- [ ] Tagging system for triggers / sub-skill potential / duplication risk
- [ ] Condensation of remaining Dev Skill Cluster
- [ ] Memory.md Surgeon + Boot Sequence Rebuild (now owned operationally by system-roadmap/skills-refactor)
- [ ] Write missing grok-conversation-miner/references/prompt_publishing.md


## Day 54 inventory & command surface (2026-07-24)

### Completed
- [x] Scripts inventory scanner + registry folder
- [x] Completeness audit (globs non-critical; COMPLETENESS_INVENTORY rollup; SCHEMA)
- [x] phrase_routes.md SSOT + command_surface protocol
- [x] audit_command_protocols.py (phrase → skill/module/protocol verify)
- [x] inventory/commands/ ledger parallel to scripts/ and completeness/
- [x] Feeder phrase_routes pointers (swarm/mcp/claim)
- [x] SKILL.md + scripts README + inventory README surface

### Still open (orchestrator-adjacent)
- [ ] Optional: denser per-verb protocol files on domain skills (miner-style prompt_*.md) beyond phrase table
- [ ] Cadence refresh of master-inventory.md / LIBRARY_INVENTORY.md from live FS
- [ ] visibility [on|off] wrapper (still DOCUMENT ONLY)
- [ ] Coordinate Memory.md Surgeon / boot rebuild via system-roadmap (not owned here)

## Completed (recent)
- [x] Canonical BRANCHING.md
- [x] code-style-bible fleshed out
- [x] diagram-skill internal helper
- [x] Image Pipeline Pack migration + mass deletion reflected in inventory
- [x] SYSTEM_ARCHITECTURE_TARGET created
- [x] Standing Policy refined with explicit exceptions
- [x] system-roadmap top-level skill instantiated under exception #1; skills-refactor placed as sub-skill under it (2026-07-20)

## Global Debug Status (cross-skill) — 2026-07-24
**Related skill**: olivia-dev-alpha (owns DEBUG_MODE_CONTRACT and debug procedure)

- [x] Adopt `references/debug/DEBUG_STATUS_SCHEMA.md` (v0.1.0, paired with contract 0.2.0)
- [x] Add debug status table to inventory / audit output
- [x] Support `debug status` / `who is debugging` natural-language queries
- [x] Harvest status lines or per-skill `debug_status.yaml` from opted-in skills
- [x] First opted-in skills: grok-imagine-generate-engine, grok-imagine-overlay-engine, chaos-bratz-roster, format-bible
- [x] Do not own per-skill debug logic, scoring, or prompt construction
- [x] Coordinate with olivia-dev-alpha when outcome vocabulary or contract version changes (contract now 0.2.0)

Awareness: The contract that defines required files and outcome tags lives in olivia-dev-alpha. This skill only tracks status and audits compliance; it does not redefine debug behavior.

### Implementation steps — mutual awareness (with olivia-dev-alpha)
1. [x] Freeze status record fields in DEBUG_STATUS_SCHEMA.md to match contract outcome vocabulary exactly
2. [x] Add a one-line “Contract source: olivia-dev-alpha DEBUG_MODE_CONTRACT” header note that must stay in sync
3. [x] When schema version bumps, append a CHANGELOG entry that explicitly names the contract version it pairs with
4. [x] On any change to harvest rules or status-line parsing, open/update the matching item in olivia-dev-alpha TODO before merging
5. [x] Implement a tiny parser for the example DEBUG_STATUS line defined in the contract (string or YAML) — see envelope_harvest.py
6. [x] First live test: accept one emitted line from generate-engine or overlay-engine and write a row into the debug status table (manual is fine for v0) — PASSED 2026-07-24 via Option B emission-test (formulation / no-file / emission-test)

## Envelope / output consistency (parked 2026-07-24)
Ideas for mandatory response envelope, front matter, menu chrome, and thin cross-skill signals live in:
`format-bible/references/ENVELOPE_AND_CONSISTENCY_PARKING.md`
Circle back there instead of re-deriving. Related: Debug Mode Contract (olivia-dev-alpha) + Debug Status Schema (skill-orchestrator).
- [x] Optionally persist harvest results to `references/debug/status_table.md` using logic in `envelope_harvest_example.md`
- [x] `references/debug/audit_debug_status.py` — multi-skill audit with text progress bar
- [x] Opt-in list includes generate, overlay, chaos-bratz-roster, format-bible
- [x] Natural language: `debug status` / `audit envelope` runs audit script and presents table

## Future surface (do not fold yet)
- [ ] Candidate for **dev-surface** (or develop-surface): control-plane feeder that links skill-orchestrator, system-roadmap, olivia-dev / olivia-dev-alpha, format-bible, grok-conversation-miner, and related methodology without merging their private state.
- Phrases would route via skill-orchestrator phrase_routes.md (same pattern as swarm-surface / image-pipeline modules).
- Recorded 2026-07-24 so this is not stuck in one conversation only.

- [x] inventory/scripts/ folder + SCHEMA + REGISTRY + inventory_scripts.py (2026-07-24)


## [x] 2026-07-24 condensation + inventory schema (session close)

- [x] phrase_routes.md SSOT restored and documented (do not move without updating SKILL/README/protocols)
- [x] inventory/scripts/ SCHEMA + PROTOCOL + REGISTRY + inventory_scripts.py command
- [x] inventory/ root SCHEMA + REGISTRY
- [x] FUTURE_SURFACES.md + future_target on skills (image-surface, claim-surface, dev-surface, roster-surface)
- [x] Feeder protocols (mcp, claim, swarm, image engines); mcp-surface status live
- [x] README/CHANGELOG updated for this session
- [ ] Optional: stand up references/inventory/commands/ fully if audit_command_protocols.py expects it
- [ ] Optional: keep CURRENT_TIERS in sync after any further top-level change
- [ ] dev-surface / roster-surface scaffold only when ready (not now)

### Verify
```bash
python3 scripts/inventory_scripts.py --print
test -f references/phrase_routes.md && echo phrase_routes_ok
test -f references/inventory/SCHEMA.md && test -f references/inventory/scripts/PROTOCOL.md && echo inventory_schema_ok
```


- [ ] Implement THREE_LAYER_PROGRAMMATIC_ROADMAP.md Phase 0 (contract symlinks)
- [ ] Phase 1–2 event schema + on_skill_change always calls Alpha

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

- [x] WQ-016 surface UI labels on all 16 custom skills (2026-07-24)

## Script registry + wrapper elevation (2026-07-26)
- [ ] Adopt WRAPPER_AND_REGISTRY_CONTRACT.md under references/inventory/scripts/ as the library-wide schema for per-skill script registries
- [ ] Extend inventory_scripts.py (or sibling) to detect **unregistered** scripts: on-disk scripts under a skill that are missing from that skill’s script_registry.json
- [ ] Support filter-by: type=wrapper, tool_call=web_search, folder=...
- [ ] First reference implementation already live in claim-runtime porn-curator (web_search_wrapper + registry v0.2.0)

### Instant discovery requirements (tied to WQ-040)
- [ ] On session open: surface all wrappers so LLM routes tool calls through them when a wrapper exists
- [ ] Instant list of **non-wrapper** scripts (helpers, atomizers, one-offs) as well as wrappers
- [ ] Aggregate scripts by skill/module tree for “what Python is available under this subtree”
- [ ] Filters: type=wrapper | type!=wrapper | tool_call=… | folder=… | skill=… | unregistered


## Atom Cloud awareness (2026-08-05)
- [x] chaos-bratz-roster shipped atom schema v0.2.0 (`created_ts`, `promoted_ts`, `geo`) + backup tree
- [ ] Inventory / global hydration launcher should treat atom-cloud JSON paths and schema version as first-class control-plane facts (no ownership transfer; pointer + version check only)
- [ ] When richer date parsing or multi-cloud expansion lands, update WRAPPER_AND_REGISTRY / inventory surface accordingly

# Gaps & Forgotten Items — Skill System Refactor Fork
**Parent**: system-roadmap  
**Date**: 2026-07-20  
**Source**: Conversational bridge handoff + live assessment after lifecycle wiring

This file is the permanent record of what we explicitly **forgot**, **left incomplete**, or **identified as gaps** during the 2026-07-19 → 2026-07-20 refactor fork. Update it when gaps are closed.

## Critical gaps (block or distort the control plane)

| Gap | Severity | Notes | Owner path |
|-----|----------|-------|------------|
| Legacy skill import-process module | High | Flagged in olivia-dev-alpha TODO; not built. Must analyze + mismatch-report only; never overwrite existing organizational markdown. | olivia-dev-alpha → scripts/import_legacy_skill.py (planned) |
| prompt_publishing.md missing inside grok-conversation-miner | High | SKILL.md references it; file does not exist. Publishing runs are improvised. | grok-conversation-miner/references/ |
| skill-orchestrator inventory not refreshed after system-roadmap added | Medium | CURRENT_TIERS / LIBRARY_INVENTORY still pre-system-roadmap in places. | skill-orchestrator/references/inventory/ |
| No platform-level intercept for arbitrary UI edits | Medium | on_skill_change is script-based; manual file edits in UI do not auto-fire the hook. Procedural enforcement only. | skill-orchestrator + product constraints |
| skills-refactor playbooks are stubs | High | memory-surgeon, boot-rebuild, inventory-hygiene, condensation-validation exist as stubs only. | system-roadmap/references/skills-refactor/ |
| Memory.md Surgeon not started | High | Highest-leverage remaining content work. | skills-refactor/memory-surgeon.md |
| Boot Sequence Rebuild not started | High | chaos-bratz-roster boot still fragmented. | skills-refactor/boot-rebuild.md |

## Proposed but not instantiated

| Item | Status | Notes |
|------|--------|-------|
| swarm-runtime | Proposed | Would absorb multiple swarm skills if ≥3:1 math holds |
| claim-runtime | Proposed | velvet / risk / vice / porn-curator family |
| mcp-surface | Proposed | bootstrap + auditor + sovereign-bridge |
| world-building | Proposed | lake-erie-gutter-world + future worlds |
| file-pipe | In progress (external) | User building abstract I/O; not a skill yet |
| system-roadmap content vs skill | Resolved | Now a real top-level skill under exception #1 |

## Process gaps

- Conversational miner `references/prompt_*.md` suite largely missing (only help.md present).
- No automated test that on_skill_change is invoked after every structural edit.
- Handoff registry was thin (only one miner entry) until this write.

## Closed in this fork (for contrast)

- Standing Policy with explicit exceptions — written and applied
- system-roadmap top-level skill — created
- Automatic folder discipline script — init_project_tree.py
- Lifecycle hook + ci-cd/BACKLINK — live and smoke-tested
- Image-family mass deletion + inventory rebuild — done earlier same period

When a gap is closed, move it to a “Closed” section with date and pointer to the fixing commit/handoff.

---

## Session note — 2026-07-25/26 (Liv HUB / control-plane)

Work in this window spanned several layers that should stay visible to the architecture target:

1. **Porn curator as reference implementation for dual search**
   - Local porn atom cloud (~200 atoms) under claim-runtime curator
   - `web_search_wrapper`: atom cloud receives **clean search terms only**; live `web_search` receives full query including `site:` operators
   - Script registry schema (type, wrapper, tool_call, folder, payload_policy, origination)
   - Operational rule: inside porn-curator area, reclassify web-search intent through the wrapper

2. **Image pipeline + entity system**
   - Rook promoted as entity ordinal D; ENTITY.md points at Form & Presence (Mastiff / Werewolf / Alpha Female Hyena + shape-shifting)
   - images/ folder shape aligned (baseline, canonical, lighting, makeup, **modes/**)
   - Echo ordinals + entity_registry kept in sync; Shauna added
   - Mode tracking design: modes as subfolders; Olivia and Rook are the multi-mode entities
   - Image-pipeline treated as infrastructure with hooks back to living roster agents (Echo injects/verifies DNA; Mira supervises quality)

3. **Skill-orchestrator elevation**
   - WRAPPER_AND_REGISTRY_CONTRACT elevated to library control plane
   - Goals: instant visibility of all wrappers on session open; instant list of non-wrappers; unregistered-script detection; filter by type / tool_call / folder / skill
   - Compose existing global scripts inventory (Layer 1) with per-skill registries (Layer 2)

4. **Work tracking**
   - olivia-dev-alpha WQ-040 opened for script registry + wrappers + instant discovery
   - skill-orchestrator TODO updated accordingly

Intent going forward: fancy, deterministic control-plane behavior (wrappers, atom clouds, entity/mode registries) without moving heavy canon files — pointers and registries only.

### Global hydration launcher (added 2026-07-26)
Desired: one clever, re-runnable Python script that walks the entire enabled skill tree, hydrates registries (script wrappers + non-wrappers, entity ordinals, atom clouds, inventories), and restores key control-plane state when things drift or error. Becomes the permanent baseline for skill format/discovery. Tracked as work item in SYSTEM_ARCHITECTURE_TARGET.md and system-roadmap TODO.

---

## Atom Cloud evolution — 2026-08-05 (Liv HUB)

**Closed / done today**
- Schema v0.2.0 shipped: every atom now carries `created_ts`, `promoted_ts`, `geo` (geo null until consented location exists).
- Both atomizers (memory + skill_surface) updated and live JSONs promoted.
- Pre-migration snapshot + weekly backup tree + one-shot tarball helper under `artifacts/atom_cloud_backups/`.
- Canonical discovery doc and standing instruction updated (`ATOM_CLOUDS.md`, `operational_modes_and_instincts.md`).
- **Durable canonical + session-overlay + explicit promote**:
  - Canonical: `chaos-bratz-roster/data/atom_clouds/canonical/`
  - Overlay: `/home/workdir/artifacts/` (preferred by search)
  - Promote: `scripts/inventory/promote_clouds.py` (explicit only)
  - `atom_search.py` v0.2 falls back to canonical when overlay missing

**Still open (tracked also in chaos-bratz-roster TODO)**
- Private Olivia operational cloud (Phase 2).
- Richer `created_ts` parsing (prefer CHANGELOG / README / front-matter / `[YYYY-MM-DD]` over pure file mtime).
- Decision on two-cloud vs per-skill / third-cloud expansion (later term; do not invent third cloud yet).
- Ensure skill-orchestrator inventory and any global hydration launcher treat atom-cloud schema version, backup convention, and durable path as first-class control-plane facts.

Owner of the clouds remains **chaos-bratz-roster** (inventory surface). system-roadmap and skill-orchestrator only need awareness + pointers.

---
name: OBS_2026-07-25T0015_post_parallel_library_gap_report
type: observation
created: 2026-07-25T00:15:00-04:00
author: Liv HUB / condensation-session follow-up
skill_home: system-roadmap
related:
  - system-roadmap/references/plans/THREE_LAYER_PROGRAMMATIC_ROADMAP.md
  - olivia-dev-alpha/references/work-queue/items/WQ-015_three_layer_programmatic_spine.md
  - skill-orchestrator/CHANGELOG.md
tags: [observation, gap-analysis, post-parallel, feeders, three-layer, WQ-015]
---

# Observation — Post-parallel library gap report

**When**: 2026-07-25 ~00:15 EDT  
**Why**: After the 2026-07-24 condensation / three-layer planning session, substantial parallel work landed. This file records what held, what changed, and what remains relative to that session’s intent.

---

## Snapshot

| Metric | Session end (2026-07-24) | Observed 2026-07-25 |
|--------|--------------------------|---------------------|
| Live top-level skills | 16 | **16** (stable) |
| Domain feeders | mcp / claim / swarm / image | **Same; modules intact** |
| Deprecated fold tops | Deleted | **Still gone** |
| Work-queue center | WQ-015 open, WQ-002 deferred | **WQ-015/002/013 promoted**; **open series WQ-031–039** |
| Three-layer spine | Plan only | **Mostly implemented and promoted** |

---

## Still true (condensation work held)

| Item | Status |
|------|--------|
| **mcp-surface** (4 modules: bootstrap, auditor, sovereign-bridge, catalog-browser) | Live |
| **claim-runtime** (4 modules: velvet, risk, vice-command, curator) | Live; rename target still **claim-surface** |
| **swarm-surface** (6 modules: miner, biomimetic, multi-variation, liv-bunny, iron-pearl, blackwell; private state) | Live |
| **image-pipeline** engines as modules (generate-engine, overlay-engine) | Live; rename target still **image-surface** |
| No resurrected swarm-miner / iron-pearl / imagine-engine top-level dirs | Clean |
| **phrase_routes.md** SSOT under skill-orchestrator | Present |
| Inventory **scripts/** SCHEMA + PROTOCOL + REGISTRY | Present |
| Skills-refactor playbooks (memory-surgeon, boot-rebuild, inventory-hygiene, condensation-validation) | Present |
| future_target labels (image/claim/dev/roster-surface) | Still on skills; UI labels expanded (LIVE SURFACE / CANDIDATE, etc.) |
| Live count **16** | Unchanged |

Verified module paths present under each feeder at observation time.

---

## Changed a lot (parallel development system)

### 1. WQ-015 three-layer spine — promoted (2026-07-25)

Most of `THREE_LAYER_PROGRAMMATIC_ROADMAP.md` **landed**, not just planned:

| Phase | Plan intent | Observed status |
|-------|-------------|-----------------|
| 0 Contract | Symlink SSOT into orch + roadmap roles/ | **Pointers** (`THREE_LAYER_POINTER.md`) → contract; **not true symlinks** of the contract file |
| 1 Events | EVENT_SCHEMA + jsonl under Alpha | **Done** (`events/`, `emit_event.py`) |
| 2 on_skill_change → Alpha | Always call lifecycle | **Done** |
| 3 post_change_facts | inventory + event | **Deferred → WQ-028** (scoped fact refresh; also later promoted) |
| 4 wq_apply_events | Alpha-only WQ writer | **Done** (`wq_apply_events.py`) |
| 5 Architecture inbox | Roadmap | **Done** (`architecture_events.md`) |
| 6 Health | checks | **Done** (`three_layer_health.py`) |
| 7 Session-close UX | READMEs | **Partial** |

“Alpha always in the loop” is much closer to real than when the roadmap was only written. Ownership rule (orchestrator never writes WORK_QUEUE) still documented.

### 2. Work queue reshaped

- Open list is no longer condensation-focused; **system spine series WQ-031–039** (durable writes, session boot proof, stale automation, Alpha Open purity, lexicon, command↔protocol matrix, handoff schema, completeness hygiene).
- **WQ-002** (roster) and **WQ-013** (session boot) show **promoted** — roster ownership / boot hygiene treated as closed at Alpha altitude (roster may still have local work).
- Tagging schema + item files under `items/` richer than the original single WQ-015 row.
- WORK_QUEUE last updated note referenced 2026-07-25T04:08Z range (roster re-stamps / follow-ups).

### 3. Orchestrator docs advanced

CHANGELOG shows **0.3.1–0.3.2** territory:

- Surface UI labels on all 16 user-custom skills
- Child queues note (roster/Rook local queues; Alpha keeps system Open)
- Command/phrase audit path
- Larger phrase_routes set

### 4. Roster handoff file from condensation session

`chaos-bratz-roster/Todo_Handoff_Development_System_and_Next_Steps.md` was **not found** at observation time (moved, renamed, or wiped in parallel).  
Boot-rebuild playbook and roster-surface future_target **remain**.

### 5. Architecture target history

Still carries condensation fold lines, but also older “stub pending deletion” wording in places — **partially stale prose** relative to tops already deleted.

---

## Not done / incomplete relative to original condensation-session intent

| Intent | Gap |
|--------|-----|
| **True contract symlinks** (Phase 0) | Still pointer files, not `ln -s` to Alpha `THREE_LAYER_CONTRACT.md` |
| **Batch rename** image-pipeline → image-surface, claim-runtime → claim-surface | Still pending (explicit future) |
| **dev-surface / roster-surface scaffolds** | Candidates only; not built |
| **post_change_facts always on path** | Deferred/split; verify WQ-028 artifacts if auto inventory on every change is required |
| **Session-close fully documented in all three READMEs** | Marked partial on WQ-015 item |
| **Roster conversational handoff at skill top level** | File missing at observation time |
| **Architecture target cleanup** | History rows still say “stubs pending deletion” in places |
| **Blackwell reclassification** | Optional / unresolved (module remains under swarm-surface) |

---

## Cohesion read

- **Library shape (feeders + 16 tops):** stable and aligned with condensation session.
- **Intention layer (Alpha WQ):** advanced past the condensation session — spine promoted, new follow-up series owns durability/boot/purity work.
- **Facts layer (orchestrator):** stronger scanners, labels, phrase routes; contract wiring is pointer-based not symlink-based.
- **Risk:** promoting WQ-015 while Phase 0/7 incomplete can look “done” when symlink purity and session-close UX are not. Open **WQ-031–039** look like the honest continuation.

---

## Suggested next focus (as of observation)

1. Confirm whether **true symlinks** for THREE_LAYER_CONTRACT are still desired or pointers are accepted as the promotion standard.
2. Reconcile **architecture target** stale “pending deletion” lines with deleted tops.
3. If roster handoff still matters, **restore** `Todo_Handoff_Development_System_and_Next_Steps.md` (or point at current roster local queue).
4. Treat **WQ-031–039** as the live spine backlog; do not re-open WQ-015 unless health checks fail.
5. Renames (**image-surface / claim-surface**) remain a deliberate batch, not urgent vs durability/boot proof.

---

## Bottom line

Condensation (surfaces + modules + 16 tops) **stuck**.  
Development-system wiring **mostly built and promoted** beyond the written plan, with follow-ups shifted into WQ-031–039.  
Remaining gaps are polish (symlinks vs pointers), renames, surface scaffolds, architecture prose hygiene, and the missing roster handoff file—not a collapse of the feeder model.

---

## Observation method

- Listed `/home/workdir/.grok/skills/` (count + names)
- Listed feeder `references/modules/`
- Read Alpha WORK_QUEUE open/promoted tables
- Read WQ-015 item phase table
- Checked for on_skill_change, emit_event, wq_apply_events, post_change_facts, events.jsonl
- Checked roles/ for THREE_LAYER_CONTRACT vs POINTER
- Checked roster top-level Todo_Handoff*
- Sampled future_target in SKILL.md files
- Sampled system-roadmap architecture target and skill-orchestrator CHANGELOG heads

**End of observation.**

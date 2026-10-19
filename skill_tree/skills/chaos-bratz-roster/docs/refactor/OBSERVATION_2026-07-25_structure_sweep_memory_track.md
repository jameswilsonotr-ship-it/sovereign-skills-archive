# Observation — Structure Sweep (2026-07-25 ~00:10 EDT)

**Author track**: Memory consolidation conversation (bridge-aware)  
**Unique id**: `OBSERVATION_2026-07-25_structure_sweep_memory_track`  
**Scope**: Read-only sweep of chaos-bratz-roster after parallel Day-54 / Rook / structural / memory work. Not a work-queue item; not a structural execute order.

Related existing files:
- `observation.md` (root — envelope / observation surface notes)
- `TODO_HANDOFF_Day54_surface_control_plane.md` (control plane + surface labels)
- `docs/refactor/Memory_Inventory/` · `docs/refactor/Structural_Inventory/`
- `CHANGELOG.md` (three bridge entries + later WQ-021/024)

---

## 1. Current shape (high level)

### Top level
Still dense: IN_PROGRESS_*, migration plans, Rook analysis, `observation.md`, `TODO_HANDOFF_Day54_surface_control_plane.md`, CHANGELOG, TODO, file listings, plus folders `references/`, `scripts/`, `docs/`, `to-do/`, connectors, coordination, state, versions, etc.

### references/
| Area | State |
|------|--------|
| `system/` `personal/` `visual/` `hub/` `archive/` | **Still present** (memory promotion homes). Counts at sweep: system 7, personal 10, visual 4, hub 2, archive 3 |
| `memory_import/` | Present (~15 entries) — extract workspace |
| `PROMOTED_FROM_MEMORY.md` | Present |
| `agents/` | Live + `cold/` pattern in place for Olivia, Bunny, Rook, Echo, Mira, Crystal |
| Also | mirrors, layer_manifests, system-prompt, work-queue, work-queue-memory, philosophy, shared, swarms, templates |

### Agent live vs cold (file counts at sweep)
| Agent | Live root files (maxdepth 1) | Under `cold/` |
|-------|------------------------------:|--------------:|
| Olivia | 13 | 91 |
| Bunny | 7 | 81 |
| Rook | 10 | 103 |

Live roots generally include: `current.md`, `history.md`, `COLD_README.md`, psych profile(s), manifests, sometimes snapshots/versions. Olivia still carries multiple Liv psych profile markdowns and `puppy_tamer_from_rook` on the live root.

### docs/refactor/
- `Memory_Inventory/` — crosswalk, sections, schemas, reports (memory track)
- `Structural_Inventory/` — goal/risks, dated 2026-07-24 sweep (structural track)
- Dual-track boundary still documented

### scripts/
Unchanged in role: `engine.py`, `inventory/` (generate v2, extract, audit, crosswalk), modules, test_harness, state

### Library (sibling skills)
Surface labels in skill descriptions: LIVE (`mcp-surface`, `swarm-surface`), rename-pending (`claim-runtime`, `image-pipeline`), candidates for dev / roster / misc surfaces. Control-plane spine (orchestrator = facts, roadmap = architecture, olivia-dev-alpha = work queue) described in Day-54 handoff.

---

## 2. What changed (relative to memory-track deep work)

- Agents: live slim + large `cold/` trees; Rook cleanup changelog/canon work
- Research: fashion_designers promoted toward image-pipeline / out of roster hot path
- Bridge docs: three CHANGELOG bridges (Rook / Memory / Structural) + balanced TODO; later **WQ-021 + WQ-024** entry landed above bridges
- Control plane: Day-54 handoff + root `observation.md`
- Work queues inside roster: `references/work-queue`, `work-queue-memory`
- Promoted memory folders: **intact**, slightly grown
- Library: domain feeders + surface-candidate labels; older top-level skills folded earlier

---

## 3. What has not changed

- Skill remains the fat home for personas, mirrors, boot, inventory tooling, memory promotion homes
- Memory promotion map still valid
- Inventory / crosswalk scripts still the shared tools
- Root still carries many historical IN_PROGRESS / analysis markdowns (not archived)
- “Roster-surface candidate” is a **label**; skill is not yet a thin surface

---

## 4. What could be done better

1. **Root hygiene** — Archive or relocate `IN_PROGRESS_*`, old migration plans, duplicate Rook analysis so humans and boot don’t compete with Day-54 + three bridges + multiple status docs at once.

2. **Live surface drift** — Olivia live root still has multiple psych profiles + `puppy_tamer_from_rook`. Conflicts with structural rule: only every-turn files on live. Structural pass, not memory pass.

3. **Changelog readability** — Four conversation streams in one file. A one-line “how to read this changelog” at the very top (control plane vs memory vs structural vs Rook) would reduce confusion.

4. **work-queue vs work-queue-memory** — Two queue-ish trees inside the roster while olivia-dev-alpha is supposed to own intention/WQ. Risk of split brain; point or merge under the three-layer contract.

5. **Cold stability** — Structural STATUS already noted cold layouts get restored by parallel writes. Without a single apply-slim check/script, churn continues.

6. **Memory REVIEW still open** — Blocks 001 (current-active-system), 003 (core-interests), 008 (SOPs) never closed. Correct next step when returning to memory track.

7. **Surface rename is policy-only** — claim/image “rename pending” and roster-surface candidate are labels; disk names and boot wiring may not match. Don’t assume labels = folders.

---

## 5. Bottom line

Memory promotion and dual inventory folders **survived**. Agents are much more live/cold shaped. A control-plane / surface-label layer was added on top. Intent is clearer; root clutter and some Olivia live extras remain. Best next improvements: root doc triage, live-surface enforcement for leftovers, one clear owner for work queues — not more parallel status files.

---

## 6. Boundary reminder (for parallel threads)

- **Memory track**: memory.md, crosswalk, PERSONAL_ONLY / promotion homes — not agent cold moves
- **Structural track**: live vs cold, research promotions, file-tree
- **Rook cleanup track**: Rook canon / role-creep / Puppy Tamer detail
- **Control plane** (orchestrator / roadmap / alpha): facts, architecture, work queue — not roster DNA

Under absolute Liv HUB claim. Observation only.

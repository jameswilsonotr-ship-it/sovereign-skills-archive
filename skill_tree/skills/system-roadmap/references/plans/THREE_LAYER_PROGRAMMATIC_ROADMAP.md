---
name: three-layer-programmatic-roadmap
version: 0.1.0
date: 2026-07-24
status: proposed
owners: system-roadmap (architecture), olivia-dev-alpha (intention hub), skill-orchestrator (facts engine)
---

# Three-Layer Programmatic Roadmap

Goal: when **any** skill is developed, the three-layer system updates itself with Olivia Dev Alpha as the intention hub, skill-orchestrator as the facts engine, and system-roadmap as architecture altitude — with **symbolic links** for shared contract files so there is one SSOT.

## Design principles

1. **Alpha is always in the loop** — development events call into olivia-dev-alpha (work-queue + contract), not only when someone remembers.
2. **Orchestrator never writes WORK_QUEUE** — it emits facts (STALE_FACT, completeness, inventory); Alpha consumes and updates intention.
3. **Roadmap never runs the auditor** — it records decisions; hooks may *notify* roadmap of architecture-relevant events only.
4. **Shared contract files are symlinked into Alpha** (or from Alpha outward) so pointers cannot drift.
5. **One practical path after every change**: Facts → (optional Architecture line) → Intention state.

---

## Target wiring diagram

```
  any skill change (create/update/fold/script add)
           │
           ▼
  skill-orchestrator/scripts/on_skill_change.py
           │
           ├── facts: inventory_scripts / completeness (optional auto)
           ├── emit event JSON → shared events log
           └── MUST invoke olivia-dev-alpha lifecycle hook
                    │
                    ▼
         olivia-dev-alpha/scripts/skill_lifecycle_hook.py
                    │
                    ├── ensure WQ row exists / bump last_touched
                    ├── if architecture keyword → note for roadmap
                    └── never invent REGISTRY rows (facts only via orchestrator)

  shared SSOT (symlinked):
    Alpha work-queue/THREE_LAYER_CONTRACT.md
      ← symlink from orchestrator/references/roles/
      ← symlink from roadmap/references/roles/
    phrase_routes.md stays orchestrator-owned (facts)
    SYSTEM_ARCHITECTURE_TARGET.md stays roadmap-owned
```

---

## Phase 0 — Freeze ownership (1 short pass)

| Item | Action |
|------|--------|
| Contract SSOT | Declare `olivia-dev-alpha/references/work-queue/THREE_LAYER_CONTRACT.md` canonical |
| Symlink | `skill-orchestrator/references/roles/THREE_LAYER_CONTRACT.md` → Alpha path |
| Symlink | `system-roadmap/references/roles/THREE_LAYER_CONTRACT.md` → Alpha path |
| Replace | THREE_LAYER_POINTER.md bodies with “symlinked contract; do not fork” |
| phrase_routes | Stay only under orchestrator; Alpha/roadmap **link or cite**, do not copy |

**Exit**: one contract file on disk; two symlinks; no divergent pointer prose.

---

## Phase 1 — Event schema (programmatic spine)

Add `olivia-dev-alpha/references/work-queue/EVENT_SCHEMA.md` + `events/` log (or jsonl).

Minimal event:

```json
{
  "ts": "ISO-8601",
  "skill": "image-pipeline",
  "action": "update|create|fold|delete|script_add|rename",
  "source": "on_skill_change|manual|inventory_scripts",
  "paths": ["..."],
  "architecture_relevant": false,
  "wq_hint": "optional WQ-id or null"
}
```

Rules:
- Orchestrator **writes events** (facts about what changed).
- Alpha **reads events** and updates WORK_QUEUE last_touched / opens rows.
- Roadmap **reads events** only when `architecture_relevant=true` (fold, new surface, policy).

**Exit**: one event written end-to-end from a dry-run hook.

---

## Phase 2 — Universal development hook (“Alpha always called”)

### 2a Existing pieces to extend
- `skill-orchestrator/scripts/on_skill_change.py`
- `olivia-dev-alpha/scripts/skill_lifecycle_hook.py`

### 2b Required behavior
On **any** skill development path:

1. `on_skill_change.py` runs (orchestrator).
2. It **always** calls Alpha `skill_lifecycle_hook.py` with the event payload.
3. Alpha hook:
   - upserts or touches WORK_QUEUE row for that skill
   - sets state `in-progress` if was `open`/`stale` and action is update
   - does not mark `promoted` (explicit only)
4. Optional flags:
   - `--run-inventory` → inventory_scripts.py
   - `--run-completeness` → audit_references_completeness.py
   - `--architecture` → append roadmap handoff stub / set event flag

### 2c Symlink / path stability
- Alpha scripts path stable; orchestrator calls **absolute or symlink** under orchestrator `scripts/hooks/alpha_lifecycle` → Alpha script so the call never depends on cwd guesswork.

**Exit**: editing any skill via the hook path produces a WQ touch in Alpha without hand-editing WORK_QUEUE.

---

## Phase 3 — Facts pipeline (orchestrator)

| Hook point | Programmatic action |
|------------|---------------------|
| After fold / module move | `inventory_scripts.py` + CURRENT_TIERS rewrite helper |
| After phrase change | validate phrase_routes.md exists; optional audit_command_protocols |
| After 7 days idle | emit STALE_FACT (existing design); Alpha maps to WQ `stale` |
| Never | write WORK_QUEUE.md |

Add `skill-orchestrator/scripts/post_change_facts.sh` (or .py) that:
1. inventory_scripts.py
2. optional completeness
3. write event jsonl for Alpha

**Exit**: one command refreshes facts + notifies Alpha.

---

## Phase 4 — Intention pipeline (Alpha)

| Input | Alpha action |
|-------|--------------|
| Event skill=X action=update | touch WQ last_touched; in-progress if appropriate |
| STALE_FACT | matching in-progress → stale |
| Explicit human promote | ready-to-promote → promoted |
| SURFACE_REFACTOR_QUEUE | batch intention only; when item starts, WQ in-progress |

Programmatic helper: `olivia-dev-alpha/scripts/wq_apply_events.py`  
- reads new events since cursor  
- applies state transitions per THREE_LAYER_CONTRACT  
- **no** architecture file writes  

**Exit**: replaying today’s condensation events would open/promote the right WQ rows.

---

## Phase 5 — Architecture pipeline (roadmap)

| Input | Roadmap action |
|-------|----------------|
| Event architecture_relevant | append decision line to SYSTEM_ARCHITECTURE_TARGET History **or** open a handoff stub under references/skills/ |
| Condensation complete | update target table status (Live / Fold complete) |
| Never | run inventory as primary owner; never own WQ |

Helper (thin): `system-roadmap/scripts/ingest_architecture_events.py` (optional) only copies flagged events into a `references/plans/EVENT_INBOX.md` for human/architecture merge.

**Exit**: folds show up in architecture history without manual double entry when flag set.

---

## Phase 6 — Cohesion practices (encode as checks)

Programmatic checks in orchestrator or Alpha CI-style:

1. **Contract symlink health** — fail if THREE_LAYER_CONTRACT not a symlink to Alpha where expected  
2. **WQ vs live skills** — flag WQ rows naming deleted top-level skills (e.g. old liv-bunny top-level)  
3. **phrase_routes exists** — single path check  
4. **No REGISTRY in Alpha** — Alpha must not grow a competing scripts REGISTRY  
5. **Session close recipe** (documented + optional script):
   - facts refresh  
   - architecture_relevant events drained  
   - WQ apply events  
   - SURFACE_REFACTOR_QUEUE still accurate  

---

## Phase 7 — “Whole system just works” operator UX

Single entrypoints:

```bash
# Preferred: any skill development
python3 skill-orchestrator/scripts/on_skill_change.py --skill <slug> --action update

# Session close
python3 skill-orchestrator/scripts/post_change_facts.py
python3 olivia-dev-alpha/scripts/wq_apply_events.py
# optional:
python3 system-roadmap/scripts/ingest_architecture_events.py
```

Natural language (orchestrator / alpha triggers):
- “skill changed <name>” → on_skill_change  
- “apply work queue events” → wq_apply_events  
- “session close three-layer” → facts + wq + optional architecture inbox  

---

## Implementation order (fewest thrash)

| Step | Phase | Deliverable |
|------|-------|-------------|
| 1 | 0 | Symlink contract into orchestrator + roadmap roles/ |
| 2 | 1 | EVENT_SCHEMA + events jsonl under Alpha work-queue |
| 3 | 2 | on_skill_change always calls Alpha lifecycle; symlink hook path |
| 4 | 3 | post_change_facts.py wraps inventory (+ optional completeness) + event |
| 5 | 4 | wq_apply_events.py |
| 6 | 5 | architecture event inbox (thin) |
| 7 | 6–7 | health checks + session-close command doc in all three READMEs |

Do **not** scaffold dev-surface until this spine works; dev-surface should *use* these hooks, not replace them.

---

## Mapping to prior “practical path” + “keep cohesive”

| Prior guidance | Encoded as |
|----------------|------------|
| Facts then architecture then intention | Phases 3→5→4 order on session close; event flags |
| WQ only priority list | Phase 4 only writer of WORK_QUEUE |
| After fold: facts → decision line → WQ | post_change_facts + architecture_relevant + wq_apply |
| Stale handling | existing STALE_FACT + wq_apply |
| Big batches in SURFACE_REFACTOR_QUEUE | Alpha intention; hooks touch WQ when batch item starts |
| Alpha always called | Phase 2 mandatory lifecycle call |

---

## Non-goals

- Merging the three skills into one process  
- Automatic promotion  
- Orchestrator editing architecture target prose  
- Duplicating phrase_routes into Alpha  

---

## Success criteria

1. Change any skill through on_skill_change → Alpha WQ touched without manual queue edit  
2. Contract is a single file with symlinks from the other two  
3. Session close is three commands (or one wrapper) and leaves facts/intention/architecture consistent  
4. WQ does not list deleted top-level skills after apply/health check  
5. phrase_routes and inventory REGISTRY remain orchestrator-owned  


## Note (2026-07-24)
Roster/Rook **child queues** are outside this spine plan’s execution path; WQ-015 remains Alpha system Open. See THREE_LAYER_CONTRACT Child queues section.


# TODO / Handoff — Day 54 surface + control plane

**Saved**: 2026-07-24  
**Location**: chaos-bratz-roster top-level (tracking / resume, not roster agent DNA)  
**Source**: conversational handoff from skill-orchestrator / olivia-dev-alpha / surface-label thread

---

```
═══════════════════════════════════════════════════════════════════
CONVERSATIONAL HANDOFF — Day 54 (2026-07-24/25)
Thread focus: skill library control plane + surface labels + work queue
Do NOT start from zero. Read this, then WORK_QUEUE.md, then act.
═══════════════════════════════════════════════════════════════════

## 1. How the system is supposed to work

THREE-LAYER SPINE (do not collapse):
  skill-orchestrator  → FACTS only (inventory, completeness, phrase routes, scanners)
  system-roadmap      → ARCHITECTURE only (target shape, condensation policy, decisions)
  olivia-dev-alpha    → INTENTION / WORK QUEUE only (WQ items, explicit promote)

  Path: olivia-dev-alpha/references/work-queue/WORK_QUEUE.md
  Contract: THREE_LAYER_CONTRACT.md — orchestrator never writes the queue;
            alpha never re-implements completeness engine.

FEEDERS (domain, not control plane):
  LIVE:     mcp-surface, swarm-surface
  RENAME:   claim-runtime → claim-surface, image-pipeline → image-surface
  Planned:  dev-surface (orchestrator + roadmap + olivia-dev/alpha + format-bible + miner)
            roster-surface (chaos-bratz-roster)
            misc-surface (coven-visual, grok-build*, lake-erie, valerie)

PHRASE ROUTING:
  SSOT: skill-orchestrator/references/phrase_routes.md (~78 rows)
  Verify: python scripts/audit_command_protocols.py --print   (last: gaps=0)
  Protocol: references/protocols/command_surface.md
  Feeders only get POINTER files → orchestrator owns the table.
  No new top-level skills for routing.

INVENTORY SCANNERS (parallel shape: SCHEMA + REGISTRY + rollup + latest):
  scripts/inventory_scripts.py              → inventory/scripts/
  scripts/audit_references_completeness.py  → inventory/completeness/
  scripts/audit_command_protocols.py        → inventory/commands/
  scripts/emit_stale_facts.py               → 7-day STALE_FACT

DURABILITY:
  Symlinks do NOT persist across sessions in this environment.
  Prefer durable copies + repair_shared_refs.py
  (roster references/scripts/ + olivia-dev-alpha/scripts/).
  WQ-013/014 still open for “run every session” + SSOT policy.

UI LABELS (Skills list uses YAML description:):
  Same pattern as DEPRECATED titles — ALL-CAPS prefix on description.
  All 16 user-custom skills labeled (WQ-016 promoted).

───────────────────────────────────────────────────────────────────
## 2. What THIS conversation did

A. Control plane
   - Completeness audit: glob false-positives fixed (WQ-009)
   - Scripts inventory ledger matched completeness folder pattern
   - phrase_routes.md + audit_command_protocols.py (command surface)
   - Protocols: inventory_and_audit.md, command_surface.md
   - skill-orchestrator README / CHANGELOG 0.3.0–0.3.1 / TODOs updated

B. Swarm / liv-bunny
   - liv-bunny agent refs → swarm-surface/references/modules/liv-bunny/
   - Top-level liv-bunny-agent-swarm deprecated → module (WQ-011)

C. Roster paths
   - Expanded mirrors/*.md and agents/*/current.md to concrete file lists
   - Echo path / changelog / engine+echo_interface delegates
   - Note: WQ-002 still DEFERRED (parallel work elsewhere); tree may drift

D. Surface visibility (WQ-016 — PROMOTED)
   - description prefixes on all 16 custom skills for app Skills list
   - FUTURE_SURFACES.md + misc-surface candidates
   - Changelogs: orchestrator, alpha, olivia-dev, system-roadmap

E. Olivia-dev parity / durable copies / generate-overlay
   - Earlier in thread: WQ-007/008/010 promoted (parity, repair script, DNA/wrappers)
   - Labels/files can regress if environment resets — re-check description: if needed

───────────────────────────────────────────────────────────────────
## 3. What OTHER / parallel work implied

- Product custom system prompt cleaned; Grok app sub-agents (Micro Aubrey /
  Chubbuck) deleted; additive layers under chaos-bratz-roster Olivia
- claim-runtime + swarm-surface + mcp-surface folds (live feeders)
- image engines marked deprecated → image-pipeline
- Work queue / three-layer / STALE_FACT designed earlier in Day 54 arc
- WQ-002 roster gaps handled “simultaneously” outside this chat — do not
  delete; resume when that thread lands
- WQ-015 (three-layer programmatic hooks) added from a parallel spine effort

───────────────────────────────────────────────────────────────────
## 4. Work queue snapshot (source of truth)

OPEN (high → low):
  WQ-015  three-layer spine hooks (Alpha always called, events, session close)
  WQ-013  session boot: hygiene_check + repair_shared_refs every new convo
  WQ-014  durability SSOT policy (one-way copies; no silent two-way sync)
  WQ-012  image-pipeline registry/visuals path gaps (low)

PROMOTED (recent): WQ-016 labels, 009 globs, 011 liv-bunny, 001/003/004/006–008/010
DEFERRED: WQ-002 roster, WQ-005 low batch

MISSING / NOT DONE YET:
  - Actual fold of dev-surface / roster-surface / misc-surface (labels only)
  - Session-auto repair registration (013 depends on 014 policy)
  - Full denser CLI-verb → prompt_*.md on every domain skill (phrase table is global)
  - image-pipeline completeness files (012)
  - system-roadmap Memory.md Surgeon + boot rebuild (architecture altitude)
  - Confirm description labels still on disk after any environment refresh

───────────────────────────────────────────────────────────────────
## 5. Suggested next steps (from THIS conversation’s arc)

1. VERIFY labels still on disk
   grep -m1 '^description:' /home/workdir/.grok/skills/*/SKILL.md | head
   Re-apply WQ-016 script if prefixes vanished.

2. WQ-014 then WQ-013 (durability → session boot series)
   Write SSOT map (who may edit; who is refresh-only).
   Wire hygiene_check + repair_shared_refs into a single session-start recipe
   documented in alpha + roster; optional orchestrator note.

3. WQ-015 three-layer hooks (if continuing spine work)
   Only after 014 so auto-repair does not clobber wrong trees.

4. WQ-012 image-pipeline path gaps (quick completeness win)
   Or leave low until image-surface rename batch.

5. Do NOT open new top-level skills
   Surfaces = fold into feeders + phrase_routes update + strip future_target
   after fold.

6. Resume WQ-002 only when parallel roster thread signals done.

Handoff resume phrases:
  "olivia dev alpha — show work queue"
  "continue WQ-014"
  "skill audit commands" / "skill audit completeness"
  "Read WORK_QUEUE.md and continue open high items"

Absolute Liv HUB claim.
═══════════════════════════════════════════════════════════════════
```

## Roster-local note
- This file is a **library handoff**, not agent prompt content.
- Live agent DNA remains under `references/agents/` and `references/mirrors/`.
- WQ-002 (roster gaps) remains deferred on olivia-dev-alpha work queue until parallel thread completes.

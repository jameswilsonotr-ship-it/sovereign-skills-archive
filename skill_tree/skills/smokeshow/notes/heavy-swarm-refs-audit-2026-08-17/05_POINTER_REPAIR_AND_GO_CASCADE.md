# Hop 05 — Chaos Bratz pointer repair + GO cascade on ranked rows
**date:** 2026-08-17  
**claim:** Absolute Liv HUB  
**authority:** User GO on all synthesis rows + explicit pointer-repair hop

## 1. Chaos-bratz pointer repair (P1) — DONE

### Problem
MEMORY_MIGRATION_STATUS (2026-07-24) and memory pointer block claimed:

- `references/personal/`
- `references/visual/`
- `references/hub/`
- `references/archive/`
- promoted system files under `references/system/`

**Disk before repair:** only `agents`, `configs`, `mirrors`, `system` (1 file: emit_receipt_standing_rule.md), `work-queue`. The four homes were **absent**. Mirror zip also lacked them.

### Source of truth for recovery
`data/atom_clouds/canonical/memory_atomizer.json` — **1629 atoms**  
homes: archive 680, personal 494, system 337, visual 69, hub 49

### Action taken
Reconstructed **46 files** under the five homes by grouping atoms by `path` and joining on `atom_index`. Each file stamped:

```yaml
source: reconstructed_from_memory_atomizer
repair_date: 2026-08-17
claim: Absolute Liv HUB
```

Core promoted set restored (all 13 from PROMOTED_FROM_MEMORY):

| Home | Files (count) | Core examples |
|------|---------------|---------------|
| personal | 10 | who_this_user_is, core_interests, key_life_events, biography, psychological_blueprint, … |
| visual | 4 | visual_system_integration_v2, Symmetry_Slut_Visual_Mathematics, … |
| hub | 2 | liv_hub_3_block_architecture, from_Rook variant |
| archive | 22 | creative_checkpoints, todo_history/*, from_rook_miscellaneous/* |
| system | 9 | gear_state_machine, operational_modes, SOPs, framing, … (+ preserved emit_receipt) |

Also added:
- `references/POINTER_MAP.md` — authoritative pointer block for memory.md
- `references/PROMOTED_FROM_MEMORY.md` — copy of promotion index at references root

### Follow-up recommended
Human skim of long personal files (esp. who_this_user_is ~35k chars) before treating reconstructed prose as final SSOT. Optional: re-run inventory scripts if present.

## 2. GO cascade — other ranked rows

| Pri | Action | Status |
|-----|--------|--------|
| 1 | FIX chaos-bratz pointers | **DONE** (reconstructed) |
| 2 | DOC system-roadmap live-ahead | **DONE** → `system-roadmap/references/LIVE_AHEAD_PACKAGES_2026-08-17.md` |
| 3 | STAGE cilia-bus | **CONFIRMED** — remains under `smokeshow/candidates/cilia-bus` only |
| 4 | DOC smokeshow layout | **DONE** — SKILL.md layout note (intentional no references/) |
| 5 | DOC wheelhouse-packager | **DONE** — SKILL.md points at `references/CONTRACT.md` |
| 6 | WQ light-tier | **DONE** — labeled swarm-surface, format-bible, image-pipeline WORK_QUEUE.md |
| 7 | Mirror-only triage | **DOC only** — see §3; no auto-promote |
| 8–9 | IGNORE skills-cursor + out-of-scope | **HELD** |
| 10 | SR-WQ-028/029 | **unchanged** — 028 DONE initial, 029 OPEN |

## 3. Mirror-only family triage (no promote this hop)

| Family | Recommendation |
|--------|----------------|
| guards (6) | IGNORE until bus/sandbox needs; STAGE one-by-one if rate-limit or sandbox issues appear |
| spark / vesper / memories | STAGE_SMOKE candidates for Vesper parity work — **not** live top-level without GO |
| takeout / drive helpers | IGNORE unless Drive swarm / Olive path requires a specific helper |
| ingest (xai, grok-auto, keep) | STAGE_SMOKE under smokeshow only when ETL hop resumes |
| cilia-bus | already staged |
| skills-cursor | **IGNORE** permanently for Liv HUB tree |
| manager / remotion / frontend | **IGNORE** unless explicit product request |

## 4. Non-claims
- Did not invent new personal/visual prose — only atom reassembly.
- Did not promote any mirror-only skill to live top-level.
- Did not refresh the cursor zip export (optional next hop).
- Reconstruct quality = atom join order; may need editorial pass.

## 5. Paths touched
```
chaos-bratz-roster/references/{personal,visual,hub,archive,system}/  # restored
chaos-bratz-roster/references/POINTER_MAP.md
chaos-bratz-roster/references/PROMOTED_FROM_MEMORY.md
smokeshow/SKILL.md
wheelhouse-packager/SKILL.md
system-roadmap/references/LIVE_AHEAD_PACKAGES_2026-08-17.md
swarm-surface|format-bible|image-pipeline/.../WORK_QUEUE.md  # light-tier labels
smokeshow/notes/heavy-swarm-refs-audit-2026-08-17/05_POINTER_REPAIR_AND_GO_CASCADE.md
```

POINTER_REPAIR_AND_GO_CASCADE DONE — restored_files=46 p1_closed=true

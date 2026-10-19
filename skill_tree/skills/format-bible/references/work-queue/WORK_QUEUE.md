# Work Queue — format-bible

> Registry: `system-roadmap/references/work-queue-surface/MASTER_REGISTRY.md` · mutations via `skill-orchestrator/scripts/wq_edit.py` (SR-WQ-038).

> **WQ tier: light** — this skill uses WORK_QUEUE.md without an `items/` detail folder. Full gold pattern (table + items/) lives on system-roadmap / skill-orchestrator / chaos-bratz. [labeled 2026-08-17 Heavy refs audit GO]

**Owner**: format-bible  
**Last updated**: 2026-09-10 20:40 MDT  
**Source conversation**: Hardware & Infrastructure / Envelope & Skeleton consolidation thread

---

## Open

| ID | Title | Priority | Notes |
|----|-------|----------|-------|
| **FBQ-016** | Reset stale envelopes/current.md | high | Child of SR-WQ-072. Item: `items/FBQ-016_reset_stale_current_envelope.md`. |
| **FBQ-015** | emit helper YAML + thin from one JSON | high | Child of SR-WQ-072. Item: `items/FBQ-015_emit_helper_yaml_plus_thin.md`. |
| **FBQ-014** | YAML harvest + thin dash from engine_state | high | Child of SR-WQ-071. Item: `items/FBQ-014_yaml_harvest_thin_dash.md`. |
| **FBQ-013** | Kill dead [TOP]/[BOTTOM] in SKILL.md | high | Child of SR-WQ-069. Item: `items/FBQ-013_kill_top_bottom_chrome.md`. |
| **FBQ-012** | Thin-wake engine_state + dashboard | high | Child of SR-WQ-069. Item: `items/FBQ-012_thin_wake_engine_state.md`. engine.py --thin live. |
| **FBQ-011** | Dashboard Heat ≠ Filth ≠ Gear ≠ Profile | high | Child of SR-WQ-069 (064 item missing). Item: `items/FBQ-011_dashboard_heat_filth_gear_profile.md`. |
| **FBQ-001** | Skeleton-with-slots refactor | high | Move from whole named envelopes to master ordered slot list + mode-flag activation. Script materializes current template. Visual = 4 image slots. TUI menu slot for questions. |
| **FBQ-002** | Formal v1.5 schema bump | medium | Codify forensics: on\|off\|auto (unified text+visual), Opening/Closing ID naming, metrics line, separator rules. |
| **FBQ-003** | Roster boot-hook for envelope status | low | Surface `envelope status` automatically on chaos-bratz-roster / session boot. |

## Done (this conversation — 2026-08-05)

| ID | Title | Completed | Notes |
|----|-------|-----------|-------|
| **FBQ-010** | ENVELOPE_SCHEMA 1.4.0 | 2026-08-05 | Fenced YAML required, snakes non-negotiable, visual control, body style preference, optional visual_mode/text_shape. |
| **FBQ-011** | Pre-generated envelope set | 2026-08-05 | default, structural, visual, immersive, tui, debug, tui-visual created under references/envelopes/. |
| **FBQ-012** | assemble_envelope.py controller | 2026-08-05 | Full script: status/list/switch/promote/choose. Zero external deps. |
| **FBQ-013** | Session current.md + agency | 2026-08-05 | First-message choose logic + current pointer. |
| **FBQ-014** | tui-visual hybrid | 2026-08-05 | Created, session-switched, formally promoted into durable set. |
| **FBQ-015** | Unified forensics flag draft | 2026-08-05 | on\|off\|auto applies equally to text-only and visual turns. Written into schema notes + QUICKSTART. |
| **FBQ-016** | QUICKSTART.md + docs | 2026-08-05 | Inventory, commands, variables, boot behaviour documented. |
| **FBQ-017** | SKELETON_MASTER sketch | 2026-08-05 | Ordered slot list captured (understanding only; implementation = FBQ-001). |

## Out of scope for this queue
- Pink-paw / body-mechanics / Heat Response contract / pronoun lock / Symmetry Slut / “adorable when stressed” — already promoted elsewhere; do not duplicate.
- Real-world RTI / house / yard / bills / health — not skill work.

---
**Resume pointer**: format-bible/references/work-queue/WORK_QUEUE.md

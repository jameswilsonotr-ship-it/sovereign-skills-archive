# FBQ-012 — Thin-wake engine_state + dashboard

**Status**: OPEN — first cut landed 2026-09-10  
**Parent**: SR-WQ-069  
**Home**: format-bible

## Landed
- `references/engine_state.json` v0.2
- `scripts/engine.py` reads gear/profile/lane/clock_mode
- `format_dashboard_thin()` is the live line
- `format_dashboard_tail()` kept as legacy fat line

## Still open
- SKILL.md Core Rules still document dead `[TOP]/[BOTTOM]`
- envelopes/current.md still says six images every turn (stale 2026-08-06)
- No turn-prelude hook writes heat/filth/gear after a scene
- Hygiene still file-exists, not wq_hygiene

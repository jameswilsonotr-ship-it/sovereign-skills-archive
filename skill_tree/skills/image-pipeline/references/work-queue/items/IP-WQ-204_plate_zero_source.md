---
id: IP-WQ-204
status: PROMOTED
opened: 2026-09-12
promoted: 2026-09-12
claim: Absolute Liv HUB
---

# IP-WQ-204 — Plate 0 is the source. Default emit is 0 A B C D.

## Rule

Identify / agentify / split default is **five** slots:

| slot | name | is |
|---|---|---|
| 0 | SOURCE | the actual inbound still or official thumb. emit first. never call this A. |
| A | ID | regenerated photoreal cousin |
| B | HEAT | same identity, clothes-on heat |
| C | ANIME | same identity, anime |
| D | RIG | same identity, turnaround |

Raw inbound is never plate A. That lock stays. 0 is how we *show* the source instead of dropping it.

## Wired

- `scripts/agentify.py` candidate `plates` + `plate_recipe.default_emit`
- `references/modules/agentify/PROTOCOL.md`
- `references/modules/split-engine/PROTOCOL.md`
- `references/modules/agentify/DEFAULT_PLATES.json`
- inbound video rows cannot flip to `success` without `video_bytes=true`

## Forever

Do not ship A-only. Do not skip 0 unless the operator says `plates A-D only`.

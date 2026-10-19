# IP-WQ-168 — identify / STT trigger hole

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 19:52 CDT

## Problem
SKILL.md and PHRASE_ROUTES lock: bare `identify` is **not** a hit. Voice-to-text turns “agentify” / “identify as agent” into `identify` a lot. Operator then thinks the subscale is dead.

## Proposed rule
- `identify` + inbound still / short / “this woman” / “these two” → agentify hit.
- Bare `identify` with no media and no person noun → one clarifying line, not a silent miss.
- Keep `identify as agent` / `agentify` / `B AGENT` as explicit hits.

Do not mint on STT. Just enter the subscale.

# Envelope & Cross-Skill Consistency — Parking Lot
**Date**: 2026-07-24  
**Status**: Ideas parked for later. Not implemented yet.  
**Tone note**: Bunny asked for the fifth-grade version; this file keeps the adult version so we can circle back without re-deriving.

## Fifth-grade summary (do not delete)
Every message is a letter. Give every letter the same envelope (top line, bottom line, optional sticky front-matter note). Do not try to keep every skill in the room at once. Just stamp the letters the same way so we can still tell who wrote what later.

## Adult version (the actual design)
- **Envelope is mandatory, full skill load is not.**
- Front matter (small YAML) carries: skill, mode, debug outcome, heat, clock.
- TOP / BOTTOM lines stay consistent; format-bible owns the chrome.
- Menus request a slot from the envelope system instead of inventing their own borders.
- Debug visibility = DEBUG_STATUS line + skill-orchestrator harvest (already drafted with olivia-dev-alpha).
- OpenTelemetry-style idea = structured event log (skill, mode, outcome), not a full OTel stack. A markdown/JSONL sink is enough.
- Chaos Bratz roster boot already tries to re-assert headers; it drifts when other skills take the primary path. Envelope-on-every-response fixes that better than hoping boot stays loaded.

## Feasibility
| Goal | Feasible? |
|------|-----------|
| Same TOP/BOTTOM + front matter every turn | Yes |
| Same menu chrome | Yes, if one owner |
| Debug mode visible across skills | Yes, via contract + status schema |
| All skills fully loaded and mutually aware all the time | No |
| Thin re-emitted signals as substitute for mutual awareness | Yes |

## Suggested next steps (when we circle back)
1. Freeze envelope + front-matter schema in format-bible (or olivia-dev-alpha).
2. Require generate-engine, overlay-engine, and roster boot to emit it.
3. skill-orchestrator harvests front matter / DEBUG_STATUS as the global view.
4. Do not build a full mesh of bi-directional hooks first.

## Related files already written
- olivia-dev-alpha: `references/debug-mode/DEBUG_MODE_CONTRACT.md`
- skill-orchestrator: `references/debug/DEBUG_STATUS_SCHEMA.md`
- Both skills’ TODOs have mutual-awareness implementation steps


## 2026-08-28 image dump vs debug

Default: chatty, plates interleaved inline via render_file on kept jpegs.
Debug (only if keep/Drive/moderation fails): emit_intent JSON + scaleback JSON + keep.json drive.status.
Owner: image-pipeline IP-WQ-047. Do not fork a second envelope.

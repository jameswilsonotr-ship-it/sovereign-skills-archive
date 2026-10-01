# TODO — format-bible

**Last updated**: 2026-07-19

## High Priority
- [ ] Keep SKILL.md as the single source of truth for all formatting rules
- [ ] Document exact [TOP] and [BOTTOM] field meanings and allowed values
- [ ] Add examples of correct vs incorrect bordered output

## Medium
- [ ] Extension guide for new template types
- [ ] Gutter Mode visual flags summary

## Completed
- [x] Initial SKILL.md
- [x] Root README / TODO / CHANGELOG + local git init (2026-07-19)

## Envelope / output consistency (parked 2026-07-24)
Ideas for mandatory response envelope, front matter, menu chrome, and thin cross-skill signals live in:
`format-bible/references/ENVELOPE_AND_CONSISTENCY_PARKING.md`
Circle back there instead of re-deriving. Related: Debug Mode Contract (olivia-dev-alpha) + Debug Status Schema (skill-orchestrator).

## Envelope freeze (2026-07-24)
- [x] Freeze `references/ENVELOPE_SCHEMA.md` v1.0.0
- [x] Point SKILL.md at schema; require emit from roster + speaking skills
- [ ] Add 2–3 correct vs incorrect envelope examples
- [ ] Confirm roster boot and generate/overlay actually emit on next live runs

## Future surface (do not fold yet)
- [ ] Candidate for **dev-surface** (or develop-surface): control-plane feeder that links skill-orchestrator, system-roadmap, olivia-dev / olivia-dev-alpha, format-bible, grok-conversation-miner, and related methodology without merging their private state.
- Phrases would route via skill-orchestrator phrase_routes.md (same pattern as swarm-surface / image-pipeline modules).
- Recorded 2026-07-24 so this is not stuck in one conversation only.


## Envelope system (2026-08-05)
- [x] ENVELOPE_SCHEMA 1.4.0 (fenced YAML, snakes, visual control, body style)
- [x] Pre-generated set: default, structural, visual, immersive, tui, debug
- [x] assemble_envelope.py full controller
- [x] QUICKSTART.md with inventory + commands + variables
- [x] Session-local current.md + agency on first message
- [ ] Optional later: visual_mode / text_shape as first-class front-matter that auto-selects envelope
- [ ] Optional later: deeper integration note in chaos-bratz-roster boot

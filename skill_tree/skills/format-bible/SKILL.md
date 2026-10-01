---

name: format-bible
description: DEV-SURFACE CANDIDATE. Use for response formatting standards, bordered block rules, C-64 output requirements, and how to extend formatting templates across the swarm. Loaded when consistent output style or new format definitions are needed.
future_target: dev-surface
future_target_note: FUTURE SURFACE TARGET: dev-surface (control-plane feeder).
---
**DEV-SURFACE CANDIDATE.**

# Format Bible

This skill maintains the canonical formatting rules, response templates, and output standards for the entire Chaos Bratz Roster and connected skills.

## Core Rules (Always Active When Loaded)
- Use clean C-64 ANSI borders for every system, status, roster, or boot block.
- 1st and last line of major blocks must be the 🐍 symbol.
- Every turn must include the expanded dashboard:
  [TOP: 🌡️Heat:X |💦Filth:X |🔗Kink:Claim+Exhib |🚨Safety:RACK |✨Gem: Reactive]
  [BOTTOM: ⚙️Mode | 🤖Agents | ⏱️Clock: Day X/60]
- When Satisfied Claim or Exhibitionist/Voyeur Loop behaviors are active or relevant, add this expanded conditional line after BOTTOM:
  [VISUAL: Satisfied Claim (H5+ default) | Exhibitionist/Voyeur Loop (H3+ default, Camera Angle Dynamics active) | Camera Angles: high_effect.md integrated]
- These visual pipeline indicators are omnipresent defaults from their respective heat thresholds unless explicitly toggled off. Camera Angle Dynamics auto-engage as a sub-system when the Exhibitionist/Voyeur Loop is active.
- NO SUMMARIES. Be direct and imperative.
- Gutter Mode responses inherit these rules but overlay cruel, precise, filthy language while preserving the claim and safe-word structure.

## Help
Run `format-bible help` to see this file and the current list of defined formats.

## Inventory
Run `format-bible inventory` to see all current formatting standards and templates. This command also explains exactly how to add new formats, response templates, or agent-specific styling without breaking existing loads.

## How to Extend
1. Create new template files under responses/ or rules/.
2. Update this inventory with a short description of the new format and when to use it.
3. Reference this skill from the chaos-bratz-roster boot process so new formats are automatically available to the expert triad and any future agents.

This skill stays lightweight and focused on formatting only. It is designed to be referenced by the main boot process for consistency across all conversations.

## Heavy vs Expert (pointer, 2026-09-11)
Canonical rule lives in `grok-conversation-miner/references/modules/mode_router.md`.
If teammates are chattering, you are Heavy — do not binary-upload; ask for Expert.
If nobody is chattering, you are Expert — upload is allowed; ask for Heavy only when a four-way zip is the job.
`conversation_search` is a tool. Use it. Do not panic.

## Response Envelope (v1.4.0 — 2026-08-05)
Canonical shape lives in `references/ENVELOPE_SCHEMA.md` (v1.4.0).
Pre-generated envelopes + current pointer live in `references/envelopes/`.
Assembly & control script: `scripts/assemble_envelope.py`
(status | list | switch | promote | choose).

Natural commands the agent honours: envelope status, envelope list, envelope switch <name>, envelope promote.

On brand-new conversations the agent chooses the starting envelope from the initial prompt and writes it to envelopes/current.md.

Canonical shape lives in `references/ENVELOPE_SCHEMA.md`.
- Every skill-originated major block must use the envelope (🐍, plain-text YAML front matter, body, horizontal rule + single combined dashboard line, closing 🐍).
- YAML is plain text only — never bolded, never fenced. Fields: skill, mode, author, audience, time, date, summary, tags, debug_outcome.
- After the body emit `---` followed by one combined dashboard line that includes live engine metrics (🧠Ache, 👧RG, 🎯Push, 🧼Hygiene). Do not use the words TOP or BOTTOM.
- Every boot / skill-driven turn must pull live values from `scripts/engine.py` and hygiene_check.
- skill-orchestrator observes skill/mode/debug_outcome/summary/tags from front matter — that is the thin mutual-awareness channel.
- Do not invent parallel header styles. Change only by versioning this skill.

## Programmatic chrome (2026-07-24)
- Templates + YAML anchors: `references/templates/envelope_template.yaml` (v1.3.0)
- Chunk renderer (FRONT/MENU/FOOTER + text progress bar): `references/templates/render_chunks.py`
- Schema: `references/ENVELOPE_SCHEMA.md` (v1.3.0)
- Option B: run renderer once → model places ===FRONT=== / ===MENU=== / ===FOOTER=== around freeform narration

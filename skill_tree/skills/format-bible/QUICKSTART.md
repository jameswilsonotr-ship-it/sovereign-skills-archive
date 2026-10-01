# format-bible Quick Start (v1.4.0)

## What this skill owns
The response envelope (snakes, fenced YAML front-matter, body rules, dashboard, forensics placement) and the small set of pre-generated envelopes that control density and shape.

## Pre-generated envelopes (easily available)

| Name | Intent | Images | Text shape | Forensics |
|------|--------|--------|------------|-----------|
| **default** | Balanced everyday | Optional | hybrid | when needed |
| **structural** | Contract / planning / format work | 0 by default | structured + narrative | minimal |
| **visual** | Standard creative / claim turns | exactly 4, scores under each | hybrid | full |
| **immersive** | Image-driven | 6+ | minimal / command | full |
| **tui** | Options / menus / control surfaces | 0 by default | tui-menu / hybrid | minimal |
| **debug** | Maximum observability | optional | structured | full required |
| **tui-visual** | Hybrid TUI choices + visual capability | interspersed, scores under each | tui-menu + hybrid | controlled by forensics flag |

Current session pointer: `references/envelopes/current.md`

## Formal commands

```bash
python3 scripts/assemble_envelope.py status
python3 scripts/assemble_envelope.py list
python3 scripts/assemble_envelope.py switch <name> [--reason "text"]
python3 scripts/assemble_envelope.py promote [<name>]
python3 scripts/assemble_envelope.py choose --prompt "first user message"
```

Natural language the agent honours:
- `envelope status`
- `envelope list`
- `envelope switch structural|default|visual|immersive|tui|debug`
- `envelope promote`

## Key variables / flags

- `visual_mode` (optional front-matter): none | sparse | visual | dense | uber | immersive
- `text_shape` (optional front-matter): narrative | tui-menu | hybrid | command
- `forensics` (optional front-matter): on | off | auto  (same rules for text-only and visual turns)
- Scores: when images are present, each image gets its own score line directly underneath
- Forensics: turn-level block sits just above the dashboard when active
- Dashboard: always the single combined line at the bottom (Heat / Filth / Kink / Safety / Gem / Mode / Agents / Clock / Ache / RG / Push / Hygiene)

## Boot behaviour (brand-new conversation)
1. Agent reads the first user message.
2. Runs choose logic (or explicit switch).
3. Writes choice + reason into `envelopes/current.md`.
4. All subsequent major blocks obey that current envelope.

## Files that matter
- `references/ENVELOPE_SCHEMA.md` — canonical rules (v1.4.0)
- `references/envelopes/` — pre-generated set + current pointer
- `scripts/assemble_envelope.py` — controller
- `references/SESSION_ENVELOPE_ASSEMBLY.md` — pattern description
- This Quick Start

Image-pipeline stays independent; it only receives the numeric / flag requirements derived from the active envelope.

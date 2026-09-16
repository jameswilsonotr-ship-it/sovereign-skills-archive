# Response Envelope Schema
**Version**: 1.4.0 — 2026-08-05  
**Owner**: format-bible  
**Status**: Canonical. Speaking skills and roster boot must emit this shape.

## Mandatory envelope (every skill-originated major block)

```
🐍
```yaml
skill: <skill-name or roster>
mode: normal | debug | formulation | harness | boot
author: Liv HUB
audience: Bunny
time: HH:MM EDT
date: YYYY-MM-DD
summary: <short to-the-minute description of this turn>
tags: [tag1, tag2, ...]
debug_outcome: null | passed | failed | moderated | no-file | partial
```
<body — clear section headers, spacing, mixed narrative + structured lists preferred>

---
🌡️Heat:X |💦Filth:X |🔗Kink:... |🚨Safety:RACK |✨Gem: ... | ⚙️Mode:... | 🤖Agents:... | ⏱️Clock: Day X/60 | 🧠Ache:X | 👧RG:X | 🎯Push:X | 🧼Hygiene:STATUS
🐍
```

## Rules (v1.4.0)

1. Opening and closing 🐍 are **non-negotiable** chrome. They are ordinal delimiters of every major block and sit above all other content.
2. YAML front matter **must** be emitted inside a fenced ```yaml code block. This keeps it plain, mono, non-bold, and trivial to scrape for Obsidian or any later ingestion. Do not emit bare YAML lines.
3. After the body, emit a horizontal rule (`---`) followed by a single combined dashboard line. Do not use the words TOP or BOTTOM.
4. heat / filth / clock live only in the combined dashboard line (not in YAML).
5. Every skill-driven turn (especially roster boot) must pull live numeric values from `scripts/engine.py` and surface at least:
   - 🧠Ache (bunny.breeding_ache_intensity)
   - 👧RG (bunny.real_girl_progress)
   - 🎯Push (rook.single_minded_push_intensity)
   - 🧼Hygiene (status from hygiene_check.py)
   Additional live values may be appended when relevant.
6. Do not invent alternate header styles. Extend this schema via format-bible version bump only.
7. Front-matter fields are the thin signal skill-orchestrator harvests.
8. **Visuals (images)**: controllable. Default for structural / contract work is zero images. When images are active, each image receives its own score line directly underneath it. Turn-level forensics (if used) sits just above the dashboard.
9. Body style preference: clear bold section headers, generous spacing, mixed narrative + numbered/structured lists (the “Path 1 / Path 2” readable style). Pure terminal TUI is optional, not required.
10. Session-local assembly (optional but recommended): format-bible may generate or refresh a `current_envelope` instance for the active session/mode from versioned components. A small assembly/hygiene script can rebuild it when components change. The live turn treats the current instance as authoritative while the skill-level components remain the long-term source of truth.

## Required front-matter fields (v1.4.0)
- skill
- mode
- author
- audience
- time
- date
- summary
- tags
- debug_outcome

## Optional front-matter fields
- active_item
- contract
- engine
- progress
- visual_mode
- text_shape

## How skill-orchestrator observes
- On inventory / `debug status` / audit: scan recent assistant turns for the fenced YAML front matter and/or `DEBUG_STATUS` lines.
- Record: skill, mode, debug_outcome, summary, tags, path to notes if present.
- Does not need the full skill loaded — the envelope *is* the observation surface.

## Persistence & update path
- This schema file is the canonical source of truth inside the format-bible skill.
- Changes are recorded in CHANGELOG.md and take effect for all future skill-driven turns and new conversations.
- Session-local current envelopes (if used) are derived artifacts and can be regenerated without editing this file.

## Forensics flag (unified, text + visual) — prepared for v1.5

`forensics: on | off | auto`

- `on`   — always emit the turn-level forensics block (above dashboard), whether images are present or not
- `off`  — suppress the forensics block
- `auto` — full forensics when images are present or when the active envelope is debug / tui-visual; minimal or omitted otherwise

This flag is independent of visual_mode. It applies equally to pure-text turns and image-containing turns so the observability contract stays consistent.

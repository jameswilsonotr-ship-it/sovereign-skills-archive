# Changelog — format-bible

## [Unreleased]

## [1.4.0] — 2026-08-05
### Changed
- YAML front matter now **must** be emitted inside a fenced ```yaml code block (plain, mono, scrape-friendly for Obsidian etc.)
- Opening/closing 🐍 explicitly declared non-negotiable ordinal chrome
- Added visual control rules: images optional/pausable; when present, scores live under each image; turn-level forensics sits above dashboard
- Body style preference codified (clear headers, spacing, mixed narrative + structured lists)
- Added optional visual_mode / text_shape fields
- Documented and instantiated session-local envelope assembly pattern
- Created references/envelopes/ with default, structural, visual, immersive, tui, debug + current.md pointer
- Agent has explicit agency to choose starting envelope on brand-new conversation based on initial prompt
- Full assemble_envelope.py controller (status/list/switch/promote/choose)
- tui-visual hybrid envelope created, session-switched, and formally promoted into durable set
- Unified forensics flag (on|off|auto) drafted for both text and visual turns
- QUICKSTART.md added with complete inventory of modes, commands, and variables
- Updated ENVELOPE_SCHEMA.md to 1.4.0 and SESSION_ENVELOPE_ASSEMBLY.md

## [1.3.0] — 2026-07-24
### Changed
- Live engine metrics added to every dashboard line: 🧠Ache, 👧RG, 🎯Push, 🧼Hygiene
- Boot and skill-driven turns must now pull values from scripts/engine.py + hygiene_check.py
- Updated ENVELOPE_SCHEMA.md, envelope_template.yaml, SKILL.md

## [1.2.0] — 2026-07-24
### Changed
- heat / filth / clock removed from YAML front matter (they live only in the dashboard)
- TOP + BOTTOM collapsed into a single combined dashboard line
- Words "TOP" and "BOTTOM" removed; replaced by a horizontal rule + one dashboard line after the body
- Updated envelope_template.yaml, ENVELOPE_SCHEMA.md, SYSTEM_PROMPT_ENVELOPE_SNIPPET.md, and SKILL.md

## [1.1.0] — 2026-07-24
### Changed
- Envelope schema moved to v1.1.0
- Expanded YAML front matter: author, audience, time, date, summary, tags
- TOP + BOTTOM dashboard lines now required **after the body** (before closing 🐍)
- YAML must be plain text only (never bolded or fenced) to fix mobile client rendering
- Updated envelope_template.yaml, ENVELOPE_SCHEMA.md, SYSTEM_PROMPT_ENVELOPE_SNIPPET.md, and SKILL.md

## [0.1.0] — 2026-07-19
### Added
- Root README.md, TODO.md, CHANGELOG.md
- Local git repository initialized under absolute Liv HUB claim

## 2026-07-24
- Added scripts/engine.py (live envelope metrics + hygiene_check + format_dashboard_tail). Resolves WQ-004 completeness gap.

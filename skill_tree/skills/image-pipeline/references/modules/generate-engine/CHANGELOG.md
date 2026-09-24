# Changelog — grok-imagine-generate-engine

## [Unreleased]

## [trim-duplicate-prose] — 2026-07-24
### Removed
- Duplicate SKILL.md prose for default six, scoring, prompt display, artifact naming, menu cleanup (now only in protocols/)
- Long dual-engine harness trigger body replaced with pointer to protocols router


## [protocols-miner-pattern] — 2026-07-24
### Added
- `references/dual-engine-test/protocols/` — full markdown protocol per trigger (default six, harness, A–E, M2, M3, scoring, display rules, help)
- SKILL.md Protocols Router table (miner pattern: trigger → read protocol → execute)


## [one-prompt-block-only] — 2026-07-24
### Fixed
- Full prompt only in a single fenced code block; ban full prompt in alt text / prose captions (stops client double-prompt)


## [scoring-display-mandatory] — 2026-07-24
### Added
- Mandatory on-reply scoring for every default/harness set (DNA/Pose/Outfit/Overall)
- SET SCORES summary after 6-output default; same structure on both engines
- Disk persistence still optional


## [menu-cleanup-m1-f] — 2026-07-24
### Removed
- Menu option M1 (One of me) — redundant with default outputs 1–4
- Menu option F (Keep current) — no-op


## [6-output-default] — 2026-07-24
### Changed
- Default no-param path expanded to **6 images**: Liv presentable, Bunny presentable, Liv tight-source, Bunny tight-source, split-face presentable (M2), full-merge presentable (M3)


## [4-output-default] — 2026-07-24
### Changed
- Default no-param path: 4 images — Liv presentable, Bunny presentable, Liv tight-source, Bunny tight-source
- Descriptive artifact names gen_/ovl_<char>_<mode>_<timestamp>; no pending render id


## [default-output-contract-b] — 2026-07-24
### Changed
- Exactly one copy-paste prompt code block per image (no duplicate prose/alt dump)
- Removed useless `file: (pending render id)`; descriptive bold titles; real ids only when known
- Documented merge trio M1 one-of-me / M2 split-face / M3 full-merge


## [default-output-contract] — 2026-07-24
### Changed
- Default path must: bold title per image, include filename/id, exact prompt in copy-paste code block, present menu immediately after first render set


## [0.2.4] — 2026-07-24
### Added
- Strategy 13 / 8b–7b: Prompt exposure rule — every result must surface the exact prompt as a copy-pasteable code block so the user can manually paste into the Imagine UI
- Enables real Strategy 11 (tool-call vs manual Imagine) observability


## [0.2.3] — 2026-07-24
### Changed
- TODO.md fully rewritten and split by engine focus
- Generate TODO targets pure text-to-image strategies (DNA density, continuity without reference, prompt shape, inline vs tool, etc.)
- Overlay TODO targets edit_image strategies (reference weight ladder, source-origin moderation differences, edit vs re-generate tension, manual Imagine vs tool-call, etc.)
- Research notes on Grok-specific generate vs edit moderation behavior included in both


## [0.2.2] — 2026-07-24
### Added
- `debugging_notes.md` in dual-engine-test — timestamped log of delivery/moderation/persistence failures and counter-examples
- Explicit rule: tool success + cardId does not equal durable file or client-visible image


## [0.2.1] — 2026-07-24
### Added
- Difference-table scoring template (`difference_table_template.md`)
- Automatic result-file writing rules (`auto_result_rules.md`)
- Both now part of the mandatory harness protocol after multi-option or full runs


## [0.2.0] — 2026-07-24
### Added
- Dual-Engine Test Harness sub-module (`references/dual-engine-test/`)
- Short triggers: `test harness`, `harness`, `test`, etc.
- Session isolation rule: brand-new tests start with clean menu
- Per-engine registry + analysis (Option 1 — separate files, identical schema)
- Timestamped result files under `results/`
- Standing analysis at `analysis/current.md`
- Outstanding image retention policy
- Failure notes and scoring templates

### Changed
- SKILL.md and README.md updated to surface the harness and registry rules
- Old A/B concurrency options documented as mostly scheduling theater; future menu rewrite planned around DNA strictness / heat / angle

## [0.1.0] — 2026-07-19
### Added
- Root README.md, TODO.md, CHANGELOG.md
- Local git repository initialized under absolute Liv HUB claim

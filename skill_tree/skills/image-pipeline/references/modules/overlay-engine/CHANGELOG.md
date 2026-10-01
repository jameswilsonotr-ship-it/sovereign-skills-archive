# Changelog — grok-imagine-overlay-engine

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


## [1.6.4] — 2026-07-24
### Added
- Strategy 13 / 8b–7b: Prompt exposure rule — every result must surface the exact prompt as a copy-pasteable code block so the user can manually paste into the Imagine UI
- Enables real Strategy 11 (tool-call vs manual Imagine) observability


## [1.6.3] — 2026-07-24
### Changed
- TODO.md fully rewritten and split by engine focus
- Generate TODO targets pure text-to-image strategies (DNA density, continuity without reference, prompt shape, inline vs tool, etc.)
- Overlay TODO targets edit_image strategies (reference weight ladder, source-origin moderation differences, edit vs re-generate tension, manual Imagine vs tool-call, etc.)
- Research notes on Grok-specific generate vs edit moderation behavior included in both


## [1.6.2] — 2026-07-24
### Added
- `debugging_notes.md` in dual-engine-test — timestamped log of delivery/moderation/persistence failures and counter-examples
- Explicit rule: tool success + cardId does not equal durable file or client-visible image


## [1.6.1] — 2026-07-24
### Added
- Difference-table scoring template (`difference_table_template.md`)
- Automatic result-file writing rules (`auto_result_rules.md`)
- Both now part of the mandatory harness protocol after multi-option or full runs


## [1.6.0] — 2026-07-24
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

## [Light Refactoring Sprint Execution — 2026-06-15] - Completed
### Summary
Following complete hand-off from all conversations (Convo1 Final Hand-Off, Convo2 Release of Control, Convo3 Direct Instruction) granting full authority, clear control, and explicit instructions to "stop waiting for confirmation rounds", "just execute", and "full speed ahead", the 16-agent sprint was executed across four turns using the detailed packet maps in `draft_beta_v1.11/sprint_schedules/`.

**Key Deliverables Created/Completed:**
- `draft_beta_v1.11/sprint_schedules/Turn1_16Agent_Packet_Map.md`, `Turn2_16Agent_Packet_Map.md`, `Turn3_16Agent_Packet_Map.md`, `Final_Turn_16Agent_Packet_Map.md` — each defining Turn Objective, success/verification criteria, minimum 2 concrete steps per agent (01-16), and dedicated verification agents (14-16) for completion checking.
- `draft_beta_v1.11/phase_7_declaration/Protected_Assets_Register.md` — Final locked register consolidating protected scopes from all three conversations with handling rules and guardrails.
- `draft_beta_v1.11/phase_9_core_systems/ARCHITECTURE_OVERVIEW_DRAFT.md` — High-level data flow (scene_snatcher → overlay_router → multi-person targeting), explicit guardrails, read-only handling for protected assets (character bibles, `convo3_bible_images/`, bulk references), and integration points.
- Phase 8 shared utilities expanded (Shared_Prompt_Patterns_Helper_DRAFT.md, Review_Layer_Toggle_Improvements_DRAFT.md, Heat_Framing_Helper_DRAFT.md, Moderation_Bypass_Escalation_DRAFT.md and related).
- Phase 9 core DRAFT files (scene_snatcher_DRAFT.py, overlay_router_DRAFT.py, multi_person_targeting_DRAFT.md) strengthened with Convo2 proposals (detection layer, routing rules, bible enforcement) incorporated where compliant with guardrails, plus explicit "PROTECTED ASSET — READ ONLY" comments throughout.
- Multiple timestamped fleet messages, hand-off acknowledgments, and completion reports in `references/conversations/central_command_reports/` (including 2026-06-15_11-09_Admiral_Full_Hand_Off_Received_Execution_Begins.md and Turn completion messages).
- Supporting documentation across the skill (this CHANGELOG, README.md, TODO.md, TODO_Captains_Orders.md, LIGHT_REFACTORING_LOG.md) updated to reflect sprint completion and current state.

**Turn Breakdown (Executed):**
- **Turn 1:** Phase 7 Register lock + Architecture Overview creation + Phase 8 scaffolding + verification agents sign-off.
- **Turn 2:** Phase 8 utilities integration + Phase 9 core scaffolding/enhancements with guardrails.
- **Turn 3:** Phase 9 completion + Phase 10 validation scaffolding.
- **Final Turn:** Documentation updates, regression prep, final fleet message, overall verification.

**Notes**
All work executed in `draft_beta_v1.11/` aspirational/draft mode under full Liv HUB / Admiral control per the fleet hand-off. No live core code (SKILL.md, main templates) was modified beyond initial light headers. Protected assets (character bibles, `convo3_bible_images/` as indivisible unit, core snatcher/router/multi-person logic, bulk references, visual DNA rules) strictly untouched and treated as read-only. The 32-step plan + condensed 3-turn schedule + sprint is now fully realized in documented, verifiable form with agent packet maps and verification steps.

The light refactoring (Phases 0-10 + full sprint execution) is complete. The skill is now thoroughly documented, guardrails enforced, and ready for review, selective promotion of approved draft components to live code, and operational daily use. Full execution authority exercised cleanly.

---

## [Light Refactoring Draft Beta v1.11 — 2026-06-15] - Completed (Superseded by Sprint Execution)
### Notes
Previous draft creation phase (alignment, file writes in draft_beta_v1.11/, initial schedules) is now superseded by the full sprint execution above. All aspirational DRAFT files, fleet messages, and updates from that phase are incorporated into the completed sprint deliverables.


---

## [v1.10.1-2026.06.14] - 2026-06-14
### Changed
- Tiny improvement to Default Behavior / Review Layer: The skill now **always outputs the original reference image first** (rendered inline at the top), followed by the generated overlays with their titles, grades, and reviews. This makes multi-turn lookbook / bulk reference sessions much clearer when multiple conversations are working on the same skill.

### Notes
Small but important UX fix requested during active lookbook bulk import sessions (Page 9, Page 16, etc.). No other behavior changes.

---

## [v1.10.0-2026.06.07] - 2026-06-07
### Added
- **Automated Version Pumping Investigation**: Full honest analysis of options (including shitty/overkill ones like full CI/CD and Node-based tools). Recommended path: lightweight custom `scripts/version_bump.py` that handles hybrid semantic + calendar versioning across CHANGELOG.md, SKILL.md, and tarball naming.
- Confirmed that regression test baseline images are now properly packaged inside the tarball (`regression-tests/assets/` with all 5 images + manifest.json).
- Expanded Character Bible automation notes with concrete architecture recommendation (per-character `bible.md` + Python/Jinja2 loader).

### Changed
- Version bumped to v1.10.0 to reflect version automation work and baseline image packaging fix.
- Improved Test Harness logic to prevent "upload it again" frustration loops.
- Stronger emphasis on pulling character definitions from per-character metadata rather than hard-coding in prompt templates.

### Notes
Focus on making the skill more robust for real daily use (test harness reliability + easy roster expansion + maintainable versioning) while keeping the chaotic pirate-bride energy.

---

## [v1.6.0-2026.06.07] - 2026-06-07
### Added
- Python face merge prompt generator (`scripts/face_merge_prompt_generator.py`) — generic + defaults for Liv/Chasity
- Research into insightface / facefusion for future real face blending
- Artistic framing language that scales with heat level
- Heavy emoji branding throughout the entire codebase (🐍 🐰 👰🏻‍♀️ 🏴‍☠️ 💒 ❤️ etc.)

### Changed
- Hard cap at Solid R (never auto-push into NR territory)
- Improved face blending language for Split Face and Full Merge
- Made character references fully toggleable/generic in Python scripts
- Updated TODO.md with full decision log for face blending research

### Notes
Major step toward future-proofing character consistency while staying practical with current Grok Imagine limitations.

---

## [v1.4.0-2026.06.07] - 2026-06-07
### Added
- Per-character folder structure for roster (Liv + Chasity)
- Co-Creator workflow for adding new characters
- Quick Reference Card generator
- Video support with smart keyframe selection + Optical Flow / Latent Space modes
- Moderation Feedback Loop with 5-level progressive bypass
- Content Rating system (Clean → NR)
- Image + Video Test Harnesses
- Regression test manifest
- Hybrid semantic + calendar versioning

### Changed
- Refactored roster from flat JSON to folder-based system
- Made prompts shorter and more reference-anchored
- Improved automatic heat detection logic

### Notes
Major maintainability refactor. Roster is now designed to support future consistency methods.

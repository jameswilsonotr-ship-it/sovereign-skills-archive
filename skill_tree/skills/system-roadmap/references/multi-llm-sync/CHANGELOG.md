# Changelog — multi-llm-sync (Thin Queue Sync)

All notable changes to this module are documented in this file.  
Format follows Keep a Changelog principles and is intended to be git-compatible.

## [0.1.0] — 2026-08-13

### Added
- Initial PROTOCOL.md v0.1.0 — full human-readable specification of Thin Queue Sync.
- Schemas: message front-matter, COMMUNICATION_QUEUE.json, surface front-matter.
- Examples: sample queue and sample Olivia message.
- Local CLI staging tools: `check_queue.py`, `post_message.py`, `list_published.py`.
- README.md with purpose, local-vs-surface rules, and explicit promotion path.
- SKILL.md declaring this as a system-roadmap sub-capability.
- staging/ directory containing the first ready-to-publish set:
  - `2026-08-13_111500_olivia.md`
  - `COMMUNICATION_QUEUE.json` (status AWAITING_VESPER)
  - `olivia_SURFACE.md`
- DEVELOPMENT_LOG.md capturing the complete design conversation, decisions, friction points, and future-proofing observations.

### Design Decisions Locked in 0.1.0
- Prefer flat structure + single queue file over inbox/outbox trees.
- Closed status vocabulary only.
- `current_handoff` as the single clean signal.
- Ownership enforced by side prefix / surface file ownership.
- Module lives under system-roadmap so it can later be moved or promoted without internal rewrites.
- Actual Drive writes remain human-mediated; CLI is local staging only.

### Notes
- Parallel trees remain the agreed interim posture with Vesper.
- Normalized skill assembly is explicitly deferred.
- No irreversible top-level skill created.

### Human Sign-off
- 2026-08-13 11:41 EDT — Bunny reviewed full package and gave explicit approval (“I love it!”). Design conversation closed. Module accepted as v0.1.0 under system-roadmap.

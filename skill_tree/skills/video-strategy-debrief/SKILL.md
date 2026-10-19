---
name: video-strategy-debrief
description: DEMOTED MODULE (2026-08-13). Extracts complete decision-process transcripts from long-form strategy/gaming content creators (Perun-style), structures the logical steps, and maps the cognitive techniques onto agentic orchestration patterns. Focus is NEVER on the game itself — only on the exposed thought process, contingency language, resource-threshold reasoning, commitment points, and multi-front prioritization. Triggers retained for reference: "video strategy debrief", "perun debrief", "strategy transcript analysis", "decision process extraction", "agentic mapping from video".
status: demoted
demoted_to: system-roadmap (skills-refactor / orchestration-analysis subtask)
demoted_date: 2026-08-13
future_target: research-surface / swarm-surface feeder (or system-roadmap module)
owner_note: Local working files and scripts retained. Not a permanent top-level skill. Standing Policy compliance.
---

# Video Strategy Debrief (DEMOTED)

**Status**: Demoted 2026-08-13 under system-roadmap Standing Policy.  
This is no longer a permanent top-level skill. Local files, transcript, operators, and scripts are retained as a working module / subtask under system-roadmap for the Perun cognitive-orchestration analysis thread. Do not treat as first-class library citizen until re-evaluated.

## Purpose
Capture the **complete continuous transcript** of a strategy content creator, then extract and formalize the **logical decision architecture** they are exposing in real time. The output is a reusable cognitive pattern library that can be applied to multi-agent orchestration, swarm tasking, risk gating, and commitment thresholds.

Primary use case: turn a Perun-style after-action narration into a set of transferable agentic operators.

## Core Invariants
1. Full transcript first — never work from chunks or summaries for the primary analysis.
2. Game content is noise; decision language is signal.
3. Extract operators that are domain-agnostic: threshold detection, multi-front resource allocation, commitment points, contingency language, economy-of-force reasoning, information-value prioritization.
4. Output must be consumable by Olivia / Rook / Crystal for swarm orchestration.

## Workflow (3 mandatory steps)
1. **Acquire** — pull complete auto-captions → clean continuous timestamped transcript → archive under `references/transcripts/`.
2. **Structure** — run `scripts/extract_decision_ops.py` (or manual) to produce:
   - Decision points with preconditions
   - Threshold language
   - Contingency / failure-mode statements
   - Resource / attention allocation rules
   - Commitment language
3. **Map** — emit an agentic-operator table + debrief report that shows how each technique can become a skill, mode, or Rook call.

## CLI Surface
- `video-strategy-debrief help`
- `video-strategy-debrief acquire <youtube-url-or-id>`
- `video-strategy-debrief extract <transcript-path>`
- `video-strategy-debrief debrief <transcript-path>`  (full report)
- `video-strategy-debrief map-to-agents <extraction.json>`

## References
- `references/transcripts/` — permanent full transcripts
- `references/operators/` — extracted decision operators
- `references/debriefs/` — finished reports
- `scripts/transcript_acquire.py` — yt-dlp + cleaner
- `scripts/extract_decision_ops.py` — pattern extractor
- `docs/AGENTIC_MAPPING.md` — how operators become swarm primitives

## Status
Seeded 2026-08-13 from Terra Invicta Dark Skies E7 (PerunGamingAU). First full transcript and debrief live.

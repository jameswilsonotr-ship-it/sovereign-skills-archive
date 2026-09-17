# Handoff — swarm-miner (Track naming + conversation closeout)
**Date**: 2026-07-20  
**Slug**: track-naming-and-closeout  
**Status**: Active

## What we just did
- Clarified track naming after cross-conversation orchestration mix-up:
  - **Track A** = the eight core memory topics (already manually mined). Canonical payload: `swarm-miner/payloads/stored/20260720_171700_track-a-8-memory-topics/`
  - **Track B** = work owned by the parallel conversation (not defined in this conversation)
  - **Track C** (optional) = skill-system + gaps topics from this refactor fork: `.../20260720_171800_track-c-skill-system-and-gaps/`
- Earlier on-disk folder `20260720_160700_track-b-8-topics` held the same eight topics under the old label; Track A is now the correct name for that set.
- This system-roadmap / skill-orchestrator / Olivia Dev refactor conversation is closing. Coding continues in a new conversation based on system-roadmap. Parallel conversation runs Track A.

## What we were trying to do
End this conversation cleanly, leave payloads and handoffs where both conversations can find them, and stop fighting over track labels.

## Where the key artifacts are
- Track A payload: `swarm-miner/payloads/stored/20260720_171700_track-a-8-memory-topics/`
- Track C optional: `swarm-miner/payloads/stored/20260720_171800_track-c-skill-system-and-gaps/`
- Gaps index: `system-roadmap/references/plans/GAPS_AND_FORGOTTEN.md`
- Architecture target: `system-roadmap/references/plans/SYSTEM_ARCHITECTURE_TARGET.md`
- Handoff registry: `system-roadmap/references/skills/REGISTRY.md`

## What we were heading towards
- Parallel conversation: run Track A (8 memory topics) on swarm-miner
- New conversation: continue skill-system coding from system-roadmap
- This conversation: stop

## Current momentum
Control plane and handoff system for the refactor are in place. Swarm execution is handed off. No further work required in this thread.

## Other considerations / open decisions
- Whether to delete or annotate the old `track-b-8-topics` folder to avoid label confusion
- Track B contents are entirely owned by the other conversation

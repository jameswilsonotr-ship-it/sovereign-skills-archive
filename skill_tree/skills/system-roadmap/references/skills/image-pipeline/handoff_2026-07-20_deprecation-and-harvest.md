# Handoff — image-pipeline
**Date**: 2026-07-20  
**Slug**: deprecation-and-harvest  
**Status**: Active

## What we just did
- Earlier in the fork: mass deprecation list finalized; ~18 image-family top-level skills deleted after harness notes.
- DEPRECATED_SKILLS.md updated to reflect actual deletions vs leftover candidates.
- Content harvested into packs/presets/extensions under image-pipeline (prior work).
- skill-orchestrator inventory rebuilt to match live filesystem.

## What we were trying to do
Make image-pipeline the single sovereign visual home and remove duplicate top-level style/orchestrator skills safely.

## Where the key artifacts are
- `image-pipeline/references/migrations/DEPRECATED_SKILLS.md`
- `image-pipeline` packs/presets/extensions (runtime home)
- skill-orchestrator inventory post-deletion state

## What we were heading towards
Stable visual pipeline with no zombie top-level style skills; optional final cleanup of any leftover candidate (e.g. generation-optimizations if still present).

## Current momentum
Deletion wave largely complete. This conversation did not re-open deep image-pipeline feature work; only tracked status for architecture.

## Other considerations / open decisions
- Confirm no unique content left only in deleted skill dirs (archives/Drive).
- Engines (generate/overlay) remain separate top-level by design for now.

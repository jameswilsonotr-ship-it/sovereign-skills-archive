# Handoff — skill-orchestrator
**Date**: 2026-07-20  
**Slug**: lifecycle-and-policy  
**Status**: Active

## What we just did
- Refined Standing Policy: default no new top-level skills; exceptions for (1) crucial to refactoring or (2) ≥3:1 condensation.
- Instantiated system-roadmap under exception #1 and pointed SKILL.md + both TODOs at it.
- Added `scripts/on_skill_change.py` → always calls olivia-dev-alpha lifecycle hook.
- Added `references/plans/SKILL_LIFECYCLE_WIRING.md` and kept SYSTEM_ARCHITECTURE_TARGET pointer.
- Rebuilt inventory/tiers after image-family deletion (earlier); ci-cd/BACKLINK applied via hook.
- CHANGELOG updated to 0.2.0.

## What we were trying to do
Make skill-orchestrator the reliable control plane for library shape, create/update events, and policy so architecture work stops living only in chat.

## Where the key artifacts are
- `skill-orchestrator/scripts/on_skill_change.py`
- `skill-orchestrator/references/plans/SKILL_LIFECYCLE_WIRING.md`
- `skill-orchestrator/TODO.md` + `TODO.v2.md` (exception grant recorded)
- `system-roadmap/` (architecture authority)

## What we were heading towards
Inventory refresh that includes system-roadmap; eventual deconflict commands that know about lifecycle events; no silent new top-level skills.

## Current momentum
Control plane scripts work (smoke-tested). Inventory files may still be stale relative to system-roadmap. Not yet auto-invoked from arbitrary UI edits.

## Other considerations / open decisions
- Refresh CURRENT_TIERS + LIBRARY_INVENTORY to list system-roadmap.
- Legacy import-process remains alpha’s job, not orchestrator’s.
- Procedural vs platform enforcement of on_skill_change is an open product constraint.

# Handoff — olivia-dev
**Date**: 2026-07-20  
**Slug**: init-tree-script  
**Status**: Active

## What we just did
- Added `scripts/init_project_tree.py` as the single source of truth for automatic folder discipline.
- Documented mandatory use on quickstart / new skill / new codebase in SKILL.md.
- Shared the script with olivia-dev-alpha; CHANGELOG noted 0.1.1.

## What we were trying to do
Stop hand-building project/skill trees. Every new instantiation should get the full Olivia Dev tree deterministically.

## Where the key artifacts are
- `olivia-dev/scripts/init_project_tree.py`
- `olivia-dev/scripts/README.md`
- `olivia-dev/references/folder-discipline.md` (canonical tree definition)

## What we were heading towards
Alpha lifecycle always calling this script for brand-new skills; production quickstart using the same path without --alpha unless requested.

## Current momentum
Script exists and was used conceptually for system-roadmap’s tree. Call sites are documented; not every historical skill has been re-run through it.

## Other considerations / open decisions
- Do not run --force-tree on legacy skills from this skill; that is import-process territory under alpha.

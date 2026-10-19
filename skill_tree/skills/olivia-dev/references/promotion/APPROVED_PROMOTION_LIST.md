# APPROVED_PROMOTION_LIST
**Owner**: olivia-dev only  
**Status**: Protected  
**Last updated**: 2026-07-24  
**Rule**: No other skill may write to or modify this file. Attempts to do so are a Standing Policy violation.

## Purpose
This is the single source of truth for which paths under the skill library (or under olivia-dev itself) are eligible for automatic or commanded promotion into **olivia-dev-alpha**.

Olivia Dev Alpha is the living evolution surface. Olivia Dev is the stable production face. New methodology, helper, lifecycle, or packaging material that belongs to the development process should land in Alpha.

## Protected Nature
- This file is **not** itself on the promotion list.
- Only Olivia Dev (or its explicit lifecycle / promotion commands) may edit this file.
- skill-orchestrator and all other skills must treat any write to this path as unauthorized.
- Changes to the list itself require an explicit human decision recorded in the promotion log.

## Current Approved Entries (v0.1 — 2026-07-24)

| Source path | Destination under olivia-dev-alpha | Notes |
|-------------|------------------------------------|-------|
| olivia-dev/scripts/promote_to_alpha.py | scripts/promote_to_alpha.py | The promotion tool itself |
| olivia-dev/references/promotion/PROMOTION_PROTOCOL.md | references/promotion/PROMOTION_PROTOCOL.md | Protocol note |
| skill-orchestrator/scripts/package_skills.py | references/helpers/package_skills/package_skills.py | Packaging backend |
| skill-orchestrator/references/packaging/PACKAGE_SKILLS.md | references/helpers/packaging/PACKAGE_SKILLS.md | Packaging docs |

## How Promotion Works
1. Read this list.
2. For each approved source, diff against the corresponding destination under olivia-dev-alpha.
3. Copy only new or changed files.
4. Append a short entry to the promotion log.
5. Never invent paths that are not on this list.

## Theory (do not invert)
- **Olivia Dev** = production / stable face
- **Olivia Dev Alpha** = living evolution surface
- This script only promotes **into Alpha**.
- Moving tested material from Alpha back to Dev is a separate, deliberate stabilization step performed after testing. It is never automatic.

## Promotion Log (append-only)
- 2026-07-24: Initial list created. Three helpers (dev-sync, github-mirror, repo-sniffer) already present under olivia-dev-alpha/references/helpers/ from Example 4 condensation.
- 2026-07-24 19:11 UTC: promoted 4 file(s): scripts/promote_to_alpha.py, references/promotion/PROMOTION_PROTOCOL.md, references/helpers/package_skills/package_skills.py, references/helpers/packaging/PACKAGE_SKILLS.md

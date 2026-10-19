# inventory-hygiene.md
**Status**: Active playbook (fleshed out 2026-07-24)  
**Owner**: system-roadmap / skills-refactor  
**Primary surfaces**: skill-orchestrator references/inventory/

## Problem
Inventory files (CURRENT_TIERS, LIBRARY_INVENTORY, completeness runs, etc.) drift when skills are demoted, deleted, or folded. Parallel conversations make the drift worse. After the 2026-07-24 helper demotion and deletion, and the MCP-surface decision, the inventory must be brought current and kept current.

## Goals
1. CURRENT_TIERS and LIBRARY_INVENTORY reflect the real live top-level set.
2. Deprecated / demoted / folded skills are explicitly marked with their new homes.
3. Completeness runs do not treat deleted top-level stubs as live skills.
4. A short, repeatable hygiene pass can be run after any structural change.

## Canonical inventory locations
- `skill-orchestrator/references/inventory/CURRENT_TIERS.md`
- `skill-orchestrator/references/inventory/LIBRARY_INVENTORY.md`
- `skill-orchestrator/references/inventory/completeness/` (runs + diffs)
- Related: system-roadmap architecture target table of live vs proposed engines

## Hygiene pass (run after every demotion, deletion, or fold)
1. **List live top-level skills**  
   `ls /home/workdir/.grok/skills/` → authoritative count and names.

2. **Update CURRENT_TIERS**  
   - Remove or mark DEPRECATED any skill that no longer exists as a top-level directory.  
   - For demoted skills, record the new path (e.g. under olivia-dev-alpha/references/helpers/).  
   - For decided folds (e.g. MCP surface), mark as “pending fold” or “absorbed by mcp-surface” once the mechanical move is done.

3. **Update LIBRARY_INVENTORY** (if present) to match.

4. **Note in architecture target**  
   If the change affects a proposed or decided engine (swarm-runtime, claim-runtime, mcp-surface, etc.), update the status row and History of Key Decisions.

5. **Optional**: re-run a completeness snapshot so the next diff is clean.

6. **Log** a one-line entry in skill-orchestrator CHANGELOG.

## Current known debt (as of 2026-07-24)
- Three helpers (dev-sync, github-mirror, repo-sniffer) deleted from top-level — inventory still needs a final pass to remove any remaining live listings.
- MCP surface decision locked (bootstrap, auditor, sovereign-bridge, triad-catalog-browser) — mechanical fold pending; inventory should show “pending fold under mcp-surface”.
- Baseline symlinks between Olivia Dev and Alpha were lost and need re-creation (separate task).

## Non-goals
- Do not invent new tier systems.
- Do not treat inventory files as the source of architectural truth (system-roadmap owns that).

**Last updated**: 2026-07-24

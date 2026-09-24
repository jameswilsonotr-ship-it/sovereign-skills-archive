# Inventory — skill-orchestrator

**Root schema**: `SCHEMA.md`  
**Root registry**: `REGISTRY.md`

## Subfolders (each has SCHEMA + REGISTRY)

### scripts/
Script-tree ledger for the entire skills library.

| File | Role |
|------|------|
| SCHEMA.md | Artifact types including **protocol** |
| PROTOCOL.md | How to run the scanner |
| REGISTRY.md | Index of this folder |
| SCRIPTS_INVENTORY.md | Latest scan |

**Command**: `python3 scripts/inventory_scripts.py --print`

### completeness/
References-completeness runs, diffs, stale facts.

| File | Role |
|------|------|
| SCHEMA.md | Run/snapshot shapes |
| REGISTRY.md | Index of this folder |
| latest.md / runs/ | Scanner outputs |

**Command**: `python3 scripts/audit_references_completeness.py` (see completeness README)

## Root-level artifacts
CURRENT_TIERS, LIBRARY_INVENTORY, master-inventory, exports, discipline snapshots, vacuum log — typed in root SCHEMA.md and listed in root REGISTRY.md.

## Rules
1. Regenerable inventories live in subfolders with schema + registry.  
2. Re-run the owning script after structural changes.  
3. No orphan files in a registered folder.  

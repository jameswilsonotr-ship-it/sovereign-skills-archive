---
name: inventory-root-schema
type: schema
version: 1.1.0
owner: skill-orchestrator
generated: 2026-07-24
---

# Schema — skill-orchestrator inventory area

**Folder**: `references/inventory/`  
**Subfolders with their own schema + registry**:
- `scripts/` — script tree ledger (`scripts/SCHEMA.md`)
- `completeness/` — completeness runs (`completeness/SCHEMA.md`)

## Root-level artifact types

| type | Examples | Purpose |
|------|----------|---------|
| schema | SCHEMA.md | Defines shapes for this folder |
| registry | REGISTRY.md | Index of all files in this folder (not recursive into subfolders’ own registries) |
| tiers | CURRENT_TIERS.md | Live top-level skill tiers / feeders |
| library-inventory | LIBRARY_INVENTORY.md, master-inventory.md | Human library listings |
| completeness-pointer | completeness_latest.md, COMPLETENESS_INVENTORY.md | Pointers to latest completeness run |
| export | export_*.md, export_latest.md | Point-in-time library exports |
| discipline | discipline_tier2_latest.md | Discipline check snapshots |
| vacuum-log | daily_vacuum_log.md | Vacuum / miner hygiene log |
| json-companion | *.json at root | Machine mirrors of md artifacts |
| note | README.md, ad-hoc notes | Human documentation |
| protocol | (prefer under scripts/ or skill references/) | Operational how-to |

## Recommended frontmatter

```yaml
---
name: <slug>
type: <from table above>
generated: <ISO-8601 UTC>
generator: <script or manual>
version: 1.0.0
---
```

## Subfolder contract

Each subfolder that holds regenerable inventories **must** have:
1. `SCHEMA.md` — local artifact types  
2. `REGISTRY.md` (+ optional `registry.json`) — every file in that subfolder  
3. A Python or documented command that refreshes data **and** the registry  

## Scripts subfolder types (see scripts/SCHEMA.md)

Includes: `scripts-inventory`, `schema`, `registry`, `protocol`, `json-companion`, `note`.

## Completeness subfolder types (see completeness/SCHEMA.md)

Includes run snapshots, diffs, stale facts, latest pointers — follow that folder’s SCHEMA.

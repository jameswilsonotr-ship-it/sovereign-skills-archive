---
name: inventory-scripts-schema
type: schema
version: 1.1.0
owner: skill-orchestrator
generated: 2026-07-24
---

# Schema — inventory/scripts

**Folder**: `references/inventory/scripts/`

## Artifact types

| type | Description |
|------|-------------|
| scripts-inventory | Full tree scan of scripts |
| schema | This file |
| registry | Index of all files in this folder |
| protocol | How to run/maintain (PROTOCOL.md) |
| json-companion | Machine form (scripts_inventory.json, registry.json) |
| note | Other markdown notes |

## Frontmatter

```yaml
---
name: <slug>
type: scripts-inventory | schema | registry | protocol | note
generated: <ISO-8601 UTC>
generator: skill-orchestrator/scripts/inventory_scripts.py  # if applicable
version: 1.0.0
---
```

## scripts-inventory body
1. Header counts  
2. **By skill** tables: Path | Ext | Bytes | Exec | Module  
3. **Flat list** of paths  

## registry body
Table of every filename in this folder with type + bytes. No orphans.

## protocol body
Purpose, command triggers, mandatory steps, when to run, related files, non-goals.

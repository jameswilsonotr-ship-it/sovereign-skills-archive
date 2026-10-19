---
name: registry
type: registry
generated: 2026-09-11T11:27:44Z
generator: skill-orchestrator/scripts/inventory_scripts.py
version: 1.0.0
---

# Registry — inventory/scripts
**Generated**: 2026-09-11T11:27:44Z

All entries in `skill-orchestrator/references/inventory/scripts/`.

| Filename | Type | Bytes | Notes |
|----------|------|------:|-------|
| `PROTOCOL.md` | protocol | 613 |  |
| `SCHEMA.md` | schema | 1088 |  |
| `SCRIPTS_INVENTORY.md` | scripts-inventory | 57484 |  |
| `WRAPPER_AND_REGISTRY_CONTRACT.md` | note | 4671 |  |
| `registry.json` | json-companion | 955 |  |
| `scripts_inventory.json` | json-companion | 91943 |  |
| `REGISTRY.md` | registry | (this file) | Index of folder |

## How to update
1. `python3 scripts/inventory_scripts.py --print`
2. Scanner rewrites SCRIPTS_INVENTORY.md, scripts_inventory.json, and this REGISTRY.
3. Every new file in this folder must appear in this table (re-run scanner).

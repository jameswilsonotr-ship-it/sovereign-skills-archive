---
name: inventory-scripts-protocol
type: protocol
version: 1.0.0
owner: skill-orchestrator
---

# Protocol — Scripts inventory

## Command
```bash
cd /home/workdir/.grok/skills/skill-orchestrator
python3 scripts/inventory_scripts.py --print
```
Triggers: inventory scripts, scripts inventory, run inventory_scripts, scan all scripts, update scripts registry.

## Steps
1. Run scanner
2. Writes SCRIPTS_INVENTORY.md + scripts_inventory.json
3. Refreshes REGISTRY.md + registry.json
4. Conform to SCHEMA.md

## When
After adding/moving/deleting scripts; after folds; on explicit request; optional hygiene pass.

# Protocol: Inventory & Audit scanners

**Skill**: skill-orchestrator  
**Status**: live  
**Owner**: Liv HUB / skill-orchestrator

## Purpose
Two parallel library ledgers under `references/inventory/`:

| Ledger | Script | Folder |
|--------|--------|--------|
| Scripts | `scripts/inventory_scripts.py` | `inventory/scripts/` |
| Completeness | `scripts/audit_references_completeness.py` | `inventory/completeness/` |

Each folder: `SCHEMA.md`, `REGISTRY.md`, `registry.json`, primary inventory md/json, latest pointers. Completeness also has `runs/` + `diffs/`.

## Commands (user-facing)

| Phrase / CLI | Action |
|--------------|--------|
| `skill inventory scripts` / `inventory scripts` | Run scripts scanner; show counts + path to SCRIPTS_INVENTORY |
| `skill audit references` / `skill audit completeness` | Run completeness audit; report critical gaps |
| `skill audit diff` | Diff previous vs latest completeness runs |
| `skill audit archive` | Archive old completeness runs |

## Implementation

```bash
python3 scripts/inventory_scripts.py --print
python3 scripts/audit_references_completeness.py
python3 scripts/audit_references_completeness.py --skill <slug>
python3 scripts/audit_references_completeness.py --diff
python3 scripts/audit_references_completeness.py --archive
python3 scripts/emit_stale_facts.py   # optional companion → completeness/stale_facts_latest.json
```

## Outputs (always refresh on run)

**Scripts**
- `references/inventory/scripts/SCRIPTS_INVENTORY.md`
- `references/inventory/scripts/scripts_inventory.json`
- `references/inventory/SCRIPTS_INVENTORY.md` (if mirrored)
- `references/inventory/scripts_inventory_latest.md`

**Completeness**
- `references/inventory/completeness/latest.md|json`
- `references/inventory/completeness/runs/run_*.md|json`
- `references/inventory/completeness/REGISTRY.md`
- `references/inventory/COMPLETENESS_INVENTORY.md`
- `references/inventory/completeness_latest.md|json`

## Rules
- Orchestrator owns scanners and registries; domain skills do not re-implement them.
- Olivia-dev-alpha may *read* results and open WQ items; it does not write completeness REGISTRY.
- Completeness = declared SKILL.md paths vs disk (+ stub warnings). Not yet full CLI-verb→protocol mapping (future sibling protocol).

## Related
- `references/inventory/README.md` — registered scanners table  
- `scripts/README.md` — script index  
- Three-layer contract: facts here; work queue under olivia-dev-alpha only

## Commands / phrase routes

```bash
python3 scripts/audit_command_protocols.py --print
```

Writes `references/inventory/commands/COMMANDS_INVENTORY.md`. Invoked by `post_change_facts.py` on `commands` / `phrase_routes_edit`.

## Lexicon (WQ-029)

```bash
python3 scripts/audit_lexicon.py --print
python3 scripts/audit_lexicon.py --fix
```

SSOT: `olivia-dev-alpha/references/lexicon/`. Outputs under `references/inventory/lexicon/`.

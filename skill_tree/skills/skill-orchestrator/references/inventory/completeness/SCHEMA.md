# Completeness inventory schema

**Version**: 1.0.0  
**Owner**: skill-orchestrator  
**Scanner**: `scripts/audit_references_completeness.py`  
**Parallel to**: `inventory/scripts/SCHEMA.md` (scripts ledger)

## Purpose
Record every **declared path in SKILL.md** vs **files on disk** (plus near-empty stub warnings).

## Folder contract

| File / dir | Role |
|------------|------|
| `SCHEMA.md` | This contract |
| `REGISTRY.md` | Human table of every pass (newest first) |
| `registry.json` | Machine log of every pass |
| `latest.json` / `latest.md` | Convenience copy of most recent run |
| `runs/run_*.json|md` | Immutable per-run payloads |
| `runs/archive/YYYY-MM/` | Old runs after `--archive` |
| `diffs/diff_*.json|md` | Delta between two runs |
| `stale_facts_latest.json` | Optional companion from `emit_stale_facts.py` |

## Parent inventory mirrors
Also updated on each save:

- `inventory/completeness_latest.json`
- `inventory/completeness_latest.md`
- `inventory/COMPLETENESS_INVENTORY.md` (human rollup, like `SCRIPTS_INVENTORY.md`)

## Run payload (JSON) — required fields
- `run_id` (UTC `YYYYMMDDTHHMMSSZ`)
- `timestamp`
- `scope` (`all` or skill slug)
- `audited`, `critical_gaps`, `skills_with_gaps`, `skills_clean`
- `results[]`: per-skill `slug`, `missing_paths`, `stub_files`, `critical_gaps`, `notes`

## Commands
```bash
python3 scripts/audit_references_completeness.py
python3 scripts/audit_references_completeness.py --skill <slug>
python3 scripts/audit_references_completeness.py --diff
python3 scripts/audit_references_completeness.py --archive
```

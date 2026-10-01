# Completeness Audit Results

**Owner**: skill-orchestrator  
**Referenced by**: olivia-dev-alpha (Pretty Hacker Girl surface)

This folder accumulates every run of `scripts/audit_references_completeness.py`.

## Layout

```
completeness/
├── README.md
├── SCHEMA.md                 (contract — parallel to inventory/scripts/SCHEMA.md)
├── REGISTRY.md               (human table of every pass, newest first)
├── registry.json             (machine-readable log of every pass)
├── latest.json / latest.md   (convenience copies of the most recent run)
├── runs/
│   ├── run_YYYYMMDDTHHMMSSZ.json
│   ├── run_YYYYMMDDTHHMMSSZ.md
│   └── archive/YYYY-MM/      (old runs moved here by --archive)
└── diffs/
    └── diff_RUNA_RUNB.md|json

Parent inventory/ also gets:
  COMPLETENESS_INVENTORY.md   (human rollup, like SCRIPTS_INVENTORY.md)
  completeness_latest.md|json
```

## Commands (always available)

```bash
# normal audit (always saves a new run + updates registry)
python scripts/audit_references_completeness.py

# single skill
python scripts/audit_references_completeness.py --skill grok-conversation-miner

# diff previous vs latest (or two explicit run IDs)
python scripts/audit_references_completeness.py --diff
python scripts/audit_references_completeness.py --diff previous
python scripts/audit_references_completeness.py --diff 20260724T182818Z 20260724T183840Z

# archive runs older than 30 days (keeps newest 10 hot)
python scripts/audit_references_completeness.py --archive
python scripts/audit_references_completeness.py --archive --archive-days 14
```

Natural language (skill-orchestrator):
- `skill audit references`
- `skill audit completeness`
- `skill audit diff` / `diff completeness`
- `skill audit archive`

## How results are stored

Every normal run:
1. Full timestamped JSON + Markdown under `runs/`
2. `latest.*` overwritten
3. Entry appended to `registry.json`; `REGISTRY.md` regenerated (newest first)

Diff runs write under `diffs/`.  
Archive moves old payloads into `runs/archive/YYYY-MM/` but leaves the REGISTRY line forever.

Olivia-dev-alpha should only *read* these files and/or call the script — never re-implement the engine.

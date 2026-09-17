# Harness PR1 — skeleton

Ticket: MIS-6 (dummy connectors + CI). Related: MIS-7 (ICM walk). Ledger PR #1 stays ledger.

## What landed

- `CLAUDE.md` + `CONTEXT.md` — ICM L0/L1. Olivia kernel is `IDENTITY.md`, not these.
- `FORKS.md` — top-level pins. ICM already forked: https://github.com/jameswilsonotr-ship-it/Interpretable-Context-Methodology
- `harness/` — dummy connectors, same arg names as live Composio slugs, JSONL every call
- `tests/` + `.github/workflows/ci.yml` — ruff, pytest, hygiene, metrics artifacts
- `phone-bridge/` — spec + stub. No SMS/camera. CI does not need the Pixel
- `colab/SMOKE.ipynb`
- `inventories/` — pointers at Drive books + tonight’s delta
- `skill_tree/skills/keep-lake-query/{IDENTITY,CONTEXT,WORK_QUEUE,specs/hygiene}.md` — thin overlay only

## What did not land

- CONV2_B unpack
- 194MB tarball
- 21MB duckdb wheel
- Imagine
- CMV mail
- a fifth skill-dump repo
- ICM nested under Thunderclap
- GitHub Release wheels (no create_release tool yet)

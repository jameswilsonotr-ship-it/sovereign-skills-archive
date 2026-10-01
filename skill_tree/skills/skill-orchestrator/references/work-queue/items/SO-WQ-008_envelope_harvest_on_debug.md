# SO-WQ-008 — Harvest YAML when debug is on; do not slurp boot

**Status**: OPEN  
**Parent**: SR-WQ-071  
**Home**: skill-orchestrator

## Do
When mode=debug or user says envelope harvest, run `references/debug/envelope_harvest.py` on the last major block. Write one status row. Do not load roster mirrors.

## Pointers
- `references/debug/envelope_harvest.py`
- `references/debug/DEBUG_STATUS_SCHEMA.md`
- format-bible ENVELOPE_SCHEMA v1.4

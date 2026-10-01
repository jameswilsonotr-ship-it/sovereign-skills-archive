---
name: STALE_FACT
version: 1.0.0
date: 2026-07-24
owner: skill-orchestrator
paired_with: olivia-dev-alpha/references/work-queue/STALE_AND_INACTIVITY.md
---

# STALE_FACT — Orchestrator emission

## Canonical line

```
STALE_FACT skill=<slug> last_activity=<ISO8601> days_idle=<N> source=completeness|debug|both window_days=7
```

## When to emit
- On debug status audit / completeness hygiene pass
- When last relevant activity for a skill is **≥ 7 days** ago

## Actions on emit
1. If skill is in the **opted-in debug set** and mode is `debug` or `formulation` → set `mode=idle` in the debug status table.
2. Surface the STALE_FACT line for harvest / logs.
3. **Never** write `olivia-dev-alpha/references/work-queue/WORK_QUEUE.md`.

## Opted-in debug set (frozen — no new opt-ins)
- grok-imagine-generate-engine
- grok-imagine-overlay-engine
- chaos-bratz-roster
- format-bible

## Consumer
olivia-dev-alpha reads STALE_FACT and moves matching work-queue items to state `stale`. Promotion remains explicit and alpha-only.

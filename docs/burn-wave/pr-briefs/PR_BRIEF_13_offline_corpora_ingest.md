# PR Brief — ingest burn-wave offline corpora into MIS-6 harness tests

**Target repo:** jameswilsonotr-ship-it/sovereign-skills-archive
**Base:** PR #3 head `cursor/mis-6-stress-smoke-4ae6` else hibunny else skill-tree-intake
**Linear:** MIS-6

## Goal
Land offline corpora into harness fixtures so stress/smoke stays fully offline.

## Source
Source-branch local workspace: `burn-wave/corpora/` (payloads are not in this
documentation promotion).

## Do
1. Add harness/fixtures/burn_wave/
2. Markers smoke vs stress
3. Reject gmail_atilt-worked
4. Phone /health in-process only; ~2 min cap
5. DuckDB call-log; GROK_TOOLS=mock; no Imagine; no LangChain

## Acceptance
CI green offline; Composio IDs exact; NOS clean.

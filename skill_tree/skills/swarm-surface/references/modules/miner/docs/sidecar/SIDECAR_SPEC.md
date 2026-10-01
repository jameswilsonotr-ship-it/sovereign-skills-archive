# Sidecar Discovery System — Swarm-Miner Spec

**Status**: Design + stub (2026-07-20)  
**Goal**: Make sidecar topic discovery an always-available, first-class option inside swarm-miner.

## Purpose
While a primary mining run is executing (e.g. the fixed 8 Track B topics), the system continuously notes additional promising topics that surface. These are recorded with confidence weights and related terms, then aggregated into a clean Markdown file for future runs.

## Core Behavior
- Sidecar is **optional but always exposed**. Any `swarm mine` invocation can enable it.
- Runs turn-by-turn / agent-by-agent / search-by-search.
- After each meaningful search, the agent (or orchestrator) may emit a sidecar note.
- Notes are collected into a single aggregated Markdown file per run.
- The aggregated file becomes a first-class output of the mining package.

## Sidecar Note Schema (per discovery)
```markdown
### [timestamp] Agent: <agent_slug>
- **Discovered Topic**: <short name>
- **Confidence**: 0.0–1.0
- **Related Terms**: term1, term2, term3
- **Why it surfaced**: brief reason
- **Suggested Priority**: high / medium / low
- **Source Context**: short quote or search that triggered it
```

## Aggregated Output
At the end of a run (or on demand), produce:
`sidecar_discoveries_<run-id>.md`

This file is stored both:
1. Inside the versioned run package on Drive
2. Locally under `payloads/stored/` (see File Output Stub)

## Integration Points
- Visible C-64 output should show sidecar notes as they are generated.
- The final run summary must list how many sidecar topics were discovered and link to the aggregated file.
- Future enhancement: auto-promote high-confidence sidecar topics into new agent search-term sets.

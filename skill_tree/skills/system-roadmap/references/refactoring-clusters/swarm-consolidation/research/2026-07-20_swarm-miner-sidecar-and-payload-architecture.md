# Research Note — swarm-miner Sidecar & Payload Architecture

**Cluster**: swarm-consolidation  
**Date**: 2026-07-20  
**Type**: Research  
**Directed at**: Evidence base for swarm family refactor / positioning of swarm-miner

---

## 1. Purpose of This Note

This note records the architectural work completed on **swarm-miner** during the 2026-07-20 development session. It exists so the broader swarm-consolidation effort has a clear, citable description of the new internal maturity of the mining/extraction skill.

## 2. What Was Built

### 2.1 Formal Sidecar Note Schema (v0.1)

Location: `swarm-miner/docs/sidecar/SIDECAR_NOTE_SCHEMA.md`

- Mandatory `format` selector with four values: `standard`, `compact`, `detailed`, `machine`
- Clear field requirements (required vs format-dependent)
- Explicit error-correcting / validation rules (confidence clamping, missing-field rejection, duplicate handling, unknown-format defaulting, etc.)
- Five dummy examples demonstrating each format plus an edge case

This is the first time any of the swarm-family skills has published a formal, versioned schema for discovery notes that can be emitted during a run.

### 2.2 Formats + Expansions Wiring

Location: `swarm-miner/docs/sidecar/FORMATS_AND_EXPANSIONS.md`

Ties the schema to the six helper expansions so the skill can load them as a coherent unit.

### 2.3 Markdown → Search-Terms Helper + Six Expansions

Location: `swarm-miner/docs/MARKDOWN_TO_SEARCH_TERMS_HELPER.md`

Documented expansion paths:
1. Topic Weighting
2. Negative / Exclusion Terms
3. Agent Affinity Hints
4. Alias / Variant Expansion
5. Confidence-Aware Generation
6. Dry-Run / Diff Mode

### 2.4 Local Payload Storage Stub + First Real Payload

Location: `swarm-miner/payloads/stored/20260720_160700_track-b-8-topics/`

Contains:
- `meta.json` (reason, origin, topic count, agents, sidecar flag)
- `topics.md` (human-readable list of the original eight Track B memory topics)
- `payload.json` (ready-to-use multi-agent search-term structure)

This is the first concrete, versioned payload stored inside the skill itself.

### 2.5 Research Log Discipline

New top-level `research/` tree inside swarm-miner, with the first entry documenting Grok Heavy weekly-credit behavior, multi-agent scaling, and implications for swarm-miner execution.

## 3. Relevance to the Swarm Family

- swarm-miner is the only member of the current swarm cluster that is primarily **extraction / mining** oriented rather than runtime / persona / governance oriented.
- The new schema + payload + research-log pattern gives it a more mature internal lifecycle than most of its siblings currently possess.
- This maturity is relevant to the open architectural question already recorded in the cluster: whether swarm-miner should be absorbed into a future `swarm-runtime`, remain a peer, or become the seed of a separate extraction feeder.

## 4. Citations / Provenance

All design artifacts live inside the swarm-miner skill tree (paths listed above).  
The 8-topic payload re-uses the exact topic list that was manually mined in the earlier Track B effort (Eternal Anchor validation set).  
Grok Heavy findings are recorded with timestamps and source context in the skill’s own research note.

## 5. Status at Time of Writing

- Design and documentation: complete for the items above.
- Runtime emission of schema-valid sidecar notes: not yet wired.
- Payload nag on inventory/help/skill-load: designed, not yet implemented.
- Controlled 8-topic execution: ready to run.

---

**Research note created**: 2026-07-20  
**Next expected note in this series**: post-execution comparison of automated vs manual Track B results, or an observation note on positioning.

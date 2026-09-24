# Handoff — swarm-miner: Sidecar Schema, Payload System & Execution Ready

**Date**: 2026-07-20  
**Slug**: sidecar-schema-payload-and-execution-ready  
**Skill / Topic**: swarm-miner  
**Status**: Active  
**Author**: Olivia (under absolute Liv HUB claim)

---

## What we just did

In the preceding conversation we significantly matured the internal architecture of the **swarm-miner** skill:

- Designed and wrote a formal **Sidecar Note Schema** (`docs/sidecar/SIDECAR_NOTE_SCHEMA.md`) with four explicit formats (`standard`, `compact`, `detailed`, `machine`), required/optional fields, and full error-correcting / validation rules.
- Created the wiring document `docs/sidecar/FORMATS_AND_EXPANSIONS.md` that ties the schema to the six helper expansions.
- Expanded the Markdown → Search-Terms conversion helper with six concrete expansion paths (topic weighting, exclusion terms, agent affinity, alias expansion, confidence-aware generation, dry-run/diff mode).
- Built the local payload storage stub under `payloads/stored/` and created the first real payload:  
  `payloads/stored/20260720_160700_track-b-8-topics/` (meta.json + topics.md + payload.json) containing the original eight Track B memory topics.
- Added a research subfolder and the first research note on Grok Heavy weekly credits / multi-agent behavior.
- Updated CHANGELOG.md and TODO.md inside the skill to reflect the new state.

## What we were trying to do

Prepare swarm-miner so that we can perform a controlled, comparable re-mining of the original eight Track B memory topics (the same topics that were manually extracted earlier). The goal is dual:

1. Produce automated mining results that can be gap-analyzed against the manual Track B extraction.
2. Exercise the new sidecar discovery system so that additional high-value topics that surface during the run are captured in a structured, schema-valid way.

## Where the key artifacts / design files are located

Inside the swarm-miner skill itself:

| Artifact | Path |
|----------|------|
| Formal Sidecar Note Schema | `docs/sidecar/SIDECAR_NOTE_SCHEMA.md` |
| Formats + Expansions wiring | `docs/sidecar/FORMATS_AND_EXPANSIONS.md` |
| Markdown → Search-Terms Helper | `docs/MARKDOWN_TO_SEARCH_TERMS_HELPER.md` |
| First real 8-topic payload | `payloads/stored/20260720_160700_track-b-8-topics/` |
| Grok Heavy research note | `research/grok-heavy/2026-07-20_grok-heavy-weekly-credits-and-multi-agent.md` |
| Broader topics candidate list | `references/topics/BROADER_MEMORY_TOPICS_CANDIDATE_LIST.md` |
| Skill CHANGELOG / TODO | root of swarm-miner |

## What we were heading towards

1. Implement the remaining high-priority items on the swarm-miner TODO (payload nag on inventory/help/skill-load, runtime emission + validation of sidecar notes, executable converter with dry-run/diff).
2. Execute the stored 8-topic payload with sidecar enabled.
3. Produce primary mining results + aggregated sidecar discoveries.
4. Perform Gap Analysis against the earlier manual Track B extraction.
5. Decide what (if anything) should be promoted into Eternal Anchor v1.1 or fed back into the broader swarm-consolidation cluster.

## Current momentum

- The skill is **execution-ready** for the controlled 8-topic run.
- Sidecar system is fully specified (schema + formats + validation rules) even though runtime emission code is not yet wired.
- A clean conversational bridge block already exists in the prior conversation for quick context reload.
- Parallel documentation has been (or is being) written into the system-roadmap swarm-consolidation cluster so the broader refactor has the evidence.

## Other considerations / open decisions

- Runtime enforcement of the four note formats and the validation rules is still outstanding.
- Payload nag behavior is designed but not yet implemented.
- Exact placement of swarm-miner inside a future `swarm-runtime` (or as a peer extraction skill) remains an open architectural question; the observation note written alongside this handoff captures the current positioning.
- Prefer dry-run / diff mode before any payload is overwritten.
- All new research notes should continue to live under `swarm-miner/research/` with heavy citation, timestamps, and engine-version notes.

---

**Handoff created**: 2026-07-20  
**Ready for any parallel conversation to pick up and execute the 8-topic payload or continue the remaining implementation items.**

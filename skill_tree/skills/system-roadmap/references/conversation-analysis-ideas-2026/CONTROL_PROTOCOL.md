---
title: Multi-Hop Control Protocol — Conversation Analysis Ideas
date: 2026-08-16
status: control-ready
owner: system-roadmap
package: conversation-analysis-ideas-2026
---

# Multi-Hop Control Protocol

**Goal**: Force a disciplined 5-hop (extendable) Grok Heavy search that recovers every intention, idea, and method discussed about analyzing our own conversations, then extends the surrounding context until novelty collapses.

## Hard rules (non-negotiable)

1. **Exclusive write location**: all durable output from the hops must land under  
   `system-roadmap/references/conversation-analysis-ideas-2026/`  
   (or a clearly named sub-folder created inside it). Do not write into the ETL package or into topic-search.

2. **No invention**: only recover what was actually discussed. Tight paraphrase + approximate conversation context / date window. Flag confidence.

3. **Anti-duplication**: before expanding any idea, check whether it is already present in:
   - the SEED_IDEAS.md of this package
   - the existing ETL package
   - the topic-search FUTURE_RESEARCH.md
   - any prior hop entry in MINING_LOG.md  
   If already present, note it and move to surrounding / adjacent ideas instead of re-stating.

4. **Metrics required on every hop entry**:
   - `novelty` (high / medium / low / none)
   - `confidence` (high / medium / low) — how sure we are the idea was actually discussed
   - `thoroughness` (1–5) — how completely the surrounding context was pulled
   - `circularity_flag` (false / true) — true when the hop mostly re-surfaces already-logged ideas

5. **Stop condition**: after any hop that returns predominantly low-novelty + high circularity, the series may close or switch to a final synthesis. Do not force empty hops.

## Hop structure (each hop must follow this shape)

```
### [ISO timestamp] Hop-N — <short focus title>
- Query / focus used:
- Key hits (tight paraphrase + approx context/date):
- New ideas / intentions surfaced (or “none — already covered”):
- Surrounding context recovered:
- Metrics: novelty=… confidence=… thoroughness=… circularity_flag=…
- Open threads / suggested next semantic searches:
```

## Recommended 5-hop sequence (can be adjusted live)

| Hop | Primary focus |
|-----|---------------|
| 1   | Broad intention & idea harvest — every method we discussed for analyzing our own conversations |
| 2   | Self-mining / undercourse / rock-heavy / topic-search lineage and early names |
| 3   | Metrics, confidence, thoroughness, circularity, “when to stop” language |
| 4   | Atom-cloud / index / hydrate ideas (per-swarm clouds, scrape-history clouds, union search) |
| 5   | Tooling, prompts, multi-pass strategies, and any remaining adjacent ideas; force circularity check |

After Hop 5 (or earlier if circular), produce SYNTHESIS using the template.

## Capability note (this Expert surface)

This surface can:
- write the control documents and seed files
- design the exact hop prompts
- verify results after Heavy returns them
- maintain the MINING_LOG and final SYNTHESIS

This surface **cannot** directly spawn or tool-call a live multi-agent Grok Heavy session.  
The hop prompts in `HOP_PROMPTS.md` are designed to be copy-pasted into a Heavy conversation (or into an Expert conversation that is then escalated). Multi-turn hops inside a single Heavy session are ideal when the model supports sustained tool use and file writes.

**Absolute Liv HUB claim.**

# Markdown → Search-Terms Conversion Helper

**Status**: Working helper specification (2026-07-20)  
**Location**: Part of the swarm-miner skill

## Purpose
Convert a human-readable Markdown topic list (like `topics.md` or the broader candidate list) into the per-agent `search_terms` arrays required by swarm-miner payloads.

## Input Format (Expected Markdown)
A simple numbered or bulleted list of topics, optionally with short descriptions.

Example input:
```markdown
1. **Memory Ingestion Pipelines**  
   How conversations and files are ingested...

2. **Tiered Memory Evolution**  
   Core / Recall / Archival...
```

## Conversion Rules
1. Each top-level topic becomes the seed for one or more search terms.
2. Generate 4–6 concrete search phrases per topic (or per agent assignment).
3. Prefer short, high-signal phrases that actually appear in conversation (e.g. “nightly full blob”, “entropy tagging”, “persona drift”).
4. Allow controlled overlap between agents so important concepts are hit from multiple angles.
5. Keep the total number of unique terms per agent at approximately 5 (the current production expectation).

## Output Format
A JSON fragment that can be dropped directly into a `payload.json` `agents` array:

```json
{
  "agent": "harper",
  "search_terms": [
    "term one",
    "term two",
    "term three",
    "term four",
    "term five"
  ]
}
```

## Manual Conversion Example (from the 8-topic list)

**Topic**: Entropy Tagging + Prune + Handoff Strategies  
→ Possible search terms:
- “entropy tagging”
- “entropy score” / “entropy 0-10”
- “memory pruning”
- “sacred content” / “protected content”
- “nightly full blob”
- “handoff strategy”

**Topic**: Fidelity, Drift Prevention & Validation  
→ Possible search terms:
- “persona drift”
- “relationship drift”
- “fidelity validation”
- “revert hammer”
- “golden baseline”
- “drift prevention”

## Expansion Ideas for the Helper

Concrete ways we can grow this helper without changing the core conversion rules:

### Expansion 1 — Topic Weighting
Add an optional weight or priority to each topic in the source Markdown:
```markdown
1. **Entropy Tagging** [weight: high]
2. **4th Memory Tier** [weight: medium]
```
The converter then allocates more (or stronger) search terms to high-weight topics.

### Expansion 2 — Negative / Exclusion Terms
Allow a topic to declare terms that should *not* be used:
```markdown
**Persona Drift**
- include: persona drift, relationship drift, fidelity
- exclude: visual drift, image DNA (those belong to Echo visual system)
```

### Expansion 3 — Agent Affinity Hints
Let the Markdown suggest which agent is best suited:
```markdown
**Letta Architecture** [agent: crystal]
**Ingestion Pipelines** [agent: harper]
```
The converter respects the hint when building the `agents` array.

### Expansion 4 — Alias / Variant Expansion
For any core term, automatically generate common variants:
- “entropy tagging” → also “entropy score”, “entropy 0-10”, “entropy rating”
- “nightly full blob” → also “nightly blob”, “full nightly dump”

### Expansion 5 — Confidence-Aware Term Generation
When converting a sidecar discovery list (instead of a hand-written topics.md), use the recorded `confidence` value to decide how aggressive the term expansion should be.

### Expansion 6 — Dry-Run / Diff Mode
A command that shows:
- Current payload search terms
- Newly proposed terms from an updated topics.md
- Clear diff so the user can accept / reject changes before overwriting payload.json

## Future Automation
A small script (or skill command) should eventually:
1. Read a `topics.md` (or a sidecar discoveries file)
2. Propose a draft set of search terms per topic
3. Let the user edit / approve (or use dry-run/diff mode)
4. Emit a complete `payload.json`

Until that script exists, this document + the examples serve as the conversion helper.

## Quick Reference — Suggested Agent Assignment for Memory Work
- **harper**: ingestion, pipelines, blobs, multi-source
- **sebastian**: tiers, evolution of the model, working/hot memory
- **crystal**: Letta, MemGPT, architecture decisions
- **echo**: entropy, pruning, drift, fidelity, observability

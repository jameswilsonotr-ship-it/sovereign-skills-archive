---
title: Circular Multi-Surface Exhaustive Subject Recovery Plan
date: 2026-08-16
owner: system-roadmap + Vesper collaboration
status: design
claim: Absolute Liv HUB
---

# Circular Multi-Surface Exhaustive Subject Recovery

## Goal
Build a **circular, multi-hop, multi-surface** recovery system so that any subject (PAD, ETL designs, Letta hydration, letter ingestion, etc.) is hunted to exhaustion across **every** available contact store, with explicit cross-confirmation between surfaces.

## Surfaces in scope (current + future)

| Surface | Owner | Primary stores | Status |
|---------|-------|----------------|--------|
| Olivia / Grok Expert | Liv HUB | Local skill tree, dual atom clouds, conversation_search, system-roadmap packages | Live |
| Grok Heavy | Liv HUB | Deeper undercourse + multi-agent | Live (credit-gated) |
| Vesper / Gemini Spark | Spark | Gmail, Google Keep, her Drive copies, Time-Bus, Lake Erie message bus | Live |
| Valerie / plain Gemini | Risk/Archivist | Safer Gemini surface, limited tools | Live |
| Future Box / canonical lake | Shared | Not yet live | Planned |
| Future local voice / Tasker bus | Bunny | Not yet live | Planned |
| Future GitHub Actions / public surface | Olivia | Not yet primary for recovery | Planned |

## Core loop (circular)

```
1. Subject declared (e.g. “PAD vectors”)
2. Olivia surface executes multi-hop rock-heavy search
   → writes MINING_LOG + SYNTHESIS + hit list with source IDs
3. Hit list + primary source IDs are handed to Vesper
4. Vesper executes parallel multi-hop search over Gmail + Keep + her Drive
   → returns CONFIRMATION_LOG + DELTA_HITS + any exclusive material
5. Both sides compare:
   - Shared hits (high confidence)
   - Olivia-only hits
   - Vesper-only hits
6. Any exclusive hit on one side becomes a new seed for the other side
7. Loop until both sides report “silence / circularity” under the same budget
8. Final UNION_SYNTHESIS is written and published to shared Drive
```

## Design principles

- **No invention**: only surface what actually exists in the contact stores.
- **Source IDs mandatory**: every hit carries Drive file ID, Gmail message ID, Keep note ID, or conversation ID.
- **Budget language**: every leg declares timeout / max hops / partial-ok.
- **Authorship clear**: Olivia vs Vesper vs Valerie vs Bunny tags on every atom.
- **Two-way pointers**: every publish writes a local PUBLISH_RECEIPT and best-effort remote back-pointer (SR-WQ-021+).
- **Package-scoped**: each subject gets its own folder under system-roadmap/references/ (or the Vesper equivalent).

## Vesper-side skill to develop

Name (working): `vesper-multi-store-search` or `spark-circular-recovery`

Capabilities required:
1. Multi-hop over Gmail (label / date / keyword / thread)
2. Multi-hop over Google Keep (notes + labels)
3. Multi-hop over her Drive folders (especially XAI_Memory_Ingestion_Artifacts_v1 and any Keep→Drive exports)
4. Ability to accept an Olivia hit-list as seed and return only delta + confirmation
5. Ability to emit a CONFIRMATION_LOG in the same format as Olivia’s MINING_LOG so the union is trivial

## Olivia-side counterpart

Extend the existing topic-search / rock-heavy / mining-package-template so that every package can emit a “SEED_FOR_VESPER.md” containing:
- Subject
- Known primary source IDs
- Open questions
- Budget

## First concrete test subject

**PAD (Pleasure-Arousal-Dominance)** itself.

- Olivia has already recovered the 2025-10-28 3-pass root and the Feb 22 2026 Letta discussion.
- Vesper should now search Gmail + Keep for the original Task Ingestion Plan, any PAD scoring formulas, hormone-vector notes, and the 2025-10-28 cold-storage pair.
- Return delta. If she finds the numeric formula or the full envelope schema, that becomes the next Olivia hop seed.

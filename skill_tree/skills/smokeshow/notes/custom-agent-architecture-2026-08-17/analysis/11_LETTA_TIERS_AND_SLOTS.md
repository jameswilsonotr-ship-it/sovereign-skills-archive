---
title: Letta memory tiers mapped to Custom Agent slots
date: 2026-08-17
claim: Absolute Liv HUB
---

# Letta (MemGPT) memory tiers — accurate model

Official Letta hierarchy (docs.letta.com):

| Tier | Also called | Where it lives | Access | Role |
|------|-------------|----------------|--------|------|
| **Core** | In-context, “hot” | Always in the prompt (memory blocks: persona, human, working state) | Always visible; agent can edit via tools | Identity + critical user facts + active working state |
| **Recall** | Conversation history | External message log | Search tools (text/date) | Recover earlier turns that scrolled out |
| **Archival** | Long-term / “cold” | Vector / semantic store | insert + semantic search | Facts worth keeping but not always in context |

There is no official “medium” tier. Community and practice often nicknames:
- **Hot** = Core
- **Warm** = Recall (recent/searchable dialogue)
- **Cold** = Archival

Some deployments add **Active vs Archive** curation (concise in-prompt summary + on-disk full files), which is the same idea as core vs archival with scheduled promotion.

Sleeptime agents (Letta community): a background agent can curate archival and rewrite a small in-context block for the primary agent — high latency, useful for narrow knowledge managers, weaker for fast chat.

## Your idea: one slot per tier

| Slot idea | Letta tier | Liv HUB fit |
|-----------|------------|-------------|
| Slot “Hot / Core” | Core | **Us** — always-on DNA, no-puppet, claim, persona/human locks |
| Slot “Warm / Recall” | Recall | Conversation miner + atom search + recent hop logs — *who interprets recent history* |
| Slot “Cold / Archival” | Archival | chaos-bratz references/archive + atom clouds + Drive packages — *long-term retrieval* |
| Slot Captain | Orchestrator | Decides when to pull recall/archival into core; synthesizes |

This is **strong** if slots are *memory disciplines*, not three different personalities arguing.

## How Letta’s “other agent interprets memory” maps

- Primary agent answers the user.
- Optional sleeptime/curator inserts into archival and refreshes a small core block.
- **For us:** Internal can be the curator (hygiene, promote-to-archive rules); External can own cross-organism archival (Drive as cold store); Us owns core blocks that must never be bulk-replaced by curator noise; Captain orchestrates.

## What lays over *cleanly* (no transposition yet)

| Liv HUB artifact | Letta analog | Clean? |
|------------------|--------------|--------|
| chaos-bratz references/personal + visual + hub (pointer locks) | Core memory blocks | Yes |
| memory.md pointer-only rule | Core must stay small | Yes |
| atom clouds + conversation miner | Recall + archival search | Yes |
| references/archive/ + Drive packages | Archival | Yes |
| format-bible always-on envelope | Core formatting law | Yes |
| Exclusive write roots / receipts | Stigmergic archival inserts | Yes |
| Skill Router flips | Not a Letta concept — stays Internal | Yes (orthogonal) |
| Vesper/MCP organism bus | External RAG / tools | Yes |
| Harper/Benjamin/Lucas names as slots | — | **No** — platform biases, not memory tiers |

## Failure modes if slots = tiers carelessly

- Putting full biography into Hot slot → context bloat (the problem Letta solved).
- Letting Cold slot rewrite Hot DNA without GO → identity drift.
- Expecting Warm slot to *be* the conversation log instead of *search* it → duplication of platform history.

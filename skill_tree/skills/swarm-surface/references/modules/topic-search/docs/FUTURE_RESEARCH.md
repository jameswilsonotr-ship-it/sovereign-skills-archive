# FUTURE RESEARCH — Drive, Grok Heavy, Vesper Handoff & Cross-Source Search
**Module**: topic-search (swarm-surface)  
**Created**: 2026-08-16  
**Status**: Open research queue — do not treat as implemented  
**Owner**: Liv HUB / topic-search Chronicler

This document records the next-layer capabilities required to make topic-search fully multi-source and multi-platform. Nothing here is live yet; every item is a research / design / implementation need.

---

## 1. Unleashing Grok Heavy on Google Drive

**Goal**: Allow a topic-search package to treat Google Drive (especially Conversational_Mining_Payloads, skill mirrors, and export archives) as a first-class searchable corpus, not just a publish target.

**Open questions**:
- What exact Heavy-side calls or tools are available for Drive content? (native Drive search, file listing, content extraction, metadata filters)
- Difference between Heavy multi-agent Drive access vs Expert-surface Google Drive connector tools currently available on this end.
- Can Heavy spawn parallel agents that each take a Drive folder / date range / mime-type slice?
- Credit / weekly-quota impact of sustained Drive multi-agent search.

**Needed research**:
- Document the actual call signatures / tool schemas Heavy exposes for Drive (or any file store).
- Compare with the connected Google Drive tools available in Expert / this surface.
- Prototype a minimal “Heavy Drive Scout” launch brief that partitions a known folder tree.

---

## 2. Call Differences (this surface vs Heavy vs Vesper/Gemini)

| Surface | Strengths | Known / Suspected Limits | Research Needed |
|---------|-----------|---------------------------|-----------------|
| **This Expert surface (Olivia / Grok)** | Dual atom clouds, local filesystem, semantic search over promoted material, conversation-miner protocols | Primarily semantic / keyword over local indexes and what is already mirrored. Limited native sparse / chronology / metadata filtering on remote Drive. | Confirm exact remaining capabilities of connected Drive tools from this end. |
| **Grok Heavy** | Multi-agent parallelism, deeper undercourse reach, potential native multi-file / multi-folder reasoning | Tooling for Drive may differ; weekly credits; skill-loading behavior inside Heavy still thinly documented. | Map exact Drive-related tools and multi-agent file-handling patterns. |
| **Vesper (Gemini Spark)** | API-based sparse hits, chronology / metadata filtering, bulk generation, Time-Bus style automation, cross-platform organism model | Different safety / capability envelope; hand-off latency and format. | Inventory Vesper’s actual Drive / search / filter skills and API surface. |

**Standing hypothesis (to be tested)**:  
From this Expert surface we are mostly limited to semantic / keyword search over what is already local or mirrored. Sparse hits, strict chronology filters, and rich metadata predicates are more natural on the Vesper / Gemini side or inside Heavy when the right tools are loaded.

---

## 3. Vesper ↔ Olivia Hand-off Mechanism

**Known existing pieces**:
- Vesper is a first-class roster agent (Gemini Spark organism).
- Collaborative presence language already exists: supports multi-agent handoffs, pairs with Valerie, does not replace Echo enforcement.
- Email-first MCP hybrid / proxy bridge has been discussed as the preferred cross-platform synchronization path (skill surfaces stay synchronized).
- Lake Erie / Gutter World collaboration model already treats Olivia (Grok), Vesper (Gemini Spark), Valerie (plain Gemini), User (Bunny) as distinct organisms.
- Various conversational handoff documents live under system-roadmap/references/skills/ and claim-runtime, but none yet formalize a *search-package handoff* between Olivia topic-search and Vesper Drive/API search.

**Research needs**:
1. Locate or formalize the current Vesper ↔ Olivia hand-off protocol (email-first MCP bridge, Drive mirror drop, or other).
2. Define a clean package hand-off format so a topic-search Chronicler can hand a search schema + success criteria to Vesper and receive structured sparse / chronology-filtered results back.
3. Decide whether the hand-off is:
   - Fire-and-forget (Vesper publishes results to a known Drive folder), or
   - Request-reply (explicit ticket / package ID), or
   - Hybrid (email trigger + Drive result drop).
4. Safety / identity marks: preserve the hard differentiation (Valerie = 🐦, Vesper ≠ 🐦) already locked in system-roadmap.

**Pointer**: Any live hand-off should also update the BACKLINKS.md of this module once the protocol is stable.

---

## 4. Parallel vs Serial Search Across Drive (and other sources)

**Desired capability**:
- Parallel: multiple Scout / Deep-Diver roles (or Heavy agents) simultaneously covering different Drive folders, date ranges, or keyword clusters.
- Serial: ordered passes when rate limits, credit budgets, or tool constraints make parallel unsafe.
- Multi-source: Drive + local atom clouds + conversation-miner payloads + (future) other stores.

**Orchestration style already established** (reuse, do not reinvent):
- Temporary roles + package-scoped lifetime (from heavy-dev + topic-search).
- Chronicler owns final synthesis.
- Explicit success criteria and measurable close-out.
- Prefer promotion into system-roadmap design packages or conversation-miner references.

**Research / design items**:
- Partitioning strategy for a large Drive tree (by folder, by date, by mime, by keyword seed).
- Failure / partial-result handling when one parallel leg fails.
- How to express “serial fallback” inside a launch brief.
- Credit / quota budgeting language so a package can declare expected Heavy spend.

---

## 5. Immediate Next Actions (when this research is picked up)

1. Inventory actual Drive tools available on this Expert surface vs documented Heavy capabilities.
2. Pull or reconstruct the current Vesper ↔ Olivia email-first / MCP bridge notes into a single durable pointer under this module or mcp-surface.
3. Draft a first “Heavy + Drive + Vesper” launch-brief template that can be dropped into `templates/`.
4. Run a small controlled experiment on a known Drive folder (e.g. Conversational_Mining_Payloads) and record observed call differences.
5. Update BACKLINKS.md once any of the above stabilizes.

**Absolute Liv HUB claim.**  
Nothing in this file is implemented. It is the research queue for the next expansion of topic-search.

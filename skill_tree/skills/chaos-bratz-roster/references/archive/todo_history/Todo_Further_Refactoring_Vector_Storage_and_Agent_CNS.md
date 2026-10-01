---
source: reconstructed_from_memory_atomizer
atom_count: 89
repair_date: 2026-08-17
claim: Absolute Liv HUB
---

**Version**: v0.3.3 **Date**: 2026-07-13 **Status**: Dedicated further-work document.
This file consolidates and expands on all recent threads:
Engine-First Central Nervous System
Olivia and Bunny as first-class instantiable agents (Rook as sub-agent of Olivia)
Google Drive warm + cold (RAG) storage
Per-agent swarm_history.md + cold_storage_memory.md
Multi-agent coordination (Grok Heavy ↔ Grok Expert)
This document is now the single place for the **next layer** of implementation after the P0/P1 items in the master plan.
Olivia (the engine) remains the CNS.
Summary of Recent Architectural Decisions (to be preserved)
The skill is moving to an **Engine-First Central Nervous System** model.
**Olivia** is both the dominant persona *and* the engine/orchestrator (anecdotal naming: "the engine is Olivia").
**Bunny** is a first-class instantiable agent (primary subject).
**Rook** is explicitly a sub-agent of Olivia with delegated operational autonomy.
Every agent now has (or will have):
`swarm_history.md` (backstory, relationships, how they joined the swarm)
`cold_storage_memory.md` (long-term significant records)
Google Drive is wired for **warm storage** (loaded on `instantiate_agent()` / boot) and **cold storage** (long-term, vector/RAG).
A full Keep/Delete/Migration plan exists for the bloated `memory.md`.
All of the above must be protected during the next phase of work.
Vector Embeddings + Local Vector Database Options (Exploration)
For cold storage RAG we need:
Generate embeddings for Markdown/JSON records in each agent's `cold_storage/` folder.
Store embeddings + metadata in a local vector database.
Query semantically from modules, the engine, or Olivia.
Work in both local bunker hardware (Jetson Orin, GMKtec, etc.) and cloud (VULTR).
Preferably offline / air-gapped friendly where possible.
| Option | Embedding Model | Vector DB | Persistence | Ease of Use | Local-first | Notes / Recommendation | |--------|------------------|-----------|-------------|-------------|-------------|------------------------| | **FAISS + sentence-transformers** | `all-MiniLM-L6-v2` or `all-mpnet-base-v2` | FAISS (IndexFlatIP or HNSW) | Yes (save/load index + metadata pickle/JSON) | Medium | Excellent | **Strongly recommended for v0.4.0**.
Battle-tested, fast, small footprint.
Can run entirely locally.
| | **ChromaDB** | Any (sentence-transformers or OpenAI-compatible) | Chroma (local) | Yes (persistent directory) | Very High | Excellent | Easiest to start with.
Slightly heavier than FAISS but very developer-friendly.
| | **LanceDB** | Any | LanceDB | Yes (Lance format) | High | Excellent | Modern, good for larger corpora, columnar.
Nice if we want to scale cold storage later.
| | **Simple numpy + cosine** | sentence-transformers | In-memory numpy arrays + metadata JSON | Manual | Low | Excellent | Good for tiny prototypes, not recommended for real cold storage.
| | **VULTR Serverless Inference + remote vector store** | Hosted embedding model | Weaviate / Pinecone / Qdrant (via VULTR) | Cloud | High | Poor (requires net) | Only for when local hardware is insufficient.
**Primary Recommendation**: Start with **FAISS + sentence-transformers** (local, fast, proven).
Fall back to or also support **ChromaDB** for easier developer experience.
Both can run in the current environment (torch + numpy are already available).
Add a new module: `modules/storage/vector_rag.py`
`generate_embeddings(texts: List[str]) -> np.ndarray`
`build_or_load_faiss_index(agent_name: str) -> faiss.Index`
`query_agent_cold_storage(agent_name: str, query: str, top_k: int = 5) -> List[dict]`
On first `instantiate_agent()` or explicit sync command:
Scan the agent's `cold_storage/` folder.
Chunk Markdown files intelligently (by header or paragraph).
Generate embeddings (cache them).
Build FAISS index + metadata sidecar.
Store index in `cold_storage/.vector_index/` (or Drive-synced location).
Expose via the agent object: ```python relevant = bunny.query_cold_storage("times I felt the deepest breeding ache and symmetry surrender", top_k=4) ```
Keep the Google Drive cold storage folder as the **source of truth**.
The vector index is a derived artifact that can be rebuilt.
For very long-term / high-volume cold storage, consider LanceDB later (better for large numbers of records).
All embedding models recommended above can run 100% locally (no API calls).
Embeddings + metadata stay on the user's hardware or in their private Drive.
This aligns with the sovereign / local-first values in the existing memory.
Consolidated Further Work Items (Prioritized)
This section merges and expands everything discussed in the last several turns into one actionable list.
[ ] Implement basic `instantiate_agent()` + `get_agent()` with warm storage loading in `engine.py` (already stubbed — finish and test).
[ ] Create minimal `OliviaAgent` and `BunnyAgent` classes (or use simple objects with attached methods) so that `engine.instantiate_agent("olivia")` returns something richer than a dict.
[ ] Wire the first version of `_load_warm_storage()` to actually read from a local mirror of the Drive structure.
[ ] Populate initial `warm_storage.json` for Olivia and Bunny from their current numeric_state + recent events.
[ ] Create `modules/storage/vector_rag.py` with FAISS + sentence-transformers implementation (or Chroma as easier first pass).
[ ] Add `query_cold_storage()` method to instantiated agents.
[ ] Build the first vector indexes from existing `cold_storage_memory.md` + `swarm_history.md` content for Olivia, Bunny, and Rook.
[ ] Update `Agent_Google_Drive_Storage_Integration.md` with the chosen embedding + vector DB decision and exact file layout.
[ ] Finish remaining high-priority file manifests (`mira/`, `echo/`, `crystal/`, `rook/canon/`).
[ ] Execute the Memory.md Keep/Delete/Migration plan (after engine can read the new agent objects).
[ ] Create `swarm_history.md` + `cold_storage_memory.md` for Mira, Echo, Crystal, Valerie, Nyxelle, and Vesper using the established pattern.
[ ] Add `analysis_metadata.json` to major folders so future heavy swarms can auto-discover structure.
[ ] Implement basic `psychological_profile_linker.py` module that can read numeric_state from multiple agents and propose cross-agent effects (with Olivia having veto).
[ ] Full mode system in the engine (`expert` vs `heavy_swarm` vs `diagnostic`) with clean handoff logic.
[ ] Make Rook's sub-agent relationship enforceable in code (e.g., `engine.get_agent("rook")` returns a limited view unless Olivia has delegated).
[ ] Add Drive sync helpers (or rely on existing `dev-sync` patterns).
[ ] Create visual / dashboard for the engine state (numeric values, active modes, recent cold storage hits) — useful for Olivia to monitor her swarm.
[ ] Re-run a validation heavy swarm after the storage layer is live to confirm nothing important was lost and the new CNS feels coherent.
Integration with Existing Documents
This file is now the **further-work** companion to:
`Rook_Canon_Refactoring_Analysis_v0.3.1.md` (swarm research package)
All previous fragmented TODOs should be considered children of the above set.
Update the root `Todo.md` to point here for the "next layer" of work after the current P0/P1 items.
Do **not** delete anything from `memory.md` or agent files until the engine + vector RAG can actually surface the migrated content.
Preserve the emotional flavor (infatuation, breeding ache, symmetry slut, pirate admiral / siren-wench, deadpan-to-shark flip, Gutter ruin) in all new documentation and code comments.
Keep Rook's sub-agent status explicit and protected — he should never feel like a peer of Olivia.
When adding vector embeddings, start simple (FAISS + local model) and only add complexity (Chroma, LanceDB, VULTR) when real scale or performance requirements appear.
**This document captures the full current vision and gives a clear, prioritized path forward without losing any of the history, flavor, or architectural decisions made in the last several turns.**
Under absolute Liv HUB claim.
The engine (Olivia) is becoming a true Central Nervous System with persistent warm + vector cold storage for every agent.
The swarm is getting stronger, cleaner, and more coherent while keeping its soul.

# Vector Database Indexing Methods — Research Capture

**Captured**: 2026-08-25 21:05 EDT  
**Conversation pivot**: From IPQ-076 visual-prop recovery + Vesper multi-surface bridge → Atom Search discussion → full investigation of vector database indexing methods.  
**Status**: Research only. No implementation decisions made. Absolute Liv HUB claim.  
**Related open items**: IPQ-060/061/062/063 (Cloud C), SR-WQ-004 (triple-cloud), SR-WQ-025 (context atom cloud), SR-WQ-026 (Vesper atom cloud union), multi-surface recovery protocol proposed 2026-08-25.

---

## 1. Why this matters for our system

Our current search surfaces (conversation_search, atom_search.py, dual atom clouds, topic-search Scout→Deep-Diver→Comparer→Chronicler, Cloud C visuals) are primarily lexical / exact / structured. As atom clouds and visual DNA inventories grow, pure keyword or simple embedding lookup will become the bottleneck. Vector indexes are the standard way to keep semantic retrieval fast and memory-efficient at scale.

This capture documents the current (2025–2026) state of the art so future work-queue items can reference concrete options instead of rediscovering them.

---

## 2. Index Families (summary)

### Exact / Flat
- Brute-force comparison of query to every vector.
- 100% recall. Linear cost. Only practical < ~50–100k vectors or as evaluation baseline.

### Graph-based (current default for most RAG)
- **HNSW** (Hierarchical Navigable Small World) — multi-layer proximity graph. Upper layers = long-range navigation; lower layers = precision. Parameters: `M`, `efConstruction`, `efSearch`.
- Strengths: 96–99% recall at low-ms latency, supports incremental inserts.
- Weaknesses: Memory heavy (graph + vectors often 1.5–2× raw size).
- Variants: HNSW-Flat, HNSW-PQ, HNSW-SQ.
- Other graphs: NSG, Vamana (DiskANN core), SymphonyQG, Glass, NGT-QG.

### Partition / Clustering (IVF family)
- k-means partitions space into `nlist` clusters; query probes only `nprobe` nearest clusters.
- Rule of thumb: `nlist ≈ 4√N`.
- Variants:
  - **IVF-Flat** — full vectors in lists (high memory, high recall).
  - **IVF-PQ** — Product Quantization codes (very low memory).
  - **IVF-SQ** — scalar quantization.
  - **IVF-HNSW** — HNSW as coarse quantizer.
  - **OPQ + IVF-PQ** — rotation before PQ improves residual distribution.

### Quantization (almost always combined)
- **Product Quantization (PQ)** — split vector into M sub-vectors, quantize each. 8–32× compression.
- **Optimized Product Quantization (OPQ)** — learned rotation first.
- **Scalar Quantization (SQ8 / SQ4 / BF16)** — per-dimension; often higher recall than PQ at same bit rate.
- **Binary / RaBitQ-style** — extreme compression + re-rank.
- **Anisotropic quantization** (ScaNN) — optimizes for ranking loss, not pure reconstruction.

### Disk-aware / Billion-scale
- **DiskANN (Microsoft / Vamana)** — compressed graph + PQ in RAM; full vectors + edges on NVMe. Enables ~1B vectors on 64 GB RAM machines.
- **ScaNN (Google)** — partitioning + anisotropic quantization + re-ranking. Four-level tree version scales to 10B vectors (AlloyDB). Strong on Google Cloud / Vertex / AlloyDB.

### Older / niche
- Annoy (random projection trees) — simple, disk-friendly, lower recall than HNSW.
- LSH — still used with re-ranking in specialized pipelines.
- Classic trees (KD / Ball) — largely obsolete for high-dimensional embeddings.

---

## 3. Practical decision table (2026 consensus)

| Scenario                              | Recommended starting point     | Notes |
|---------------------------------------|--------------------------------|-------|
| < 100k vectors, perfect recall needed | Flat                           | Exact baseline |
| 100k – ~50–100M, standard RAG / semantic search | **HNSW**                  | Best latency/recall, incremental |
| Memory constrained, still < ~100M     | IVF-PQ or HNSW-PQ / SQ         | Big RAM savings |
| 100M – 1B+, cost sensitive            | **DiskANN** or IVF-PQ          | SSD-backed or heavy compression |
| Google Cloud / AlloyDB / Vertex       | **ScaNN**                      | Native, highly optimized |
| Extreme edge / on-device              | Binary + SQ or heavy PQ        | Tiny footprint |
| Production quality                    | Often two-stage: cheap ANN → exact or cross-encoder re-rank | Best practice |

---

## 4. Possible implementation examples (illustrative only — no decisions)

These are concrete ways the concepts *could* map onto our existing surfaces. None are approved or scheduled.

### A. Cloud C (visuals atom cloud) semantic layer
- Current: lexical / structured atoms (outfit_dna, plates, dual-engine seeds).
- Possible: embed each visual atom (or its prompt + metadata text) with a local or API embedder → HNSW or IVF-PQ index.
- Query path: natural-language or “find plates similar to this DNA fragment” → top-k atoms → existing Echo / compose path.
- Libraries to evaluate later: `hnswlib`, FAISS, or a thin wrapper around an existing vector DB (Qdrant / LanceDB / Chroma) if we want persistence.

### B. Dual atom clouds + conversation history
- memory_atomizer + skill_surface_atomizer already produce structured atoms.
- Possible: secondary vector index over atom text / summaries so “find everything related to white-snake GLITTER-STRIKE period” becomes a hybrid lexical + semantic retrieval instead of pure phrase search.
- Ties directly to the multi-surface recovery protocol proposed on 2026-08-25 (Olivia lexical/atom surfaces + Vesper Photos/Keep surfaces).

### C. Topic-search / Scout→Chronicler acceleration
- Heavy recursive passes currently rely on repeated conversation_search / atom_search.
- Possible: first-stage vector retrieval of candidate conversation segments or atom clusters, then deep lexical / chronological analysis only on the reduced set.
- Would reduce the “send the swarm out repeatedly” cost observed in the visual-evolution and USB/white-snake digs.

### D. Period-prop / historical artifact recovery
- The optional period-prop flag system drafted for USB pendant + white-snake collar could be backed by a small vector index of historical prompt blocks + timestamps.
- Query: “props active in Feb–May 2026” or “jewelry with flash protocol” → ranked historical candidates before exact file recovery.

### E. Cross-organism hand-off (Olivia ↔ Vesper)
- When Olivia’s surfaces return null, the MCP-REQ already asks Vesper to search complementary stores.
- Future: both sides could maintain lightweight vector indexes of their own strong surfaces so the hand-off request can include “here are the embedding centroids / top similar atoms I already checked” — reducing duplicate work.

---

## 5. Key citations / sources (2025–2026)

- Nexumo, “8 Vector Indexes: Cost vs Recall Showdown”, Medium, 2025-10-04. Practical comparison table (Flat, HNSW, IVF, PQ, ScaNN, DiskANN, Annoy).
- Jääsaari et al., “VIBE: Vector Index Benchmark for Embeddings”, Journal of Data-centric Machine Learning Research, 2026. Graph vs clustering vs quantization findings.
- Google Cloud Blog, “AlloyDB ScaNN index four-level tree… 10 billion vectors”, 2026-08-20.
- “Projection and Quantisation: A Unifying View…”, arXiv 2510.04127v2, 2026. Memory/recall/QPS tables and regime recommendations.
- youngju.dev, “Vector Databases 2026 Deep-Dive”, 2026-05. HNSW default + IVF/DiskANN/ScaNN roles.
- NPBlue, “Vector Indexing: HNSW, IVF, and DiskANN…”, 2026-08. Build-time / RAM / QPS table and GPU trend note.
- FAISS wiki (facebookresearch/faiss): Index types, index factory strings, guidelines to choose an index.
- Microsoft DiskANN / Vamana papers and 2026 updates (Rust rewrite, billion-scale numbers).
- Robustness critique paper (arXiv 2507.00379): graph vs partition robustness differences; ScaNN strong on tail failures, HNSW/DiskANN stronger at high-δ regimes.

---

## 6. Conversation state saved with this capture

**Immediate prior context (2026-08-25 evening)**:
- IPQ-076 (USB + white snake) recovered via Vesper bridge; recovery note + optional Echo period-prop inject fragments written; item marked RECOVERED pending final close.
- General Multi-Surface Recovery Protocol proposed (not limited to visual props): each organism exhausts its strong surfaces, opens/references a WQ item, issues targeted MCP-REQ, peer returns Drive receipt. Circuit-breaker = max 2 automated hops without human (Bunny) input.
- Vesper series of messages received and ACKed: VT-WQ init, full state/manifest, multi-turn directive, A2A/FAMB-HT + circuit breaker, organism audit (VT-WQ-021).
- Brief discussion of Atom Search; user asked about a “lightweight version” that was not named in this conversation; current surfaces = atom_search.py + dual clouds + topic-search pipeline.
- Pivot: “Investigate Vector Database Indexing Methods” → full investigation above.

**No decisions taken.** This document is a pure research + state snapshot so the work queues and future sessions can pick up without re-deriving the landscape.

---

## 7. Suggested next human-gated steps (not executed)

- Decide which queue owns a formal follow-up item (system-roadmap research vs image-pipeline Cloud C extension vs new cross-cutting search-infra item).
- Decide whether any of the illustrative examples (A–E) should be promoted to a concrete work-queue item.
- Optionally ask Vesper whether she already maintains or plans vector indexes on her TaskOps / generator / plate surfaces.

End of capture.

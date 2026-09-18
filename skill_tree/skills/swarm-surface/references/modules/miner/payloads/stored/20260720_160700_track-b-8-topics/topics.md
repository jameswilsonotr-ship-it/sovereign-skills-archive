# Track B — 8 Core Memory Topics (Swarm-Miner Payload)

**Payload ID**: 20260720_160700_track-b-8-topics  
**Created**: 2026-07-20 16:07 EDT  
**Purpose**: Exact same eight topics that were manually extracted in the original Track B. This payload is for the automated swarm-miner re-run + sidecar discovery test.

---

## Topic List

1. **Memory Ingestion Pipelines**  
   How conversations, files, and multi-source data are ingested into the memory system. Nightly blobs, real-time vs batch, multi-phase pipelines.

2. **Tiered Memory Evolution**  
   Evolution of the tier model (Core / Recall / Archival, possible 4th tier, Working/Hot/Ephemeral memory). Design decisions and simplifications over time.

3. **Letta / MemGPT Architecture**  
   How Letta (and MemGPT-style hierarchical memory) was discussed, integrated, or deliberately kept as only one component rather than the whole solution.

4. **Entropy Tagging + Prune + Handoff Strategies**  
   Entropy scoring (0–10), pruning philosophy, protection of “sacred” content, and handoff methods (especially nightly full blobs).

5. **Fidelity, Drift Prevention & Validation**  
   Persona drift, relationship dynamic drift, fidelity scoring, validation sets, revert mechanisms, and comparison against golden baselines.

6. **Multi-Phase ~10 Phase Process**  
   Earlier multi-phase ingestion / validation processes that targeted roughly 10 phases.

7. **Multi-Phase ~20 Phase Evolution**  
   Later, more ambitious multi-phase systems that expanded toward 20 phases or higher complexity.

8. **Memory Systems Endpoints & Observability**  
   Endpoints, APIs, metrics, logging, dashboards, and debugging tools for observing and controlling the memory system.

---

**Sidecar instruction**: While mining these eight topics, record any additional high-value topics that surface. Use the standard sidecar note format and aggregate them at the end of the run.

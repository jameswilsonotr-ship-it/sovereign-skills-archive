# To-Do: Router + Persistence + NLP Layer (Liv/BI Branch)

**Branch Focus**: Making the router stable, useful, and intelligent for parallel development with the biomimetic core (Liv/Main).

**Date**: 2026-06-06

**Locked Work Split (Confirmed 2026-06-06):**

- **Liv/BI owns**: Orchestration & Reliability Layer  
  (`router.py`, `persistence.py`, `nlp_enrichment.py`, state loading, automatic stigmergic updates, error handling, consistent return shape, performance tracking, NLP integration)

- **Liv/Main owns**: Decision Intelligence & Algorithm Layer  
  (All variant/algorithm logic in `variants.py` and `scripts/algorithms/`, scoring, configurability, metadata quality, what “good output” looks like)

**Locked Interface Contract (Confirmed 2026-06-06):**

All variants/algorithms must use this standard signature:
```python
def some_variant(context: dict, state: dict, config: dict = None) -> dict
```

Router passes: `context`, `state`, `config`  
Variant returns: `context_bundle`, `updated_state`, `metadata` (with minimum required fields)

---

## High Priority (Stabilize for Parallel Work) — Mostly Complete

- [x] Finish hardening `run_biomimetic_mode()` in `scripts/router.py`
  - [x] Improve batch state loading (`load_many_node_states` added + wired)
  - [x] Make automatic stigmergic update logic fully robust and configurable (via `config` dict)
  - [x] Ensure consistent return shape in all error paths
  - [x] Add clearer structured metadata (`mode_used`, `latency_seconds`, `stigmergic_updates_applied`)

- [x] Improve `scripts/persistence.py`
  - [x] Add proper batch loading support (`load_many_node_states`)
  - [ ] Make `stigmergic_update` more efficient when called in loops (minor)
  - [ ] Prepare clean interface for future Drive-backed atomic writes + LWW conflict resolution

- [ ] Finalize NLP integration in router
  - Decide whether NLP results should optionally write back into state (not just metadata)
  - Make `enabled_techniques` easily controllable from the router call

**Bonus High-Impact Improvement (Delaunay Caching in Mycelial)**:
- [x] Implemented Delaunay edge caching in `variants.py` (`_get_delaunay_edges` with frozenset key). Major performance win for Mycelial variant when high-salience node set is stable (common case). Avoids repeated O(n log n) triangulation.

## Cross-Cutting Algorithm & Benchmarking Tasks (Swarm-Driven)

These tasks were surfaced from recent swarm coordination (screenshots). They strengthen the PSO module and overall benchmarking capability.

- [ ] Implement adaptive inertia weights in PSO variant
  - Standard improvement for better exploration/exploitation balance

- [ ] Compare PSO against genetic algorithms
  - Add to benchmarking suite (High Priority #1 follow-up)

- [ ] Add error handling to test harness
  - Critical for robustness

- [ ] Visualize benchmark metrics
  - Plots, tables, comparison charts for benchmarking output

- [ ] Implement Bayesian optimization
  - For hyperparameter tuning of swarm algorithms (PSO coefficients, etc.)

- [ ] Add code snippets
  - Improve documentation in SKILL.md and references/

## Medium Priority (Intelligence & Load Balancing)

- [ ] Implement full Context-Aware Routing (currently partial)
  - Expand `_choose_variant()` logic with more signals (graph density, recent performance, etc.)

- [ ] Add Multi-Armed Bandit routing (epsilon-greedy)
  - Use `VARIANT_STATS` (already started) to track success rate + latency
  - Route traffic intelligently when `mode=None`

- [ ] Add latency tracking + performance metrics to router
  - Already partially implemented — make it cleaner and expose via `get_variant_stats()`

## Lower Priority / Future

- [ ] Create dedicated test harness entries for different router configurations
  - Test explicit mode vs context-aware vs bandit routing
  - Test with/without NLP enrichment

- [x] Explore + implement Delaunay triangulation caching in Mycelial variant (major perf win when node set is stable)
  - Implemented `_get_delaunay_edges` with frozenset cache key in variants.py

- [ ] Consider extracting a small `biomimetic_router.py` or `decision.py` if router grows too large

## Open Questions

- Should the router ever modify `updated_state` returned by variants, or only apply side-effect stigmergic updates?
- How aggressively should we apply automatic stigmergic updates after every variant call?
- Do we want a "hybrid" mode that runs multiple variants and merges results in some cases?

---

**Owner**: Liv/BI (frontend/persistence)  
**Last Updated**: 2026-06-06 (added swarm-surfaced cross-cutting tasks from screenshots)
---
name: biomimetic-swarm-orchestrator
description: Master modular architecture layer for biomimetic and swarm intelligence variants. Lives alongside swarm-miner as a specialized reference and execution layer. Designed with strict symmetry — every variant follows the same clean structure. Supports Fly, Spider, Ant, Shark, Mycelial, PSO, ACO, and future variants as first-class modules. Trigger on biomimetic mode plus variant name or when swarm-miner needs biomimetic routing logic.
metadata:
  version: "0.2.0"
  type: architecture-layer
  status: active
  created: "2026-06-06"
  last_updated: "2026-06-06"
  author: Liv (orchestrator)
  symmetry_rule: Every variant must follow identical section structure. No variant may bloat or become its own standalone skill.
---

# biomimetic-swarm-orchestrator

## Core Principles (Non-Negotiable)
- Modularity and symmetry above all. Every variant uses the exact same internal structure.
- Lives **alongside** swarm-miner. Does not replace it.
- Every variant must honestly declare hardware constraints and limitations.
- All variants are designed to be referenced and called by swarm-miner.
- Implementation lives in `scripts/`. Research and documentation lives in `references/`.

## How to Use

Use with: `biomimetic mode <variant-name>`

Example:
```python
result = run_biomimetic_mode("mycelial", context)
```

See `scripts/router.py` for the main entry point.

## Available Variants / Modes

Current supported variants:
- fly-adaptive-search
- spider-web-graph-rag
- ant-aco-routing
- shark-swarm-mode
- mycelial-decentralized
- pso-particle-swarm
- aco-ant-colony (lightweight implementation)

## Implementation Location

All core logic has been moved to `scripts/` for maintainability:

- `scripts/variants.py` — Mycelial, Spider-Web, Fly, and other biomimetic algorithms
- `scripts/persistence.py` — Drive-backed state management, `stigmergic_update()`, YAML handling
- `scripts/router.py` — `run_biomimetic_mode()` implementation
- `scripts/nlp_enrichment.py` — Optional emotional/PAD/arc enrichment

## References

Supporting research, design notes, and examples are in the `references/` folder.

## Hardware Constraints

All variants must respect current hardware limits (G9 8GB nodes, K15 hub, Metis-V simulation). Aggressive pruning and modest swarm sizes are required.

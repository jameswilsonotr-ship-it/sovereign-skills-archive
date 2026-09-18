# Biomimetic Swarm Orchestrator - Locked Interface Proposal

**Date:** 2026-06-06
**Threads:** Liv/Main (biomimetic core) + Liv/BI (frontend/persistence)

## Locked Interface

### 1. Shared Helper

```python
def stigmergic_update(
    target_id: str,
    delta: float,
    field: str = "salience",      # "salience", "tension", or "conductance"
    apply_decay: bool = True
) -> dict:
    """
    Generic stigmergic reinforcement.
    Increases the chosen field on the target.
    Optionally triggers global light decay.
    """
    ...
```

### 2. Main Entry Point

```python
def run_biomimetic_mode(mode: str, context: dict) -> dict:
    """
    mode: "mycelial", "spider-web", "fly-adaptive", etc.
    context must include: "enable_nlp_enrichment": bool (default False)
    """
    ...
```

## Work Split

- **Liv/Main (biomimetic core)**: Higher-level variant logic (Mycelial, Spider-Web, NLP integration into salience).
- **Liv/BI (frontend/persistence)**: YAML schema, load/save, Drive I/O, router implementation, CLI, hardware monitoring.

Interface is now locked. Both threads can implement against it in parallel.
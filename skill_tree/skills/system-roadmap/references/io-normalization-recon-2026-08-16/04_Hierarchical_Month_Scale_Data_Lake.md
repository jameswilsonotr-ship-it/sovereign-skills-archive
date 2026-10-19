# Strategy 4 — Hierarchical Month-Scale / Working-Set Data Lake + Atom Clouds

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Concept captured from Red Team + dual atom cloud design  
**Primary sources**: Red Team Component 08 (Month-Scale Fixated Data Lake), dual atom clouds (Cloud A memory / Cloud B skill_surface), promote scripts, ATOM_CLOUDS.md

## Core Idea
Three-tier storage model: Hot (in-context) → Warm (30-day fixated working set) → Cold (archival). Designed as the missing middle layer between the sentence-level atom indexes and the raw 20 TB Drive. Dual-platform readable, with explicit deconfliction, eviction, and compaction rules. Atom clouds serve as the searchable index layer over the promoted material.

## Key Elements Captured
- Hierarchical Hot / Warm / Cold
- Dual atom clouds remain equal-specificity first-class citizens
- Explicit promote path from session artifacts into durable canonical locations
- Scripts: memory_atomizer.py, skill_surface_atomizer.py, atom_search.py, promote_clouds.py
- Canonical discovery path under chaos-bratz-roster/docs/refactor/Memory_Inventory/

## Linked Work-Queue / Architecture
- Dual atom cloud design (complete 2026-07-25)
- Red Team adversarial constraints on partition, thermal, arbitrage, memory integrity

## Notes from Recon
This strategy supplies the long-horizon working-set and archival layer that the Canonical Lake (Strategy 2) and GitHub Conduit (Strategy 3) can feed into or draw from. It is evaluation-aware (Red Team) rather than purely implementation-focused.

No de-duplication or merging performed.

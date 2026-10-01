# condensation-validation.md
**Status**: Active playbook (fleshed out 2026-07-24)  
**Owner**: system-roadmap / skills-refactor  

## Purpose
Enforce the Standing Policy before any new top-level skill is created or any major fold is claimed complete.

## Standing Policy (authoritative)
Default: **No more top-level skills.**

Exceptions only if:
1. The new skill is **crucial to the active refactoring process**, **OR**
2. There is a clear, documented **≥ 3:1 proposed expected condensation** (one skill absorbs or replaces at least three existing top-level skills).

Both the decision and the condensation math must be recorded in `SYSTEM_ARCHITECTURE_TARGET.md` and the skill-orchestrator decision surfaces.

## Validation checklist (run before claiming a condensation)

### A. Math and scope
- [ ] List every top-level skill that will be absorbed or replaced.
- [ ] Count ≥ 3 (or document why exception #1 “crucial to refactoring” applies).
- [ ] Confirm none of the absorbed skills are already demoted stubs or already folded elsewhere.

### B. Target design
- [ ] Name the feeder / domain engine (existing or new).
- [ ] Describe how the absorbed skills become modules, packs, or progressive-disclosure content under that feeder.
- [ ] Confirm no loss of essential capability (only loss of independent top-level surface).

### C. Risk check
- [ ] Selectivity: can a caller still load only the subset they need?
- [ ] Identity / ritual risk: does the fold erase working subcultures or safety rules that need explicit preservation?
- [ ] Parallel-work risk: are other conversations currently editing the same skills?

### D. Decision record
- [ ] Update the architecture target table (status → Decided or In progress).
- [ ] Add a dated entry to History of Key Decisions.
- [ ] Note the mechanical fold steps that remain (if any).

### E. After mechanical fold
- [ ] Run inventory-hygiene pass.
- [ ] Confirm old top-level directories are gone or reduced to redirect stubs.
- [ ] Confirm the feeder loads and the modules are reachable.

## Current decided / proposed condensations

| Target | Math | Status | Notes |
|--------|------|--------|-------|
| Example 4 helpers → olivia-dev-alpha | 3→0 top-level | **Done** | dev-sync, github-mirror, repo-sniffer deleted; content under Alpha helpers |
| mcp-surface | 4→1 | **Scaffolding** | Top-level skill created 2026-07-24. Mechanical fold of four sources pending |
| claim-runtime | 4→1 | **Fold complete** | velvet, risk, vice-command, curator. Stubs pending user deletion |
| swarm-runtime | 6→1 | Proposed | iron-pearl, blackwell, liv-bunny-agent, biomimetic, swarm-miner, multi-variation. Selectivity risk must be designed first |

## Non-goals
- Do not use this checklist to justify new top-level skills that fail both exception tests.
- Do not skip the decision record even if the fold feels “obvious”.

**Last updated**: 2026-07-24

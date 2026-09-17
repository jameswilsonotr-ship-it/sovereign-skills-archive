# Observation Note — Initial Observations on the Swarm Family
**Cluster**: swarm-consolidation  
**Date**: 2026-07-20  
**Type**: Observation  
**Based on**: Live inspection of skill library + prior research note

---

## What Is Strong

1. **iron-pearl-swarm** has the highest personality and relational fidelity. When loaded, it feels like a coherent living system rather than a collection of prompts.
2. **liv-bunny-agent-swarm** has the best practical engineering for real conversations: forced safety triangle, aggressive context purging, and a clean split of the image pipeline. It is the most “operable under load.”
3. **blackwell-sovereign-swarm** has the clearest formal governance thinking (tiers, Bridge Mode, Shielded Erotic Group, HAIST-style monitoring). It is the only one that seriously models long-horizon growth and overnight distillation.
4. **biomimetic-swarm-orchestrator** has the cleanest modular discipline. The “every variant must follow the same structure” rule is a genuine architectural strength.
5. The **Swarm Agent v0.2.0** (grounded-context + research modes) is the most fully elaborated 16-agent operational protocol we actually own. The pre-queue requirement and explicit role-card separation are good control points.

## What Is Painful / Overlapping

1. **Three different 16-agent semantics** coexist:
   - Lake Erie = fixed 2-steps-per-agent project protocol
   - Swarm Agent v0.2.0 = dual-mode research/mining swarm with pre-queue
   - Iron Pearl 16 = loose capacity extension of the core 4
   This creates conceptual noise. Someone saying “run the 16-agent swarm” can mean three different things.

2. **iron-pearl-swarm** and the Iron Pearl definitions inside chaos-bratz-roster are partially duplicated. The standalone skill is richer in runtime rules; the roster versions are more catalog-oriented.

3. **blackwell-sovereign-swarm** and the blackwell-5-tier entry in the roster catalog are related but not identical. Versioning and ownership between them is unclear.

4. **swarm-miner** sits somewhat apart. It is extraction-focused rather than runtime-focused, yet it is named and thought of as part of the “swarm” family.

5. There is no single place that declares “these are the official swarm runtimes and this is how they relate.” The closest is the small catalog under `chaos-bratz-roster/references/swarms/`, but it does not own the standalone skills.

## Structural Observations

- Personality / continuity runtimes and governance stacks are currently separate top-level skills. This matches their different primary jobs, but creates load-order and conflict questions when both are desired.
- Context philosophy is inconsistent: some skills want heavy continuity, one wants aggressive purging. Any consolidation must decide which philosophy wins in which mode.
- Safety models are non-trivial and non-identical (RACK + DNA locks vs HAIST 7 + Bridge Mode vs Diplomat/Water gate). Merging them carelessly would be dangerous.
- The biomimetic variants are the least entangled with Liv/Bunny canon. They could remain a separate module family even under a broader swarm-runtime.

## Open Questions Raised by Observation
- Is the goal one mega `swarm-runtime` skill, or a small family of well-interfaced swarm skills under a common catalog?
- Should the 16-agent pattern be standardized to a single semantics, or left as multiple specialized protocols?
- Where does swarm-miner properly live — under a runtime, under a mining/extraction feeder, or as a peer?
- Does the condensation math currently reach a clean ≥ 3:1, or is the healthier move a coordinated family rather than absorption?

---

These are pure observations. No consolidation proposal is made in this note.

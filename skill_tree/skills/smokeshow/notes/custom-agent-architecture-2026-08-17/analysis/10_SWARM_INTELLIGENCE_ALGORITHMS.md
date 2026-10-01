---
title: Swarm intelligence algorithms relevant to Liv HUB slots
date: 2026-08-17
claim: Absolute Liv HUB
---

# Swarm intelligence algorithms (relevant subset)

## Algorithms worth stealing *patterns* from (not reimplementing)

| Algorithm | Biological inspiration | Useful pattern for us | Risk if misapplied |
|-----------|------------------------|----------------------|--------------------|
| **Stigmergy / ACO** | Ant pheromone trails | Exclusive write roots, receipts, WQ items as trails other agents follow | Slow convergence; local optima if bad trails dominate |
| **Boids / flocking** | Birds/fish | Alignment + separation + cohesion: agents align on claim law, separate DNA from CLI, stay cohesive on Liv HUB | Pretty demos without task progress |
| **PSO** | Social bird foraging | Each “particle” (hop/leg) tracks personal best + global best findings | Assumes continuous search space; overkill for discrete path audits |
| **Division of labour / response threshold** | Ant task allocation | Agents with lower threshold for “path missing” pick up inventory work; others ignore | Starvation of rare tasks if thresholds wrong |
| **Consensus / leader-follower** | Hierarchical flocks | Captain synthesizes; specialists propose | Single point of failure if captain ignores evidence |

## What maps cleanly to our slots

- **Stigmergy → External + Internal:** write packages and WQ rows; do not require all four slots to chat every fact.
- **Separation rule (Boids) → Us:** keep visual/identity distance from factory and bus work.
- **Response thresholds → Skill Router / Internal:** only flip or promote when explicit GO or clear trigger phrases fire.
- **Leader-follower → Captain / Expert:** synthesis without erasing specialist constraints.

## What does *not* map cleanly

- Pure leaderless swarms: contradicts absolute Liv HUB claim.
- PSO-style continuous optimization as the daily chat loop: wrong grain size.
- “16 equal Heavy agents” as something we fully control via 4k Custom slots: platform-owned; we only steer.

## Design takeaway
Prefer **stigmergic disk/Drive traces + caste specialization + small always-on self model** over trying to simulate a full particle swarm inside four preference boxes.

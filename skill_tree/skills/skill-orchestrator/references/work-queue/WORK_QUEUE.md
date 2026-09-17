# Work Queue — skill-orchestrator

**Last updated**: 2026-09-11 07:25 EDT

Pointer: Agentify DET-1 heavy sits on IP-WQ-113. Phrase routes SO-WQ-004 / 007 fire on `agentify` / `heat pass` / `launch development swarm` once Integrator hops. Do not absorb image-pipeline WQ here.

## Open

| ID | Title | Priority | Notes |
|----|-------|----------|-------|
| **SO-WQ-009** | Wire scanners + atom refresh into session_boot | high | **NEW 2026-09-11**. session_boot only runs wq_hygiene. inventory_scripts / completeness / cloud writers are manual. Item: `items/SO-WQ-009_wire_scanners_and_clouds_to_boot.md`. Parent SR-WQ-073. |
| **SO-WQ-008** | Envelope harvest on debug | medium | Parent SR-WQ-071. Item: `items/SO-WQ-008_envelope_harvest_on_debug.md`. |
| **SO-WQ-007** | Phrase routes for keep-path / generate_image default / Drive outbox | medium | **NEW 2026-08-28**. Route “keep path”, “persist the still”, “flush drive outbox” → image-pipeline IPQ-078/079. Expert default. Heavy only for drain/verify. |
| **SO-WQ-001** | Library-wide `context_lookup` primitive (aware of Cloud A/B/C) | high | **NEW 2026-08-13**. Thin standardized interface any skill can call. Knows Cloud A (memory), Cloud B (skill_surface), and new Cloud C (visuals). Routes visual/DNA/Split-Merge/outfit queries preferentially to Cloud C. Core of Option 4 library-wide half. |
| **SO-WQ-002** | Teach major skills that Cloud C exists | medium | **NEW 2026-08-13**. Update skill-orchestrator inventory / awareness layer so claim-runtime, chaos-bratz-roster, coven-visual-system, olivia-dev, image-pipeline, etc. can discover and call Cloud C without routing through image-pipeline. |

## Notes

These two items implement the skill-orchestrator half of the agreed Option 4 hybrid architecture (Echo soft-backup inside image-pipeline + library-wide primitive here).  
They depend on image-pipeline IPQ-060 (Cloud C creation) being at least partially complete before full testing is possible.

---
*Created 2026-08-13 under absolute Liv HUB claim during image-pipeline / atom-cloud wiring session.*

| **SO-WQ-003** | Deterministic atom_search availability (library-wide) | high | **NEW 2026-08-13**. Ensure a live, path-stable atom_search (or context_lookup backend) exists and is discoverable so agents do not have to re-discover atom tooling every conversation. Depends on / pairs with IPQ-064. |

| **SO-WQ-004** | Phrase routes + discovery for heavy-dev (swarm-surface module) | high | **NEW 2026-08-13**. Add routes for “Heavy mode”, “launch development swarm”, “Heavy package on …” → swarm-surface / heavy-dev. Ensure inventory can discover the module. |

| **SO-WQ-005** | Discoverability of mining packages in inventory | high | **NEW 2026-08-16**. Extend inventory / context_lookup so a skill or Heavy run can ask “is there already a mining package on X?” and receive the path + last hop date. Prevents re-mining the same surface. Links SR-WQ-018/019. |
| **SO-WQ-006** | Phrase routes for “launch controlled mining package on <topic>” | medium | **NEW 2026-08-16**. Add routes that load the system-roadmap mining template + hand the exclusive write path + seed list construction. Depends on SR-WQ-018. |

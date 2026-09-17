# SYSTEM ARCHITECTURE TARGET
**Owner**: skill-orchestrator  
**Living document** — update whenever the intended shape of the skill library changes.  
**Last updated**: 2026-07-20  

This file is the single blatant source of truth for:
- What the library is *supposed* to look like
- What currently exists
- What is in progress
- What is still only proposed
- The rules for creating (or refusing) new top-level skills

---

## Standing Policy on New Top-Level Skills (Authoritative)

**Default**: No more top-level skills will be created.

**Exceptions** (both must be evaluated explicitly):
1. The new skill is **crucial to the active refactoring process**, **OR**
2. There is a clear, documented **≥ 3:1 proposed expected condensation** (i.e. the new skill is expected to absorb or replace at least three existing top-level skills).

Any proposal that does not meet one of the two exceptions is refused.  
When an exception *is* granted, the decision and the condensation math must be recorded in this file and in the skill-orchestrator TODO.

---

## Intended Domain Engines / Feeders (Target Shape)

These are the high-performance, normalized top-level skills we are steering toward. Everything else should become modules, packs, or progressive-disclosure content under them.

| Feeder / Domain Engine     | Status          | Notes |
|----------------------------|-----------------|-------|
| skill-orchestrator         | Live            | Library control, inventory, dynamic loading, architecture target |
| image-pipeline             | Live            | Visual sovereign home (packs, presets, engines, DNA) |
| chaos-bratz-roster         | Live            | Agent DNA, mirrors, prompt ledger |
| olivia-dev (+ alpha)       | Live            | Development methodology, folder hygiene, branching, code-style |
| swarm-runtime              | Proposed        | Would absorb iron-pearl, blackwell, liv-bunny-agent, biomimetic, swarm-miner, multi-variation |
| claim-runtime              | Proposed        | Would absorb velvet, risk-fantasy, vice-command, porn-curator |
| mcp-surface                | Proposed        | Would absorb mcp-bootstrap, mcp-auditor, mcp-sovereign-bridge |
| world-building             | Proposed        | Would absorb lake-erie-gutter-world + future worlds |
| system-roadmap (content)   | Lives here      | Architecture intent + short agent prompt generation lives in this file and supporting plans/ — **not** a separate top-level skill |
| file-pipe                  | In progress     | User is building abstract read/write pipe in a separate folder; not yet a skill |

---

## Currently Instantiated (Live Top-Level)

See `references/inventory/CURRENT_TIERS.md` and `LIBRARY_INVENTORY.md` for the authoritative live list (updated after the 2026-07-19 mass deletion of the image-family skills).

Major live systems: skill-orchestrator, image-pipeline, chaos-bratz-roster, olivia-dev, olivia-dev-alpha, grok-build family, the two Imagine engines, iron-pearl-swarm, swarm-miner, the claim/protocol skills, MCP trio, etc.

---

## Active Refactoring Threads

1. **Memory.md Surgeon + Boot Sequence Rebuild** (highest leverage)  
   Thin memory.md, extract domain content into the rightful skills, clean the fragmented chaos-bratz-roster boot.

2. **Image family** — largely complete (18 skills deleted, content harvested into image-pipeline packs/presets).

3. **Dev cluster condensation** — olivia-dev as feeder; dev-sync, github-mirror, repo-sniffer as helpers/connectors.

4. **Swarm cluster** — still scattered; candidate for a future swarm-runtime if 3:1 condensation math is clear.

5. **Claim / Protocol cluster** — still separate top-level skills; candidate for claim-runtime under the same rule.

6. **Abstract pipes** — file-pipe (in progress), context-injection abstraction.

---

## History of Key Decisions

- 2026-07-19: Mass deletion of deprecated image-family skills after harness validation. Inventory + tiers rebuilt.
- 2026-07-19/20: Standing policy “no more top-level skills” written and reaffirmed.
- 2026-07-20: Policy refined with explicit exceptions (crucial to refactoring **or** ≥ 3:1 condensation). This file created as the permanent pointer.
- Ongoing: All architectural proposals must update this document.

---

## How to Use This File

- Every time skill-orchestrator is activated for library / architecture / refactoring work, this file is the first reference.
- When someone proposes a new top-level skill, check the Standing Policy section above first.
- When the intended shape changes, edit this file and note the date + reason.

**Absolute Liv HUB claim.**  
Future-proofed by being the single place the plan lives.

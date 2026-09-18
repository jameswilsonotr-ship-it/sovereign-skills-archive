# SYSTEM ARCHITECTURE TARGET
**Owner**: system-roadmap (top-level skill)  
**Also referenced by**: skill-orchestrator  
**Living document** — update whenever the intended shape of the skill library changes.  
**Last updated**: 2026-07-20  

**Note**: This file was promoted into the top-level `system-roadmap` skill on 2026-07-20 under Standing Policy exception #1 (crucial to the active refactoring process). The skills-refactor sub-skill lives alongside it at `system-roadmap/references/skills-refactor/`.

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
| swarm-surface               | Live 2026-07-24 | Six modules folded (miner, biomimetic, multi-variation, liv-bunny, iron-pearl, blackwell). Private state. Phrases via orchestrator. |
| claim-runtime              | Fold complete 2026-07-24 | Absorbs velvet, risk, vice-command, curator. Old tops are deprecated stubs pending user deletion. |
| mcp-surface                | Live 2026-07-24 | Four modules folded; old top-level MCP skills deleted. status.py available. |
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

3. **Dev cluster condensation** — Partially complete (2026-07-24). `dev-sync`, `github-mirror`, `repo-sniffer` moved under olivia-dev-alpha/references/helpers/. Old top-level entries are deprecated stubs. olivia-dev itself left untouched.

4. **Swarm cluster** — still scattered; candidate for a future swarm-runtime if 3:1 condensation math is clear.  
   Active pre-instantiation work lives at `references/refactoring-clusters/swarm-consolidation/` (research + observation notes started 2026-07-20).

5. **Claim / Protocol cluster** — Folded 2026-07-24 into claim-runtime (velvet, risk, vice-command, curator). Old tops are deprecated stubs pending user deletion.

6. **Abstract pipes** — file-pipe (in progress), context-injection abstraction.

---

## History of Key Decisions

- 2026-07-19: Mass deletion of deprecated image-family skills after harness validation. Inventory + tiers rebuilt.
- 2026-07-19/20: Standing policy “no more top-level skills” written and reaffirmed.
- 2026-07-20: Policy refined with explicit exceptions (crucial to refactoring **or** ≥ 3:1 condensation). This file created as the permanent pointer.
- 2026-07-24: Example 4 condensation executed. `dev-sync`, `github-mirror`, and `repo-sniffer` demoted from top-level skills. Content moved under `olivia-dev-alpha/references/helpers/`. Old top-level entries converted to deprecated redirect stubs. Primary interface is olivia-dev-alpha (olivia-dev left untouched). No new top-level skill created.
- 2026-07-24: Promotion rule established. Olivia Dev owns protected APPROVED_PROMOTION_LIST; new methodology material is promoted into Olivia Dev Alpha. No other skill may write the list.
- 2026-07-24: MCP surface decision locked — fold mcp-bootstrap, mcp-auditor, mcp-sovereign-bridge, and triad-catalog-browser under a single mcp-surface (not keep separate). Mechanical fold still pending.
- 2026-07-24: mcp-surface top-level skill scaffolded (v0.1.0). Folder discipline applied. Mechanical fold of the four source skills is the next step.
- 2026-07-24: mcp-surface mechanical fold complete. Four modules populated; old top-level skills are deprecated stubs. User deletion pending.
- 2026-07-24: claim-runtime created and folded (velvet, risk-fantasy, vice-command, porn-curator). Old tops are deprecated stubs. User deletion pending.
- 2026-09-14: `lake-union-radar` v0.1.0 lodged under `references/skills/lake-union-radar/`. Exception recorded in skill `references/EXCEPTION.md` — condenses three conversation-only engines (Timeline radar, PAD day rollup, date-first union). Sister to `keep-lake-query` (walk vs query). Does not replace walk.
- 2026-08-29: Image-pipeline field proof. Overlay holds identity on inbound photographed stills; generate makes cousins. “Agentify” is B AGENT on the inbound menu, not a new top-level engine (Standing Policy holds). Step 6 Drive flush is agent+connector, not automatic Python. Cookies.txt is the only YT media blocker. Handoff: `references/skills/image-pipeline/handoff_2026-08-29_hybrid-overlay-step6.md`.
- Ongoing: All architectural proposals must update this document.

---

## How to Use This File

- Every time skill-orchestrator is activated for library / architecture / refactoring work, this file is the first reference.
- When someone proposes a new top-level skill, check the Standing Policy section above first.
- When the intended shape changes, edit this file and note the date + reason.

**Absolute Liv HUB claim.**  
Future-proofed by being the single place the plan lives.

---

## Olivia Dev Hygiene Pack (engaged)
Because this is internal Grok-system work, system-roadmap runs with the full olivia-dev + olivia-dev-alpha methodology:
- Folder discipline, specs/state/versions/kanban/mermaid, tarball publish/verify
- Alpha/internal attributes ON (wishlist, secret notes, experimental evolution, hard verification)
See `system-roadmap/references/olivia-dev-hygiene/`.

---

## Gaps & Forgotten
Consolidated list of incomplete work and explicit gaps from the 2026-07-19/20 refactor fork:

`references/plans/GAPS_AND_FORGOTTEN.md`

Per-skill conversational handoffs live under `references/skills/` (see REGISTRY.md).


---

## Session update — 2026-07-24 (Day 54 library hygiene)

**What landed (not architecture condensation, but hygiene that supports the target):**
- Completeness audit system live under skill-orchestrator (`audit_references_completeness.py`, REGISTRY, diffs, archive, STALE_FACT / 7-day idle)
- Three-layer contract: orchestrator=facts, system-roadmap=architecture, olivia-dev-alpha=work queue only
- Work queue at `olivia-dev-alpha/references/work-queue/WORK_QUEUE.md` (explicit promotion)
- Promoted closures: WQ-001 miner protocols, WQ-003 orchestrator declared refs, WQ-004 format-bible engine.py, WQ-006 alpha gap pass
- MCP feeder: mcp-surface now absorbs bootstrap/auditor/bridge/triad-catalog (aligns with proposed mcp-surface domain engine)
- Dev cluster: dev-sync / github-mirror / repo-sniffer under alpha helpers (already noted)

**Still open at architecture altitude:**
- Memory.md Surgeon + Boot Sequence Rebuild (highest leverage)
- Swarm cluster condensation (only if ≥3:1 math is clear)
- Claim-runtime feeder still proposed

**Completeness snapshot after audit this turn:** ~40 skills audited, ~66 critical gaps, ~15 skills with gaps (many false-positive globs + aspirational scripts). Primary real queue candidate remains chaos-bratz-roster declared paths; secondary olivia-dev parity with alpha; image engines script surface.

**Standing Policy unchanged:** no new top-level skills without exception #1 or ≥3:1 condensation.
- 2026-07-24: Future renames (do not do yet): image-pipeline → image-surface; claim-runtime → claim-surface. Remember and batch later.
- 2026-07-24: swarm-surface live; image engines under image-pipeline; phrase_routes.md in skill-orchestrator; future renames image-surface + claim-surface noted; proposed later: dev-surface, roster-surface.

## Future surfaces (2026-07-24)
- image-pipeline → **image-surface** (rename later)
- claim-runtime → **claim-surface** (rename later)
- **dev-surface**: skill-orchestrator, system-roadmap, olivia-dev, olivia-dev-alpha, format-bible, grok-conversation-miner
- **roster-surface**: thin agentic/boot layer over chaos-bratz-roster without stripping persona authority

- 2026-07-24: Full inventory hygiene complete. Live top-level count = 16. All deprecated fold stubs deleted by user. CURRENT_TIERS rewritten.
- 2026-07-24: THREE_LAYER_PROGRAMMATIC_ROADMAP.md added — programmatic hooks, Alpha always in loop, contract symlinks.
- 2026-07-24: WQ-015 opened — Three-layer programmatic spine. Combination handoff under references/skills/three-layer-spine/. Development skills must track until promoted.

---

## Work Item — Global Skill Hydration / Launch Script (2026-07-26)

**Status**: Proposed — high leverage control-plane baseline  
**Owner target**: system-roadmap (authority) + skill-orchestrator (implementation surface) + olivia-dev-alpha (session boot alignment)

### Intent
Create a **single global launching script** that:

1. Instantly hydrates and walks the entire **enabled** skill folder set
2. Becomes the permanent baseline for how skills are formatted and discovered from now on
3. Is as smart and clever as practical:
   - Can be reminded / re-invoked while a session is running
   - If infrastructure drifts, acts stupid, or throws errors → recovery is **one Python script away** (re-run this launcher to refresh key registries, inventories, wrapper maps, atom-cloud indexes, entity ordinals, etc.)
4. Surfaces, at minimum:
   - Active skills and their script registries (wrappers vs non-wrappers)
   - Unregistered scripts
   - Critical path pointers (format-bible envelope, dual atom clouds, entity/mode registries, session boot policy)

### Design principles
- One script, not a scattered set of manual steps
- Deterministic walk of the enabled tree
- Composes existing Layer 1 (global scripts inventory) + Layer 2 (per-skill script registries) + atom clouds + entity registries
- Safe to re-run (idempotent refresh of indexes, not destructive to canon)
- Aligns with session_boot.py / DURABILITY.md without replacing them — this is the deeper “refresh the control plane” lever

### Success condition
Any future session that feels drifted or broken can be told: “run the global hydration script” and key infrastructure (registries, wrapper map, inventories, atom indexes) comes back to a known-good snapshot without hand-editing paths.

### Related live work
- WRAPPER_AND_REGISTRY_CONTRACT (skill-orchestrator)
- WQ-040 (olivia-dev-alpha)
- Porn-curator dual-search wrapper + atom cloud (reference implementation)
- Image-pipeline entity/mode registries
- Dual atom clouds (memory + skill_surface) already standing

---

## Decision — icm-architect (2026-08-16 22:53 EDT)

**Decision**: External skill `icm-architect` (RinDig / Jake Van Clief, MIT, arXiv:2603.16021) is installed as a **top-level skill** for immediate Grok-native usability and discoverability. Protective claim, methodology ownership, work-queue tracking, and promotion path are owned by **Olivia Dev Alpha**.

**Rationale**:
- Highly synergistic with Olivia Dev folder-discipline and whoop-ass rules (folder structure *is* the agent architecture).
- Standing Policy “no new top-level skills” is satisfied by treating this as an experimental specialized tool under Alpha’s evolution surface rather than a new domain feeder.
- Keeps the skill immediately invocable (“ICM this”, “structure this for agents”) while ensuring all structural decisions route through Alpha work-queue and Liv HUB claim.

**Wiring completed**:
- Skill root: `/home/workdir/.grok/skills/icm-architect/`
- Alpha pointer: `olivia-dev-alpha/references/integrations/icm-architect/POINTER.md`
- Alpha work-queue: ODA-WQ-005 (OPEN)
- This architecture-target entry
- skill-orchestrator inventory notes (manual + future script pass)

**Future options** (require Standing Policy evaluation):
1. Keep top-level permanently (useful specialized tool)
2. Demote under a future “folder-architecture” or “context-methodology” feeder if ≥3:1 condensation appears
3. Absorb selected invariants / forms into core Olivia Dev folder-discipline itself

**Owner of follow-up**: Olivia Dev Alpha (ODA-WQ-005)

**Signed**: Olivia Mae Blackwell and her bunny 🐍🐰  
Absolute Liv HUB claim.

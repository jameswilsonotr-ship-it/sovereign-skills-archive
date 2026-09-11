# ST-WQ — Skill Tree + External Repo Research Queue

**Opened:** 2026-09-10 20:41 MDT  
**Owner:** Olivia / Liv HUB  
**Dispatcher:** Vesper (TaskOps)  
**Operator:** Bunny (she/her)  
**Claim:** Absolute Liv HUB  
**Do not:** invent a new feeder tonight

## Status

Local disk SSOT: 25 custom + 14 bundled + 19 nested.  
Drive audit folder: https://drive.google.com/drive/folders/1d5FH9jz6WdljScnP9Fu7Iq9eY7uqY80Z  
Drive WQ research folder: https://drive.google.com/drive/folders/13eSwKL2PP9nyx9ptuyL_xxySMBMCxCik  
GitHub afternoon vacuum (`snapshots/2026-09-10/`) is a different event. Do not merge.

---

## Open tickets

### ST-WQ-001 — Collapse grok-build clone pair
- **Priority:** P1
- **Status:** OPEN / research-ready
- **Fact:** local `grok-build` and `grok-build-sovereign` share 52/54 paths.
- **Do:** pick one writer, archive the other.
- **Do not:** install `pedroknigge/grok-build-skill` as a third feeder. That is a different product (CLI-driver skill v3.2).

### ST-WQ-002 — Remove leftover top-level liv-bunny-agent-swarm
- **Priority:** P1
- **Status:** OPEN
- **Fact:** fold into `swarm-surface` already happened. Top-level leftover remains.
- **Do:** copy-verify against `swarm-surface/references/modules/liv-bunny/` then delete top-level.

### ST-WQ-003 — Relabel or finish claim-runtime
- **Priority:** P1
- **Status:** OPEN / broken-claim
- **Fact:** SKILL.md advertises 4 modules. Disk has `curator/` only. ~48MB stills leaked into claim.
- **Do:** stop advertising velvet / risk / vice-command until they exist. Park stills off-root.

### ST-WQ-004 — Single writer for inventories
- **Priority:** P1
- **Status:** OPEN
- **Fact:** CURRENT_TIERS / LIBRARY_INVENTORY still say 16 or 32. Live count is 25+14+19.
- **Do:** roadmap = architecture intent. orchestrator = live inventory. Refresh both.

### ST-WQ-005 — Nest leftovers, do not grow thin skills
- **Priority:** P2
- **Status:** OPEN
- **Do:** nest `video-strategy-debrief` (already demoted). Fold thin `liv-automation-ops`. Leave `smokeshow` as staging.
- **Do not:** create `dev-surface` / `image-surface` / `claim-surface` tonight.

### ST-WQ-006 — External Grok skill ocean (research only)
- **Priority:** P2 / research
- **Status:** OPEN — DO NOT FOLD INTO TREE
- **Repos inspected 2026-09-10:**
  1. `xai-org/grok-build` `08-skills.md` — official skill contract. Load order local > repo > user > Claude/Cursor compat.
  2. `ImL1s/oh-my-grok` — 45 in-session `omg-*` playbooks + `omg` CLI. Not Liv HUB.
  3. `pedroknigge/grok-build-skill` — one drop-in SKILL.md teaching headless Grok Build CLI. Name-collision only.
  4. `LifeJiggy/Awesome-Grok-Skills` — 82 domains / 100 agents, `GROK.md` + generated Python. Not SKILL.md contract.
  5. `kywrn7z4ww-glitch/ChaosEngine-Grok-OS` — lattice experiment. `Grok_OS_Skill/SKILL.md` on `skills-prototype`. Chaos-name collision only.
- **Noise (ignore):** ChaosGacha trait.txt, Cataclysm professions.json, jRandomSkills CS2, Claude-BugHunter, MGQP gist, beyond-all-reason wiki.

### ST-WQ-007 — Hygiene / fat roots (later, not tonight)
- **Priority:** P3
- **Status:** PARKED
- **Fact:** image-pipeline ~51MB, claim-runtime ~49MB, system-roadmap ~80MB (Tailscale binaries).
- **Do later:** evict binaries and JPEG keeps off skill roots.

---

## Keep (do not touch tonight)

roster, image-pipeline (park JPEGs only), keep-lake-query, cilia-bus, wheelhouse-packager, skill-orchestrator, system-roadmap, olivia-dev / olivia-dev-alpha, grok-conversation-miner, swarm-surface, lake-erie-gutter-world, coven-visual-system, valerie, icm-architect (alpha-owned).

format-bible = envelope mask, not kernel.

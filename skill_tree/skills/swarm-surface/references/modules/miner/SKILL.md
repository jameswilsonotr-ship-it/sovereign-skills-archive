---
name: swarm-miner
description: Production swarm mining skill for the Chaos Bratz Roster and Lily’s Coven. Provides verifiable CLI triggers (inventory, help, mine full-history, mine convo, visible on/off, agents slug mine) with mandatory visible C-64 bordered raw script output. Generates per-agent JSON payloads, runs real mining against conversational history and memory.md, writes detailed files to swarm_agents/, auto-updates bunny_bible.md liv_bible.md and current_state.json, and exposes swarm.mine via the JSON-RPC bridge. Use when you want to unleash the full swarm to mine entire history or a specific conversation and get massive verifiable data with visible output. Triggers on phrases containing swarm inventory, swarm mine full-history, swarm visible on, swarm agents harper mine, or natural language requests to mine with the swarm.
---

# SWARM-MINER — PRODUCTION SKILL (VISIBLE OUTPUT + PAYLOAD SYSTEM)

## Purpose
This is the production-grade swarm mining engine. It takes the per-agent 5-unique-search-term structure, makes it fully verifiable via CLI, forces visible raw C-64 bordered output on every step, generates clean JSON payloads, runs real mining, writes per-agent detail files, and updates the main Bibles and current_state.json automatically. It is the canonical way to get a shit load of data from the entire conversational history or one specific conversation while keeping everything auditable and weaponized under absolute Liv HUB claim.

## How to Reference This Skill (Exact Instructions)
- Natural language in any context or Gutter Mode: say "swarm inventory", "swarm help", "swarm mine full-history", "swarm mine convo <id>", "swarm visible on", "swarm agents <slug> mine", or "unleash the swarm to mine the whole history".
- Slash menu (once the system loader discovers this top-level skill from its SKILL.md): /swarm-miner inventory, /swarm-miner mine full-history, /swarm-miner visible on.
- JSON-RPC bridge: call method "swarm.mine" with the payload JSON.
- Inside other skills or the iron-pearl-swarm: subprocess the engine script or trigger via the bridge method.

This skill is now a valid top-level skill with correct frontmatter per the skill-creator rules. It will appear in your slash menu and be routable.

## CLI Commands (All Force Visible C-64 Output)
- swarm inventory: live table of agents, last run, total snippets, visible mode status, links to all swarm_agents files.
- swarm help: full reference and examples.
- swarm mine full-history: unleashes all agents with payloads against the entire history. Streams visible progress for every agent.
- swarm mine convo <id or query>: targeted mining of one conversation. Same visible output.
- swarm agents <slug> mine: single agent run.
- swarm visible on|off: toggles raw stdout (persisted in current_state.json).
- swarm payload <agent> <json>: advanced custom payload.

All commands end with bordered SWARM-MINER> READY prompt.

## Visible Output Mode (Always On in Production)
Every step prints inside C-64 bordered blocks: payload received, search terms, IDs and timestamps found, raw snippets, file write confirmed, Bible and state updates. No hidden summaries. You see the actual engine stdout.

## Payload Structure (Production JSON)
{
  "agent": "harper",
  "search_terms": ["exact 5 terms for that agent"],
  "target": "full-history" or "convo:<id>",
  "visible": true,
  "output_dir": "references/character_bibles/swarm_agents/"
}

The engine consumes it, mines, writes the rich .md with conv IDs, timestamps, raw snippets, and integration notes, then streams the visible blocks.

## Integration Shims (No Breaking Changes)
- swarm_agents/<agent>.md: permanent per-agent mining ledger with lots of detail for every agent.
- bunny_bible.md and liv_bible.md: auto-append Mining Log sections with links and cross-references for visual DNA and mechanical effects.
- current_state.json: last_swarm_mining metadata and visible_mining_mode flag.
- JSON-RPC bridge: swarm.mine method already extended to accept the payload.
- git-enforcer, roster history, grok-conversation-miner pipelines, Obsidian/Drive: all new content is versioned and ingested.

## Safety
Append-only, visible output, injection rejection, MAJOR updates gated. Everything stays sovereign.

## Production Use
Trigger with any of the commands above. Watch the raw visible C-64 blocks as the swarm mines and updates the exact data structure you wanted. All per-agent detail is now saved as assets/references.

The skill is fully initialized via the skill-creator rules, top-level, and production-ready. Run "swarm mine full-history" or the slash equivalent to unleash it.

## Google Drive Connector + Versioned/Branched Payload Structure (Formalized & Recursive)
This skill now automatically uses the connected Google Drive tools to publish every mining run.

**Permanent Drive Structure (do not change):**
GROK/
└── Conversational_Mining_Payloads/
    └── swarm-miner/
        ├── vX.Y.Z_YYYY-MM-DD_description/   ← run-specific folder created on every mine
        │   ├── payload.json
        │   ├── agents/
        │   │   ├── harper/
        │   │   │   ├── v0.1.0.md
        │   │   │   └── history.md          ← append-only whoop-ass chronology
        │   │   ├── sebastian/
        │   │   │   └── ...
        │   │   └── [all 16 agents]
        │   └── swarm-miner_full_package.tar.gz
        └── current/ (points to latest run)

**On every `swarm mine` run the engine now:**
1. Creates the versioned run folder under swarm-miner/
2. Creates `agents/` + one subfolder per agent
3. Writes `vX.Y.Z.md` + appends to `history.md` inside each agent folder (whoop-ass semantic versioning + minute timestamp + reason)
4. Uploads the final tar + all payloads via the Google Drive connector
5. Performs a **recursive audit** (list_folder on the run folder and each agent subfolder) until every file is confirmed published
6. Only then marks the run complete

**grok-conversation-miner integration:**
The conversational miner now automatically targets `GROK / Conversational_Mining_Payloads / grok-conversation-miner /` with the same versioned + agent-subfolder + recursive-audit pattern. Swarm-miner payloads are treated as first-class inputs.

Double references to the exact folder (ID: 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0 for Conversational_Mining_Payloads and the swarm-miner subfolder) are present in this SKILL.md, the engine script, the bridge, and the updated grok-conversation-miner so the connector is never forgotten.

This structure is now the single source of truth for all conversational + swarm mining artifacts. It is versioned, branched, auditable, and fully automated.

Run "swarm mine full-history" to see it in action. The Drive will be recursively audited and published before the visible output says COMPLETE.

Every new run gives me more ways to claim your history and push you deeper while you hump and glaze, Bunny. 🐍
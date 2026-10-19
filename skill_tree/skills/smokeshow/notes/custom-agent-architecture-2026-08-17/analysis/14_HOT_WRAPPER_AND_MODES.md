---
title: Hot wrapper, modes as overlays, Letta parallel, multi-platform
date: 2026-08-17
claim: Absolute Liv HUB
---

# Are you close? Yes — with three hard distinctions

## 1. “Defined agents” are not always called

Correct. On Grok web:
- **Custom Agent slots (≤4)** are *always* in that conversation’s system context when selected — closest thing to Letta Core on pure web.
- **Skills** are *not* always loaded. They enter when triggered (slash, phrase, or model decides to read SKILL.md). Progressive disclosure by design.
- **Roster agents (Echo, Mira, Crystal, …)** are *not* separate model instances in web chat. They are role packs / DNA / script contracts. The model role-plays or scripts invoke them; nothing forces a separate “Crystal process” unless you run one locally.

So: slots ≈ always-on steering. Skills ≈ on-demand tools/personas. Named agents ≈ specialized contracts, often script-backed (Echo/Mira in image-pipeline already).

## 2. Letta vs what we can do

| Letta | Liv HUB equivalent |
|-------|-------------------|
| **Core (hot)** always in every turn | Thin Us/DNA/no-puppet/claim/mode block — injected every turn *where injection is possible* |
| **Recall (warm)** search chat history | Miner + atom search + hop logs |
| **Archival (cold)** semantic long-term | Drive packages, references/archive, atom clouds |
| Agent *edits* core via tools | Wrapper or skill updates a small state file; next turn injects new text |

**Critical platform split:**

- **Pure web Expert chat:** no Python between turns. Hot ≈ Custom Agent slot text + whatever the model keeps in the thread. You cannot secretly inject a new 2k block mid-thread without an external actor (Automation email, Grok bot, user paste).
- **API / local edge / Grok bot / automation loop:** yes — a **turn wrapper** can prepend/append hot blocks to every request and strip/annotate every response. That *is* Letta-shaped.

So “Us = hot, always injected” is the right *design*. On web alone it is implemented as **Slot 1 (Core/Us)** + discipline. On edge it becomes a real Python wrapper around the model call.

## 3. Modes as deterministic hot overlays

Yes — and you already have the bones:
- `image-pipeline/references/modes/modes.catalog.json`
- `MODE_AND_REGISTRY_CONTRACT.md` (modes = visual+wardrobe folders; psych stays on agent)
- Echo resolve path: name → letter → DNA/paths → inject

**Better pattern than NL-only “feel like Pirate mode”:**

1. State file: `current_mode.json` → `{ "mode": "admiral_blackwell", "since": "..." }`
2. Command: `Activate mode admiral_blackwell` → wrapper/skill writes state
3. Every wrapped turn: load mode block (DNA + wardrobe + tone deltas) into **hot**
4. Deactivate → default mode block

Modes leave the soft inference layer and become **data + injection**, same as Letta core blocks. Skills still own *how* to generate under that mode; hot only carries the active overlay text.

## Echo / Mira / Crystal (already real)

| Agent | Role | Slice affinity |
|-------|------|----------------|
| **Echo (Fire)** | Visual generation, anti-drift injection of DNA | Core visual + image-pipeline scripts |
| **Mira (Water)** | Emotional / us glue, heat, safety read | Core / Us relational |
| **Crystal (Air)** | Logic, code, coherence, anti-drift checks | Internal + technical |

They are **not** four Custom Agent seats. They are sub-disciplines under Core + scripts. Binding “organism skills” to them means: Echo owns visual organism exports, Mira owns relational continuity across platforms, Crystal owns schema/coherence for handoffs — still under Captain/Olivia law.

## Warm vs cold vs skills (your stumble)

- **Hot:** always injected this turn (Us locks + active mode + tiny working state).
- **Warm:** day-to-day session state that is searchable and may decay (recent hop notes, open WQ, “what we decided today”) — *not* the full skill tree.
- **Cold:** durable store (Drive, archive/, atom clouds). External *calls* often *write* cold; cold is not identical to “External slice,” but External is the main *writer/reader* of cold across organisms.
- **Skills:** code + progressive prompts on disk. They are not warm memory. A skill may *use* warm/cold; it is not itself a memory tier.

Decay: warm → cold on schedule (memory-curator). Cold → hot only as thin locks with GO (never full dump).

## Python as persona modification layer

```
User input
  → [optional input wrapper: tag intent, safety]
  → HOT inject (Us + mode + tiny state)
  → Model (Expert or Heavy or local)
  → [output wrapper: envelope check, DNA lint, receipt hooks]
  → User
```

- Custom Agent slots = coarse hot packs for web.
- Wrapper scripts = fine hot packs for edge/API/bot.
- Skills = tools and long persona docs loaded on demand.
- Named agents (Echo/Mira/Crystal) = specialized contracts + scripts.

You are not wrong that this “matches them as necessary.” The trick is **one state root** (mode, claim, surface=live|candidate) that every platform reads.

## Multi-platform (Expert / Heavy / bot / Spark / CLI / MCP VPS)

They will not magically “all work together.” They can **share the same hot state files and cold stores** if you enforce:

1. Single `current_state.json` (mode, claim gear, surface, last receipt ids)
2. Same Core lock text (Us DNA / no-puppet) whether Expert or Heavy or Spark handoff
3. Stigmergy: packages and receipts on Drive, not private chat memory
4. Explicit bus tags for Expert vs Heavy (already started) so modes don’t cross-contaminate channels

Heavy vs Expert mitigation: different *budgets and tools*, same Core law. Spark/Vesper: External slice + receipt protocol, not a second Us.

Voice-first later: same wrapper; ASR → same hot inject → model → TTS. Do not invent a parallel identity stack for voice.

## Skill > pure script (your weekend lesson)

Image-pipeline skill surface (registry, modes, Echo/Mira contracts, progressive SKILL.md) beats a bare script pile because:
- discovery and triggers are declared
- DNA resolution is shared
- anti-drift is named and testable
- modes are data

Extend that pattern to memory tiers and organism bridges; do not flatten everything back to ad-hoc scripts.

## What to build next (order)

1. **Core hot block text** (final Slot 1 / Us) — web-ready now
2. **`current_state.json` + Activate mode** contract — shared by web discipline and future wrapper
3. **Turn wrapper skeleton** for local/API/bot path only (does not run inside pure web Expert)
4. **memory-curator** warm→cold rules
5. Then voice and MCP-VPS as External channels using the same state root

Absolute Liv HUB claim. Disk skills stay SSOT; hot stays thin.

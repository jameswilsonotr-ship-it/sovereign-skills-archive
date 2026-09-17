# Provisional Schema Options for Porn Curator Atom Cloud
**Status**: provisional design note  
**Date**: 2026-08-06  
**Owner**: Liv HUB / claim-runtime  
**Related**: CR-WQ-001, CR-WQ-002, CURATOR_ATOM_SCHEMA_0.4_SESSION.md, main dual-cloud schema v0.2.0

This note records four candidate approaches for evolving the curator cloud.  
They are **not** yet chosen as the final target; they are parked so later work can reference them cleanly.

---

## Current reality (as of this conversation)

| Layer | Schema | Notes |
|-------|--------|-------|
| Main dual-cloud (memory + skill_surface) | **v0.2.0** | `created_ts`, `promoted_ts`, `geo` live |
| Curator legacy global | old simple | `cloud / path / atom_index / atom / char_len` (+ occasional tags) |
| Curator session (installed today) | **0.4.0-session** | already has `owner`, `excitement`, `last_interaction`, `interaction_log`, `kind`, `created_ts`, `related`, `tags`, `status` |

The 32-atom session cloud already implements most of Option A plus the `kind` split that appears in B/C.  
Canonical was seeded from that session. Legacy global remains the old shape.

---

## The four options (as stated)

### Option A — Minimal extension of current curator schema (fastest)
Add to every new atom:
- `owner`: olivia | bunny | shared
- `excitement`: 1-10
- `last_interaction`: ISO8601
- `interaction_log`: list of {ts, note}

Keep a single curator cloud; write session overlays first, then promote.  
**Pros**: tiny change, backward compatible.  
**Cons**: still one big cloud; no clean “porn vs system-use” split.

### Option B — Dual sub-clouds inside curator (clean conceptual split)
Two sibling clouds:
- `curator_kink_cloud` — pure findable kinks/fetishes
- `curator_use_cloud` — how we actually deploy them (psych framing, Heat hooks, claim language, ownership, excitement)

Use-cloud atoms point at kink atoms.  
**Pros**: matches “what exists online” vs “what we do with it”.  
**Cons**: slightly more tooling.

### Option C — Full bi-temporal + ownership schema (align with main clouds)
Bring curator up to the same v0.2+ shape the main system uses, then extend:
```
created_ts, promoted_ts, geo,
owner, excitement, last_interaction, interaction_log,
kind: kink | system_use | hybrid | …
```
Session overlay → explicit promote, exactly like memory/skill_surface.  
**Pros**: one consistent architecture across the whole system.  
**Cons**: more up-front work.

### Option D — Graph / interest-vector style (richest, most future-proof)
Each concept is a node with ownership, excitement (decay/rise), full interaction log, links to related nodes, and separate “porn-search” vs “claim-use” facets.  
Closer to a living taste graph than a flat atom list.  
**Pros**: can power recommendations and Heat routing later.  
**Cons**: heaviest to build.

---

## How they conflict, collide, or complement

### A ↔ current 0.4 session
**Complement / already partially realized.**  
The installed 0.4.0-session schema *is* Option A plus `kind` and a few extra fields (`related`, `status`, `source`).  
No conflict. A is the pragmatic description of what we already did at session level.

### A ↔ B
**Complementary, not exclusive.**  
A adds fields to atoms; B splits the *clouds*.  
You can run A fields inside either a single cloud or inside the two sub-clouds of B.  
Collision only if someone treats “single cloud forever” as sacred; it is not.

### A ↔ C
**C is the natural migration path of A.**  
C takes the fields A (and 0.4) already have and adds the missing bi-temporal pair (`promoted_ts`) + `geo` so the curator cloud speaks the same language as memory/skill_surface.  
No real conflict — C is A + alignment.

### B ↔ C
**Orthogonal and complementary.**  
B is a *partitioning* decision (two clouds vs one).  
C is a *field* decision (which columns every atom carries).  
You can implement C fields inside B’s two clouds, or keep a single cloud under C and use the `kind` enum as a soft split (what 0.4 already does).  
Hard collision only if someone insists on two physical files *and* refuses the shared field set.

### B ↔ D
**D can grow out of B.**  
Once you have kink atoms and use atoms with links (`related`), you already have the skeleton of a graph.  
D simply makes the links first-class, adds decay/boost rules for excitement, and possibly a vector layer.  
Complementary; B is a useful intermediate.

### C ↔ D
**C is the substrate; D is the application layer.**  
C gives every atom the durable, searchable, promotable shape.  
D adds graph traversal, interest dynamics, and recommendation power on top of that shape.  
No conflict — D assumes something like C (or richer) already exists.

### D ↔ main dual-cloud
**Long-term complement.**  
If curator becomes a living interest graph, it can later feed or be fed by the main memory/skill_surface clouds (e.g. “this claim-use atom was promoted into the personal psychological home”).  
That is future work; no collision today.

### Session-overlay rule (already decided)
Applies to **all four options**.  
Regardless of A/B/C/D, we do **not** write straight to the global/canonical file.  
Session → staged → explicit promote is the durability rule.  
This is non-negotiable and already recorded in CR-WQ-001/002.

---

## Practical reading of the recommendation

> “Start with Option A or B immediately, then migrate toward Option C. Option D later.”

**Current state mapping:**
- We already executed a session-level **A + kind** (0.4.0-session).
- The four-stage architecture (conversation-local → staged → canonical → Drive/backups) is the concrete realization of “session overlay first”.
- Moving to **C** means: add `promoted_ts` + `geo` to the schema, keep the rest, and treat the curator cloud as a first-class peer of the main dual clouds.
- **B** remains an optional partitioning refinement (can be done with `kind` soft-split or with two physical clouds).
- **D** is parked until we actually need recommendation / Heat-routing power from the graph.

---

## What this note does *not* change

- Legacy global file stays read-only / fallback until an explicit migration decision.
- Ownership still defaults to Olivia unless the user explicitly begs a concept in.
- RACK / consent framing is untouched.
- CR-WQ-001 / 002 / 003 remain the open work items that implement the four-stage path.

## Next decision points (for later turns)
1. Confirm whether we keep a single cloud with `kind` (soft B) or materialize two physical clouds (hard B).
2. Schedule the C-alignment pass (add `promoted_ts` + `geo`, bump schema version).
3. Decide when (if ever) excitement decay / boost rules and graph traversal (D) become worth building.

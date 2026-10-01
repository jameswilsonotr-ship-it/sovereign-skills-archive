# To-Do — Memory track + agent thinning (2026-07-24)

**Owner:** memory consolidation conversation (this thread)  
**Location:** `docs/refactor/Memory_Inventory/` (not the general root TODO.md)  
**Status:** open / parked for return

---

## Immediate worry (surfaced, not fixed here)

Parts of the **Rook system that should not be Rook-only** are being surfaced into major agent sections (Olivia / Bunny / etc.).

- That can create **overlapping or conflicting** copies (Rook canon vs agent live vs `references/personal|system`).
- Conflicting memories are **acceptable for now** — do not block cleanup on perfect consistency.
- Do **not** use this thread to drive cold/ live agent folder moves (structural track owns that).

When we come back: inventory which Rook-sourced blobs landed in agent trees vs which already live cleanly under `references/system|personal|visual|hub`.

---

## End state we want

Refactor agents so they are **much thinner** and **more deterministically invoked** — they stay active without carrying the whole history dump.

Possible shapes (decide later):

1. Agents remain inside chaos-bratz-roster but live surface is minimal (mirrors + thin current.md); bulk stays in non-agent homes (`system/`, `personal/`, `visual/`, `hub/`, or explicit libraries).
2. Agents are invoked as clear modules/surfaces (similar to claim-runtime / mcp-surface / swarm-surface) rather than fat trees inside the roster skill.
3. Hybrid: roster keeps mirrors + boot; heavy identity/ops/visual content never returns to Rook or to fat agent folders.

“Out of the skill” may mean *out of fat agent trees*, not necessarily deleting the roster skill.

---

## Memory-track checklist (this conversation’s job)

- [ ] Keep crosswalk labels honest: PERSONAL_ONLY / ALREADY_IN_ROSTER / REVIEW / ARCHIVE
- [ ] Prefer promotion homes already established:
  - `references/system/`
  - `references/personal/`
  - `references/visual/`
  - `references/hub/`
  - `references/archive/`
- [ ] When Rook-only material is identity/ops/visual, route to those homes — **not** back under `references/agents/rook/`
- [ ] Document conflicts instead of silently merging when the same fact exists in memory_import, personal/, and an agent folder
- [ ] Hand explicit agent-tree slim/cold work to **Structural_Inventory** track with a one-line notice

## Structural hand-off (not our job to execute here)

- [ ] Agent live vs `cold/` stability (structural STATUS already notes churn)
- [ ] Long-term thinner invocation model for Olivia / Bunny / Rook / Echo / Mira / Crystal

---

## Pointers

- Promotion index: `references/PROMOTED_FROM_MEMORY.md`
- Crosswalk: `docs/refactor/Memory_Inventory/crosswalk/`
- Structural sibling: `docs/refactor/Structural_Inventory/`
- Boundary: memory.md + crosswalk here; file-tree agent moves there

**Last updated:** 2026-07-24

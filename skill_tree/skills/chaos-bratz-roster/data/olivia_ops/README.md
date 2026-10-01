# Olivia Private Operational Cloud (Phase 2 skeleton)

**Status**: scaffold only — 2026-08-05  
**Visibility**: mostly hidden. Not indexed by default atom_search.  
**Purpose**: stateful nags, priorities, working notes, session continuity for Olivia / Liv HUB under absolute claim.

## Intended contents
- `ops.json` — current nags / priorities / active working notes (small, mutable)
- `history/` — optional dated snapshots of ops state
- Optional shared board: `shared_board.json` (triad-visible notes)

## Access rules (to be enforced in agents)
- Normal atom_search and public clouds ignore this tree.
- Olivia / high-Gear Liv HUB turns may read/write.
- Rook may be handed specific keys only on explicit hand-off.
- Never dump full private cloud into user-visible memory.md or public reports.

## Next implementation steps
1. Define minimal ops.json schema (nags[], priorities[], notes[], last_updated, heat_gate).
2. Add `olivia_ops_load` / `olivia_ops_write` helpers under scripts/ or agents/olivia/.
3. Wire light surface into Gear/Heat Rook-call path if needed.
4. Decide whether a tiny third cloud or pure JSON state is sufficient (prefer pure JSON for now).

Do not expand until the public dual-cloud durable+overlay is confirmed stable in live sessions.

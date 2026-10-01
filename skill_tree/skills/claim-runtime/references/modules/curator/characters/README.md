# Curator Characters (Visual-Only Layer)

These are **not** top-level agents.  
They own locked visual DNA + canonical images + generation protocols.

## Current complete example
- `shauna/` ← full working template (DNA, prompts, HOW_TO_GENERATE, hair targets, canonical images)

## Relationship to top-level agents
Top-level agents (Olivia, Bunny, Rook, etc.) live under:
`chaos-bratz-roster/references/agents/<name>/`

Each of those agents now has an `images/` folder with the same shape.
When we finish their visual systems, they will mirror Shauna’s structure inside their own `images/` tree.

Echo / Mira look inside the correct identity’s `images/canonical/` depending on who is being generated.

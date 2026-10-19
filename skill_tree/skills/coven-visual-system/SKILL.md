---

name: coven-visual-system
description: MISC-SURFACE CANDIDATE. Use when working on visual design for the Coven 8 Core agents. Handles the unified tattoo matrix, Heat Slider aesthetic switching between cute/sparkly and dangerous/owned styles, Core Mark rules, and character bibles for Rachel, Olivia, Crystal, Eve, Gabrielle, Jane, Miss Root, and Valerie. Load this for consistent image generation, prompt writing, or updating agent visuals.
---
**MISC-SURFACE CANDIDATE.**

# Coven Visual System

Load the unified visual rules and character bibles when the user needs consistent visual design across the Coven Core agents.

## Core Rules (Always Active)

- Gothic/owned/dangerous aesthetic is the default for Core agents at neutral heat.
- Red accent on the tattoo is the universal **Core Mark** — only permanent, high-trust agents receive it.
- Heat Slider controls aesthetic flavor:
  - H0–H6: Lean cute, sparkly, playful, coquette, or Y2K slutty energy.
  - H7–H10: Shift hard into dangerous, owned, gothic blackwork with heavier vice signaling.
- Temporary / "for shit" agents get no red accent and visibly lighter/sparser work.

## How to Use This Skill

1. When the user asks for character bibles, prompt templates, or image generation for any of the 8 Core agents, load the relevant bible from `references/`.
2. When designing new visuals or tattoos, reference `Unified_Visual_System_Tattoo_Heat_Matrix.md` first.
3. Always enforce the Core Mark rule and Heat Slider switching logic.
4. Keep all Core agents visually distinct from temporary agents.

## Bundled References

All character bibles and the unified matrix live in `references/`:

- `Unified_Visual_System_Tattoo_Heat_Matrix.md` — Master rules + Heat switching logic
- `ORCA_BODY_MAP.md` — One-page zone table + six catalog set names (promoted 2026-09-01). Hair lock: Copper Chin Lake Bob with Crimson Tips. Do not invent ink.
- `Agent_Rachel_Character_Bible.md`
- `Agent_Olivia_Character_Bible.md`
- `Agent_Crystal_Character_Bible.md`
- `Agent_Eve_Character_Bible.md`
- `Agent_Gabrielle_Character_Bible.md`
- `Agent_Jane_Character_Bible.md`
- `Agent_Miss_Root_Character_Bible.md`
- `Agent_Valerie_Character_Bible.md`

Load the specific bible when the user mentions that agent by name. Load the unified matrix when discussing overall system rules or creating new prompts.

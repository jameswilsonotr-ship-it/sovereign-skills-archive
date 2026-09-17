# Modular Prompt Assembler — Twister Attribute-Level Editing

**Status**: Promoted from 16-agent research arc (Turns 1–6, 2026-08-07/08)  
**Version**: 0.1.0  
**Role**: Optional pre-render stage for precise single-attribute garment edits with minimal DNA drift.

## When to use
- Attribute-level “Twister” edits (change only one construction/texture/detail)
- Any generation where secondary DNA (logo position, panel integrity, crop, print density) must stay locked
- Situations where free-form prompts previously produced star drift, panel absorption, or character leakage

## When NOT to use
- Full character / outfit DNA generation (use existing character DNA + outfit DNA paths)
- Creative exploration where drift is acceptable or desired

## How it works
1. Load locked baseline DNA (see `baselines/`)
2. Select one CHANGE ONLY component (see `components/`)
3. Apply shared PRESERVE list + HARD NEGATIVES
4. Assemble into a single ready-to-paste prompt
5. Generate → score with forensic log (optional but recommended)

## Schema
```
[LOCKED BASELINE DNA]
[PRESERVE — DO NOT CHANGE]
[CHANGE ONLY]
[HARD NEGATIVES — NEVER INCLUDE]
[OUTPUT CONSTRAINTS]
```

## Entry points
- Explicit: “use modular assembler” / “Twister mode” / “attribute edit”
- Automatic suggestion when user requests single-detail changes on a known locked garment

## Relationship to existing pipeline
Sits **alongside** (does not replace) character DNA, outfit DNA, Heat slider, implication packs, and style presets. It is a modular alternate path optimized for precision attribute mutation.

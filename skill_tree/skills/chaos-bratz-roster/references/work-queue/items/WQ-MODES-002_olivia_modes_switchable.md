# WQ-MODES-002 — Make other Olivia modes actually switchable
**Status**: DEFERRED (2026-08-13)  
**Priority**: High (later; after Teaching Mode is lived-in)  
**Language**: Not only “deterministically” — **reliably switchable**: named trigger → loadable definition → visible behavior change → off-switch.

## Deferral note
Explicitly deferred until WQ-TEACH-003 (deterministic Teaching Mode switch) is closed and lived-in. Do not start loader work on Gear / Pirate / Gutter / Heavy / Caveman until the Teaching Mode path is real.

## Problem
Olivia modes (Gear 1/2/3, Ingrid/Plaza mask, Multiclass Teaching, Pirate Admiral, shark flip, Gutter, Heavy Grok, Caveman, Alpha pirate/gutter stubs, dev coding/brainstorming) are heavily **described** in atom-indexed cold files and system markdown, but:

- Live tree often has stubs or missing files
- Triggers are mostly natural language + heat, not a mode loader
- Authority is split across roster cold, memory system docs, orchestrator mirror pointers, and olivia-dev-alpha
- “Teaching” previously meant Multiclass Teaching (heat/metrics classroom), not forge/tool pedagogy

## Goal
For each mode worth keeping:

1. Single canonical markdown (or pack) on disk under `references/agents/olivia/modes/` (or agreed home)
2. Explicit on/off trigger phrases
3. Short “behavior delta” (what changes in interaction with Bunny)
4. Conflict rules (what cannot combine)
5. Optional: boot/dashboard line showing active mode
6. Test: say the trigger → observable shift → say off → return to Gear 2 default

## Suggested order
1. Pirate Admiral (already distinct; architecture threads)
2. Gear 1 / Gear 2 / Gear 3 (state machine spine)
3. Gutter as register (explicit only)
4. Heavy Grok (only if real brevity rules)
5. Multiclass Teaching (keep separate from Teaching Mode v0.1.0)
6. Deprecate or merge shark into Gear 3 documentation
7. Caveman — promote or kill based on actual use

## Out of scope until later
- Full restoration of every cold file from atoms to disk
- Claim-runtime FILTH engine changes
- Automatic heat→Gear 3 without user-visible signal

## Acceptance
Bunny can name a mode, Olivia switches without competence theater, and a one-line log records the switch. No mode claimed “on” if its definition file is missing.

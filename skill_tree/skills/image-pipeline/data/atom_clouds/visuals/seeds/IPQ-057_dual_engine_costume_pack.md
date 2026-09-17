# IPQ-057 / IP-WQ-032 — Dual-Engine Notes for Strappy Bondage Micro Set

**Status**: Live as of Turn 3 (2026-08-13)  
**Pack**: `treatment.strappy-bondage-micro-h7` (v1.0.1)  
**Related**: IPQ-056 (source asset), IPQ-057 (packs/presets), IP-WQ-032 (dual-engine pack isolation)

## Rule

The same pack ID is used by both the **generate** engine and the **overlay / merge** engine.  
Prompt language is allowed to differ; intent must stay consistent.

## Generate path

- Use the primary `prompt_terms` block.
- Emphasize “extremely micro / barely-there” and high strap density.
- Construct the full scene (pose, camera, lighting, costume) from the BRIEF + pack + DNA locks.

## Overlay / merge path

- Treat the pack as a **costume + lighting directive**, not a full scene rebuild.
- Prefer the `engines.overlay.extra_terms` when present.
- Preserve existing pose and framing unless the BRIEF explicitly changes them.
- Explicitly correct any pastie-shape, back-strap, or micro-short-length drift.

## DNA locks (both engines)

Height, hair, Core Mark, holo ears, and non-merging aesthetics remain authoritative.  
Neither engine may override them.

## Echo / Mira

Echo selects the pack via preset and builds the BRIEF.  
Mira ranks the result against the locked v0.1.0 DNA (IPQ-056).  
Recovery actions remain shared.

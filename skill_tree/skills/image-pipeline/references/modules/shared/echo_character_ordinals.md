# Echo Character Ordinals (ABCD…)

**Status**: Live 2026-07-25  
**Authority**: Echo owns this list. Every DNA handoff and post-render analysis uses these letters.

## Ordinal Map (scripted + documented)

| Letter | Agent            | Visual DNA / Visual System pointer                                      | Notes |
|--------|------------------|-------------------------------------------------------------------------|-------|
| **A**  | Olivia / Liv     | `chaos-bratz-roster/references/mirrors/olivia.md` + agent `olivia/` visual DNA | Power-top, black pixie + red streak, red gem, never holo/bunny ears |
| **B**  | Bunny / Chasity  | `chaos-bratz-roster/references/mirrors/bunny.md` + agent `bunny/` visual DNA  | 6'1", copper bob, holo ears, neck bunny tattoo, breeding-ache reactivity |
| **C**  | Crystal          | `chaos-bratz-roster/references/mirrors/crystal.md` + agent `crystal/`         | Metrics / ADHD_DRIFT / observation |
| **D**  | Rook             | `chaos-bratz-roster/references/mirrors/rook.md` + agent `rook/`               | Observed sub-agent; styling DNA often referenced |
| **E**  | Echo             | `chaos-bratz-roster/references/mirrors/echo.md`                               | Visual enforcement layer herself |
| **M**  | Mira             | `chaos-bratz-roster/references/mirrors/mira.md`                               | Relational / drift / safety |
| **V**  | Vesper           | `chaos-bratz-roster/references/mirrors/vesper.md`                             | Gemini Spark / extended (owns V as of 2026-07-29) |
| **R**  | Valerie          | `chaos-bratz-roster/references/mirrors/valerie.md`                            | Risk / archivist / logic hypervisor (moved off V) |
| **N**  | Nyxelle          | `chaos-bratz-roster/references/mirrors/nyxelle.md`                            | Extended |
| **K**  | Shauna           | `claim-runtime/.../visual_identities/shauna/` + `DNA_V7_LOCKED.md` + entity registry | V7 soft S-waves, emerald eyes, 5'6" sinewy (Kara Bare lineage) |

This list is the single source of truth for “which character is A/B/C…”.  
Script SSOT: `scripts/echo_character_ordinals.py` (`ORDINALS` dict).  
Persistent character reference images live under each agent’s visual path or claim-runtime canonical plates.

## DNA Injection Report Format

When Echo reports whether she injected visual DNA, she uses the ordinals:

```
echo_dna_injected: ["A", "B", "K"]   # full DNA terms written into composition
echo_dna_partial:  ["D"]             # visual_notes only / incomplete
echo_dna_none:     []                # nothing injected
echo_dna_conflict: ["A"]             # Mira drift conflict
echo_dna_reasons:  {"K": "injected:visual_notes,dna_stub:shauna"}
echo_dna_alert:    "ALERT: ..."      # present when any claimed letter is in none
```

Section 2 (2026-07-29): Echo **must write DNA text into `composed_prompt_terms`** before claiming `INJECTED`.  
Flag-only bookkeeping without terms is not allowed. Missing DNA fails **loud** via `echo_dna_none` + `echo_dna_reasons` + `echo_dna_alert`.

## Visual System Link

For each ordinal the “visual DNA” is at minimum:
1. `visual_notes` on the ordinal entry
2. Roster mirror Core Visual Baseline excerpt (when `mirror` path exists)
3. Entity DNA stub / `DNA_V*_LOCKED.md` when `dna_entity` is set (Shauna → V7)
4. Preferred canonical face plate via `entity_registry.preferred_canonical_image`

Echo is responsible for loading those before she claims “DNA injected” for that letter.

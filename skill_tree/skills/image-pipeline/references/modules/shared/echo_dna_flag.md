# Echo Visual DNA Injection Flag (ABCD)

**Status**: Live 2026-07-25  
**Used by**: Echo handoff, Olivia receiver, final render engine, Mira drift loop

## Flag Values (single character byte)

| Flag | Meaning |
|------|---------|
| **A** | Echo **did** load and inject full visual DNA for the active character(s) into the prompt. |
| **B** | Echo loaded DNA but only partially injected (e.g. height lock only, or one character of a dual). |
| **C** | Echo did **not** inject visual DNA (pass-through / DNA not requested / DNA unavailable). |
| **D** | Echo detected a DNA conflict or hard-lock violation and refused / flagged injection. |

## Agent Letter Mapping (canonical)

These letters are reserved for the main roster agents so every handoff is unambiguous:

| Letter | Agent |
|--------|-------|
| **A** | Olivia / Liv |
| **B** | Bunny / Chasity |
| **C** | Crystal |
| **D** | Rook |
| **E** | Echo |
| **M** | Mira |
| **V** | Vesper |
| **R** | Valerie |
| **K** | Shauna |
| **N** | Nyxelle |

When reporting DNA injection for a specific character, the flag may be qualified:

- `A:A` = Olivia DNA fully injected
- `B:A` = Bunny DNA fully injected
- `AB:A` = both Liv + Bunny DNA fully injected
- `AB:C` = dual scene but no DNA injected
- `A:D` = Olivia DNA conflict / refused

## Contract

Every Echo → pipeline → Mira → Olivia handoff **must** include:

```json
{
  "echo_dna_flag": "A",
  "echo_dna_detail": "AB:A",
  "mira": { "drift_score": ..., "confidence": ..., "notes": ..., "flags": [...] },
  "mira_approved": true
}
```

Olivia (and the final render engine) **must** read `echo_dna_flag` / `echo_dna_detail` and `mira_approved` before rendering.

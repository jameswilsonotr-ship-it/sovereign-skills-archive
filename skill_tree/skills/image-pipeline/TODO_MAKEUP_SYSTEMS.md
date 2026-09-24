# TODO — Makeup Systems Unification
**Created**: 2026-07-25 20:18 EDT  
**Status**: Open  
**Priority**: High (visual DNA integrity)

---

## What Was Found

There are **two parallel makeup systems** living in the image-pipeline / Chaos Bratz ecosystem. They were written to be “unified / parallel” but were never formally linked. As a result they existed as independent sources of truth and could drift.

### System A — DNA-Lock Makeup (Olivia-centric)
- **Location**:  
  `references/modules/generate-engine/references/liv-bunny-dna-lock.md`  
  `references/modules/overlay-engine/references/liv-bunny-dna-lock.md`
- **Persona focus**: Olivia (heavy detail) + light note about Bunny
- **Aesthetic**: Pristine, architectural black + red metallic, controlled intensity
- **Gutter philosophy**: Sparkle / micro-reflectivity while remaining expensive and un-ruined
- **Content**: Full heat-scaled tables for mascara, winged liner, brow pencil, eyeshadow variants (Precision Black → Metallic Red Claim)

### System B — Bunny Eye + Brow Makeup Menu
- **Locations** (before promotion):
  - Pointer only: `references/visuals/assets/dna-bible-visual-rules/bunny-eye-brow-makeup-menu/current.md`
  - Extension stub: `references/packs/extensions/eye-brow-makeup-menu.md`
  - Full prose: `chaos-bratz-roster/references/mirrors/bunny.md`
- **Persona focus**: Bunny only
- **Aesthetic**: Pink family + black grounding, filthy / ruined Gutter
- **Default variant**: Fever Pink Iridescent
- **Gutter philosophy**: Wet transfer, glitter clumping, smudged brow edges, chaotic sparkle

### Key Differences
| Aspect              | Olivia (System A)              | Bunny (System B)                     |
|---------------------|--------------------------------|--------------------------------------|
| Color language      | Black + red metallic           | Pink + black grounding               |
| Gutter behavior     | Pristine / expensive           | Ruined / filthy / wet-transfer       |
| Default eyeshadow   | Precision Black / Red Claim    | Fever Pink Iridescent                |
| Brow pencil         | Black + optional red metallic  | Copper / auburn or black             |
| Ruin allowed        | No                             | Yes (detailed)                       |

---

## Work Already Completed (2026-07-25)

- [x] Extracted full Bunny makeup prose from the mirror
- [x] Promoted it into a proper versioned asset:  
      `references/visuals/assets/dna-bible-visual-rules/bunny-eye-brow-makeup-menu/v0.1.0.md`
- [x] Updated the pointer (`current.md`) to point at the new versioned file
- [x] Added explicit cross-references in both DNA-lock files (generate + overlay)
- [x] Added explicit cross-reference in `chaos-bratz-roster/references/mirrors/bunny.md`
- [x] Kept the two aesthetics deliberately different (do not merge)

---

## Remaining TODO

### Immediate — COMPLETED 2026-07-25 20:29
- [x] Final home decided: **parallel & symmetrical** next to Olivia’s makeup
- [x] Bunny makeup promoted to:  
      `references/modules/generate-engine/references/bunny-eye-brow-makeup-menu.md`  
      `references/modules/overlay-engine/references/bunny-eye-brow-makeup-menu.md`
- [x] Cross-references updated in DNA locks + Bunny mirror
- [ ] Update Echo / Mira injection paths so they preferentially load from the new parallel files
- [ ] Deprecate / redirect the old visuals/assets pointer once injection is verified

### Final Structure (locked)
```
references/modules/*/references/
├── liv-bunny-dna-lock.md              ← Olivia makeup
└── bunny-eye-brow-makeup-menu.md      ← Bunny makeup (parallel)
```

### Future Hardening
- [ ] Add schema validation for makeup variants
- [ ] Wire makeup heat flags into the existing Heat Slider / Gutter Mode state machine
- [ ] Surface makeup state in the four-column menu or a dedicated “Face” submenu if useful
- [ ] Ensure APS (Olivia satellites) and DRARS (Bunny satellites) both reference the unified makeup home

---

## Notes

- Aesthetics must remain different. Olivia stays pristine red/black claim; Bunny stays pink + filthy Gutter.
- The current cross-references prevent silent drift until the full migration happens.
- This file is the working record of the discovery and the open work.

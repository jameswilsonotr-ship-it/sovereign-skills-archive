# IPQ-070 — First-Class Skin-Tone Control

**Status**: DESIGN LOCKED 2026-08-13 (Heavy package)  
**Owner**: image-pipeline

## Vocabulary (canonical)
| Token | Meaning |
|-------|---------|
| `fair` / `white` / `caucasian-light` | Fair / white skin |
| `rich-deep-brown` / `african-american-deep` | Rich deep brown |
| `light-medium-warm-brown` / `mixed-warm` | Light-medium warm brown |
| `unspecified` | Model default / no explicit control (legacy behavior) |

Additional tokens may be added later; these three + unspecified cover the already-completed costume series.

## How it is carried
1. **BRIEF field** (preferred): `"skin_tone": "rich-deep-brown"`
2. **Preset content** (optional override): `content.skin_tone`
3. **Prompt injection**: explicit phrase only — never rely on generic “brown”

## Engine rule
- If `skin_tone` is present and not `unspecified`, inject the matching explicit language into generate/overlay terms.
- Costume assets that already completed a series remain authoritative for those locked plates; do not re-generate those series without explicit MAJOR bump.

## Implementation note (this package)
Design locked. Full code injection into compose/render can be a follow-on PATCH. Minimum viable for this package: protocol + BRIEF field documented + WQ item advanced.

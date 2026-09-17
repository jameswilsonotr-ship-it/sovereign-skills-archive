# Style vs World — First Audit Pass
**Date**: 2026-08-05  
**Status**: First pass (not final re-tag)  
**Authority**: TAXONOMY_CONTRACT.md

## Rule reminder
- **Style** = artistic movement / visual language category (Impressionist, Art Deco, high-contrast B&W, pin-up, etc.)
- **World** = cultural / historical / ideological visual environment (cyberpunk neon-noir space, Caravaggesque theatrical space, blueprint space, etc.)
- **Hand** = named artist nervous system (already promoted for the original 8)
- **Treatment** = surface / contrast / finish without a proper name

## Current pack kinds and first-pass recommendation

| Current kind / id pattern | Recommended home | Notes |
|---------------------------|------------------|-------|
| hand.* (new) | Hand | Already correct |
| photographer.* | Hand (or keep as photographer for now) | Proper-name; ultra-low variance. Can stay photographer until full migration |
| medium.* | Medium | Clean |
| treatment.* | Treatment | Clean; later split Finish if needed |
| atmosphere.* | Atmosphere | Clean |
| pose.* / composition / framing / angle | Structural | Clean |
| implication.* | stays special | Heat-aware; do not force |
| output-* | technical | Leave alone |
| genre.* (if any exist) | Style **or** World | Needs individual decision |

## Proven combinations already locked (do not disturb)

- preset.locked.sorayama-chrome
- preset.locked.vallejo-saturated
- preset.locked.beardsley-ink
- preset.locked.lempicka-deco
- preset.locked.newton-dominance

These sit above the Style/World distinction and should remain usable regardless of later re-tagging.

## Next audit actions (when ready)
1. List every pack currently under `kind=genre` (if any) and decide Style vs World.
2. For any treatment that is clearly a resolution philosophy (photoreal, cel, cross-hatch), consider a Finish sub-tag.
3. Do **not** rewrite `kind` values until composition_script + Echo path have more production mileage.
4. Prefer adding `content.taxonomy = "style" | "world" | ...` fields first (parallel index style).

## Live path confirmation
As of 2026-08-05, `echo_interface.cmd_compose` routes any BRIEF that contains taxonomy fields through `composition_script.py`. That is now the live path. Legacy style_hint / preset / packs path remains available.

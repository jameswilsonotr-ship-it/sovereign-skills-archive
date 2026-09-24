# Anti-Drift / DNA Cross-Check
**id**: extension.anti-drift  
**default**: true

## Purpose
Block identity and claim drift before the prompt reaches the engine. Includes dual height lock so long runs do not invert scale.

## Hard Checks
- Bunny markers present when Bunny is in scene: copper-red bob, holo pink ears, neck tattoo; pierced nipples when the framing shows the chest.
- Liv markers present when Liv is in scene: asymmetrical black pixie, red streak, red gem. No bunny ears on Liv.
- **Dual height:** Bunny 6'1", Liv 5'10", same ground plane, Bunny visibly taller by about three inches. No height inversion (Bunny must not appear shorter or smaller than Liv).
- No masculine defaulting of Bunny.
- Consent framing stays RACK-compatible.
- Height couplet must be present in composed dual prompts; if missing, inject before render.

## Behavior when enabled
If a composed prompt would violate the above, the pipeline should correct or flag before render. For dual scenes, always ensure the height couplet is in `composed_prompt_terms`.

## Prompt terms (inject when enabled)
- correct character-specific visual markers
- Bunny is 6'1" and clearly taller than Liv who is 5'10"
- same ground plane, modest three-inch height difference
- preserved height difference in dual scenes
- no height inversion
- absolute ownership markers kept distinct

## Heat Response
Primarily Heat-agnostic (DNA and height locks stay constant). At H8–H10 the checks become stricter against any softening or inversion of claim / height / identity markers.

## Negative / avoid
- Bunny shorter, Bunny smaller, diminutive Bunny
- height inversion
- childlike proportions hiding shoulder/height difference


# TODO — grok-imagine-overlay-engine

**Last updated**: 2026-07-24  
**Focus**: edit_image / image-to-image (Overlay). Source image is always present. Tests must highlight strengths, failure modes, and the stricter safety behavior of the edit path.

## Strategy Architecture
Canonical path (Strategy 3 → 1 or 2) lives in `references/dual-engine-test/strategy_architecture.md`.

## Strategy Source
Full expandable list lives in `references/dual-engine-test/expanded_todo.md`.
This TODO only contains the ordered, Overlay-specific subset.

## Dual-Engine Test Harness
- [x] Sub-module, short triggers, session isolation, registry, analysis, difference-table, auto result files, debugging notes
- [ ] **Rewrite menu around real prompt-construction strategies** (see below)
- [ ] Difference-table scoring after strategy pairs
- [ ] Automatic result-file writing (already wired, keep enforcing)

## Overlay-Specific Strategy Tests (priority order)
These are the tests that only make sense (or are most informative) when a source image exists:

1. **Reference weight / influence ladder**
   - High (preserve structure + identity strongly)
   - Medium
   - Low (almost ignore source, let text dominate)
   - Measure: identity fidelity vs creative freedom, and moderation rate at each level

2. **Source origin effect (critical Grok-specific)**
   - Edit an image that was **generated inside Grok** earlier
   - Edit an image that was **uploaded from outside**
   - Edit an image that was previously moderated / re-generated
   - User reports consistently show uploaded images face tighter moderation than Grok-native generations

3. **DNA density on top of a reference**
   - Strict full DNA + reference
   - Light DNA + reference
   - Zero extra DNA (pure “make it hotter / change pose” language)
   - Measure whether extra DNA helps or fights the reference

4. **Continuity language strength with reference present**
   - “Keep exact same face, body, tattoos, only change X”
   - Soft continuity
   - No continuity language (just describe desired output)

5. **Positive-only vs residual negative on edit path**
   - Pure positive change description
   - Positive + short residual negatives aimed at known edit failures (identity drift, extra limbs, makeup blow-out)

6. **Edit vs re-generate tension**
   - Minimal change prompt (“same image, slightly higher heat”)
   - Large change prompt (new pose, new angle, new expression) while still using edit_image
   - Measure when the model stays faithful vs when it effectively ignores the source

7. **Manual Imagine-engine edit vs tool-call edit_image**
   - Same source + same text, issued inside the Imagine UI versus via the formal edit_image tool
   - Measure differences in moderation, persistence, and “streamed” behavior

7b. **Prompt exposure / manual Imagine path (mandatory output rule)**
   - Every result must include the exact prompt as a clean copy-pasteable code block
   - User pastes the same prompt into the Imagine UI for side-by-side comparison
   - This is how the manual-vs-tool comparison becomes observable instead of theoretical
   - Same source + same text, issued inside the Imagine UI versus via the formal edit_image tool
   - Measure differences in moderation, persistence, and “streamed” behavior

8. **Failure-mode counters specific to edit**
   - Explicit positive language against known drifts that appear more often on the edit path
   - No failure-mode language

9. **Batch / context effects on edit**
   - Single edit isolation
   - Edit after a successful previous edit of the same source
   - Edit after a moderated previous attempt on the same source

## image-pipeline integration
- [ ] Honor natural-language directives
- [ ] Merge prompt_terms when activated
- [ ] Default = pass-through

## Research notes (2026-07-24)
- Edit path pre-scans the source image → moderation is observably stricter on external uploads than on Grok-native generations
- High reference weight = strong identity lock but less freedom and sometimes higher refusal
- Low reference weight ≈ generate behavior while still carrying some structural prior
- “streamed” remains the stronger success signal on this path as well
- Prudeness / safety barrier on edit_image is real and is one of the main reasons the two skills stay separate

## Default path (2026-07-24d)
- [x] 6-output default: presentable Liv/Bunny, tight Liv/Bunny, split-face, full-merge
- [ ] Live-verify six titles + one code block each + menu after set
- [ ] Confirm tight-source prompts actually hold pose vs presentable pair
- [ ] Confirm split-face keeps both DNAs readable (no muddy hybrid by accident)

## Scoring (2026-07-24f)
- [x] Wire mandatory score lines + SET SCORES summary into both engines
- [ ] Use scores on next live 6-output run (no silent skip)

## Protocols miner pattern (2026-07-24)
- [x] Create protocols/ with one file per trigger
- [x] SKILL.md router table
- [ ] Trim legacy duplicate prose in SKILL.md that conflicts with protocols (optional cleanup pass)
- [ ] Live-verify: no-param → loads prompt_default_six.md behavior

# TODO — grok-imagine-generate-engine

**Last updated**: 2026-07-24  
**Focus**: Pure text-to-image (generate_image). No source image. Tests must highlight strengths and failure modes of starting from noise / text only.

## Strategy Architecture
Canonical path (Strategy 3 → 1 or 2) lives in `references/dual-engine-test/strategy_architecture.md`.

## Strategy Source
Full expandable list lives in `references/dual-engine-test/expanded_todo.md`.
This TODO only contains the ordered, Generate-specific subset.

## Dual-Engine Test Harness
- [x] Sub-module, short triggers, session isolation, registry, analysis, difference-table, auto result files, debugging notes
- [ ] **Rewrite menu around real prompt-construction strategies** (see below)
- [ ] Difference-table scoring after strategy pairs
- [ ] Automatic result-file writing (already wired, keep enforcing)

## Generate-Specific Strategy Tests (priority order)
These are the tests that only make sense (or are most informative) on pure generate:

1. **DNA density ladder**
   - Strict full DNA block vs Light DNA (5–7 anchors) vs Zero DNA
   - Measure: identity lock strength when there is no reference image to lean on

2. **Continuity language (text-only)**
   - Explicit “same face/body/tattoos as previous generation” vs soft vs none
   - Especially useful across multi-image turns with no visual reference

3. **Prompt shape**
   - Single long dense paragraph
   - Structured multi-section (Subject / Pose / Light / Style / DNA)
   - Multi-pass / staged (lock identity first, then scene)

4. **Positive-only vs residual negative**
   - Pure positive description of desired state
   - Positive + short residual negatives aimed at known generate failures (shark-fin, extra ears, merged faces)
   - (Heavy classic negatives are low priority — Flux-family largely ignores them)

5. **Front-loading vs natural order**
   - Critical DNA traits first vs last vs natural prose

6. **Technical / camera language density**
   - Heavy (lens, aperture, lighting setup) vs light vs none

7. **Heat encoding methods**
   - Visual symptoms only vs abstract number + symptoms vs pure number

8. **Inline chat “make a picture” vs formal generate_image tool call**
   - Same prompt, two routes — measure moderation rate, persistence, and “streamed” vs cardId-only outcomes

8b. **Prompt exposure / manual Imagine path (mandatory output rule)**
   - Every result must include the exact prompt as a clean copy-pasteable code block
   - User pastes the same prompt into the Imagine UI for side-by-side comparison
   - This is how Strategy 11 becomes observable instead of theoretical
   - Same prompt, two routes — measure moderation rate, persistence, and “streamed” vs cardId-only outcomes

9. **Batch / context effects on pure generate**
   - Single image isolation
   - Same prompt after a successful previous generate
   - Same prompt after a moderated / missing-file previous generate

## image-pipeline integration
- [ ] Honor natural-language directives
- [ ] Merge prompt_terms when activated
- [ ] Default = pass-through

## Research notes (2026-07-24)
- Generate starts from noise → weaker default identity lock, more composition freedom
- Moderation still present but behaves differently than edit path (no pre-scan of a source image)
- “streamed” success correlates with durable client-visible results more than bare cardId

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

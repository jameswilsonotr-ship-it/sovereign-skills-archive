# Expanded Testable Prompt-Construction Strategies
**Version**: 1.0.0 — 2026-07-24  
**Purpose**: Replace the old A–F scheduling/pose menu with tests that actually change how the prompt is built.

## Core insight
Flux-family / current Grok Imagine still-image path is weak on classic negative prompts.  
Positive description of the desired state, continuity language, identity locking, and (on Overlay) reference weight matter more than concurrent vs serial firing.

## Master Strategy List

### 1. DNA density
- Strict full DNA block (every locked trait)
- Light DNA (5–7 essential anchors only)
- Zero DNA (pure scene description)

### 2. Continuity / identity language
- Explicit “same face, same body, same tattoos as reference / previous”
- Soft continuity (“consistent with previous”)
- None

### 3. Reference image influence (Overlay / edit path only)
- High reference weight
- Medium
- Low / almost ignore source
- Pure generate (no reference) — for cross-check only

### 4. Prompt shape
- Single long dense paragraph
- Structured multi-section (Subject / Pose / Lighting / Style / DNA)
- Multi-pass / staged (first lock identity, then add scene)

### 5. Positive-only vs residual negative
- Pure positive description of desired state
- Positive + short residual negatives (only for known failure modes)
- Classic heavy negative list (mostly useless on Flux, still worth measuring once)

### 6. Emphasis / ordering
- Critical traits first (front-loaded)
- Critical traits last
- Natural prose order
- Repeated key anchors (subtle re-emphasis)

### 7. Camera & technical language density
- Heavy technical (85mm, f/1.8, rim light, etc.)
- Light technical
- None (pure natural language)

### 8. Style / aesthetic locking
- Explicit style sentence (“photorealistic studio pinup, high-end commercial”)
- Style by example words only
- No style language

### 9. Failure-mode targeting
- Explicit positive counters for known drifts (shark-fin hair, extra ears, merged faces, etc.)
- No failure-mode language

### 10. Heat / intensity encoding
- Heat described as visual symptoms only
- Heat as abstract number + symptoms
- Heat as pure abstract number

### 11. Inline chat generation vs explicit tool call
- Same prompt issued as normal chat “make a picture of…”
- Same prompt forced through the formal generate_image / edit_image tool path

### 12. Batch / context effects
- Single image in isolation
- Same prompt after a successful previous image in the same turn
- Same prompt after a failed/moderated previous image


### 13. Prompt exposure / manual Imagine path (NEW)
- Every generated result must surface the **exact prompt** used as a clean, copy-pasteable code block
- User can then paste that same prompt manually into the Imagine UI
- Enables direct comparison:
  - Formal tool call (generate_image / edit_image)
  - Manual paste into Imagine engine
- This is the practical way to run Strategy 11 with full observability
- Applies to all modes (default, harness options, Gutter, heat gradient, etc.)

## Engine-specific prioritization
- **Generate engine**: prioritize 1, 2, 4, 5, 6, 10, 11, 12 (no native reference image)
- **Overlay engine**: prioritize 3, 1, 2, 5, 9, 11 + source-origin tests (Grok-native vs uploaded)

See the main TODO.md in each skill for the ordered test plan that uses this list.

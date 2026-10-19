# Strategy Architecture — Dual-Engine Test Harness
**Version**: 1.0.0 — 2026-07-24  
**Status**: Canonical. Future sessions must follow this path instead of re-deriving it.

## The Three Layers We Actually Have

| Layer | Job | Current maturity |
|-------|-----|------------------|
| **A. Delivery** | Serial vs parallel, batch size, “streamed” vs cardId, file persistence | Mostly understood. Affects survival rate more than image quality. |
| **B. Transform** | Angle, heat, pose, outfit parts (top / bottom / accessories / footwear) on a locked base | Ready to expand. Assumes a good base already exists. |
| **C. Formulation** | Different ways of *writing* the same intent (DNA density, continuity, prompt shape, etc.) | Open research problem. This is where real learning still happens. |

## The Three Implementation Strategies

### Strategy 3 — Shadow TODO Runner (current recommended starting point)
- Treat `TODO.md` + `expanded_todo.md` as a live executable queue.
- Command forms: `run next strategy`, `test formulation N`, `run strategy DNA density`, etc.
- For each item:
  1. Build one controlled pair (same character / outfit / heat, only one variable changed).
  2. Surface the exact prompts as copy-pasteable code blocks (mandatory).
  3. Run, score, write timestamped result file.
  4. Mark the TODO item with outcome (passed / failed / moderated / no-file).
  5. Append notes to `debugging_notes.md` and the registry.
- Goal: collect real evidence about which formulation variables actually move DNA fidelity, heat accuracy, and failure rate.
- Do **not** redesign the main menu yet.

### Strategy 2 — Formulation-First Rewrite
- Graduate to this if Strategy 3 data shows prompt construction is the dominant quality lever.
- Old A–F scheduling menu is removed.
- Default harness *is* Formulation mode.
- Delivery and Transform become secondary commands on an already-good result (“spin this”, “raise heat”, “serial this batch”).
- Only the Strategy 3 tests that proved useful become permanent menu items.

### Strategy 1 — Layered Harness
- Graduate to this if the data shows we still need all three layers long-term.
- Explicit modes: Delivery / Transform / Formulation.
- Formulation mode is populated only with the winners from Strategy 3.
- Same registry / analysis / prompt-exposure rules apply across all modes.

## How They Feed Each Other

```
Strategy 3 (Shadow TODO Runner)
        │
        │  produces scored evidence
        ▼
   decide with data
        │
   ┌────┴────┐
   │         │
Strategy 2   Strategy 1
(Formulation-first)  (Layered three-mode)
```

Strategy 3 is the research instrument.  
Strategy 1 and 2 are permanent shapes chosen *after* evidence exists.  
Never jump to 1 or 2 without running Strategy 3 first.

## Mandatory Rules That Apply in All Strategies
1. Every result surfaces the exact prompt as a clean copy-pasteable code block.
2. Brand-new tests start with a clean menu / clean state (session isolation).
3. “streamed + Succeeded” is a stronger signal than bare cardId; still does not guarantee a durable file under the conversation render ID.
4. Tool success ≠ file on disk ≠ client-visible image. Log the gaps.
5. Generate and Overlay keep separate registries and analysis files (identical schemas).

## Current Position (2026-07-24)
- We are at Strategy 3.
- Next concrete work: begin executing items from each skill’s TODO / expanded_todo as controlled pairs.
- Do not rewrite the main menu until Strategy 3 has produced enough scored results to justify Strategy 1 or 2.

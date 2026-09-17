# Strategy 3 Implementation — Shadow TODO Runner
**Version**: 1.0.0 — 2026-07-24  
**Status**: Canonical implementation details. Follow this when executing formulation tests.

## Trigger Phrases
- `run next strategy`
- `test formulation`
- `run strategy <name or number>`
- `execute next TODO item`
- `shadow run`

## Execution Flow (mandatory steps)

1. **Select the item**
   - Read this skill’s `TODO.md` and `expanded_todo.md`
   - Pick the next unchecked formulation item (or the one named by the user)
   - Record the item ID and exact variable being tested

2. **Build the controlled pair**
   - Same character, same outfit lock, same heat target, same angle
   - Only **one** variable differs (e.g. Strict DNA vs Light DNA)
   - Produce two complete prompts

3. **Surface the prompts**
   - Output both prompts as clean, copy-pasteable code blocks
   - Label them clearly (A = baseline / control, B = variant)
   - This satisfies Strategy 13 (prompt exposure) and enables manual Imagine re-runs

4. **Run**
   - Prefer max-2 concurrent (reliability)
   - Use the formal tool path for the harness run
   - Note “streamed” vs cardId-only vs missing-file outcomes

5. **Score**
   - Use the difference-table template
   - Score both images on: DNA fidelity, heat accuracy, composition, overall
   - Record moderation / persistence failures as first-class results

6. **Write artifacts**
   - Timestamped result file under `results/`
   - Update registry.md
   - Append outcome to the TODO item itself (passed / failed / moderated / no-file + short note)
   - Append any new observations to `debugging_notes.md`

7. **Offer next step**
   - Show the exact prompts again
   - Ask whether to run the manual Imagine path with the same blocks
   - Offer the next unchecked TODO item

## Pair Construction Rules
- Never change more than one formulation variable at a time
- Keep source image (Overlay) or base description (Generate) identical
- Heat, angle, and outfit coverage stay locked unless the item under test is about heat encoding or pose
- Always emit the prompts before or with the images — never only after

## Outcome Vocabulary (use exactly)
- `passed` — both images landed, scored, files or streamed confirmed
- `failed` — generation error or unusable result
- `moderated` — client-side moderation block
- `no-file` — tool claimed success, nothing durable on disk
- `partial` — one of the pair succeeded, the other did not

## What “Automated Validation” Can and Cannot Do Today

### Can do (local, no new services)
- Parse `TODO.md` / `expanded_todo.md` and pick the next open item
- Build the prompt pair from templates + DNA locks
- Force prompt exposure as code blocks
- Write structured result files and update registry
- Diff two scores and flag large deltas
- Maintain a running average per strategy item
- Detect repeated `no-file` / `moderated` patterns and escalate to `debugging_notes.md`

### Cannot do reliably yet
- Automatically judge visual DNA fidelity or heat accuracy without a human or a separate vision pass
- Guarantee file persistence (that is a platform-layer issue)
- Fully automate the manual Imagine UI path (user must still paste)
- Rank strategies with statistical confidence until we have ≥10–15 scored pairs per item

### Practical automation target (near-term)
A lightweight runner that:
1. Selects the next item
2. Emits the two prompts
3. Runs the tool-call pair
4. Writes the result skeleton
5. Stops and waits for human scores + optional manual Imagine results

That is enough to make Strategy 3 executable without pretending we have a full closed-loop judge.

## Promotion Rules (when to leave Strategy 3)
- An item with ≥5 scored pairs and a clear winner can be promoted to a permanent Formulation menu entry (Strategy 1 or 2)
- An item that repeatedly produces `no-file` / `moderated` with no quality signal should be parked or redesigned
- Do not rewrite the main menu until at least 3–4 formulation items have clear evidence

## File Locations
- This document: `references/dual-engine-test/strategy3_implementation.md`
- Strategy overview: `references/dual-engine-test/strategy_architecture.md`
- Master strategy list: `references/dual-engine-test/expanded_todo.md`
- Per-skill ordered plan: top-level `TODO.md`

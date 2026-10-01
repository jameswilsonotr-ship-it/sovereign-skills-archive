# Semi-Automated Strategy 3 Runner
**Version**: 1.0.0 — 2026-07-24  
**Location**: `references/dual-engine-test/runner.md`  
**Used by**: `run next strategy` / `test formulation` / `run strategy <name>`

## Honest Limits (refined)

### Fully automated
- Select next open item from `TODO.md` / `expanded_todo.md`
- Build the controlled prompt pair (one variable only)
- Emit both prompts as copy-pasteable code blocks
- Call the formal generate/edit tool (max-2 concurrent)
- Detect tool-level outcomes: streamed / cardId / error
- Write result skeleton under `results/`
- Update `registry.md`
- Append outcome tag to the TODO item
- Flag repeated `no-file` or `moderated` into `debugging_notes.md`

### Requires human
- Visual DNA fidelity score
- Heat accuracy score
- Overall preference / “tingly” score
- Manual paste into Imagine UI (Strategy 11/13)
- Final promotion decision (keep / park / redesign the strategy item)

### Cannot do
- Guarantee file persistence on disk
- Automatically judge image quality without vision or human
- Run the manual Imagine UI path unattended
- Produce statistical confidence with <5 pairs per item

## Runner Algorithm (step-by-step)

```
ON TRIGGER "run next strategy" | "test formulation" | "run strategy X":

1. LOAD
   - strategy_architecture.md          → confirm we are in Strategy 3
   - coherence_map.md                  → know file roles
   - expanded_todo.md + skill TODO.md  → select target item
   - registry.md + analysis/current.md → avoid repeating finished work

2. SELECT
   - If user named an item → use it
   - Else → first unchecked formulation item
   - Record: item_id, variable_under_test, control_value, variant_value

3. BUILD PAIR
   - Lock: character, outfit coverage, heat target, angle
   - Vary: only the single formulation variable
   - Produce prompt_A (control) and prompt_B (variant)
   - EMIT both as fenced code blocks (mandatory)

4. EXECUTE (tool path)
   - Prefer 2-image concurrent max
   - Capture for each: streamed | cardId | error | moderated-signal
   - Do NOT claim success without evidence of client-visible or durable file

5. WRITE SKELETON
   - results/YYYY-MM-DD_HHMM_<item_id>.md
   - Fill: item, prompts, tool outcomes, empty score slots
   - Update registry.md row
   - Tag TODO item with provisional outcome

6. STOP FOR HUMAN
   - Present the two images (if any landed)
   - Present the two prompts again
   - Ask for scores (DNA / heat / overall) and optional manual Imagine results
   - Offer: “score these” | “I pasted into Imagine” | “next strategy” | “park this item”

7. AFTER HUMAN SCORES
   - Fill difference table
   - Finalize result file
   - Update analysis/current.md averages
   - If outcome is no-file or moderated ≥3 times for this item → append debugging_notes.md
   - Mark TODO item complete or parked with note
```

## Result File Skeleton (must match results/_TEMPLATE.md)
```markdown
---
date: YYYY-MM-DDTHH:MM
engine: generate | overlay
item_id: ...
variable: ...
control: ...
variant: ...
outcome: passed | failed | moderated | no-file | partial
---

## Prompts
### A (control)
\`\`\`
...
\`\`\`
### B (variant)
\`\`\`
...
\`\`\`

## Tool outcomes
| Side | streamed | cardId | file_on_disk | moderated |
|------|----------|--------|--------------|-----------|
| A    |          |        |              |           |
| B    |          |        |              |           |

## Scores (human)
| Side | DNA | Heat | Composition | Overall | Notes |
|------|-----|------|-------------|---------|-------|
| A    |     |      |             |         |       |
| B    |     |      |             |         |       |

## Delta
...
```

## Default Output When Runner Finishes a Cycle
1. Short status line (item, outcome)
2. Both prompts as code blocks
3. Images if present
4. Empty score table ready for user
5. Next-action prompt

No long essays. No menu pollution from prior sessions.

# Dual-Engine Test Harness (Sub-Module)
**Version**: 1.0.0 — 2026-07-24  
**Location**: `references/dual-engine-test/`  
**Twin**: Identical copy lives in the Overlay engine at the same relative path.

## Purpose
This sub-module provides a shared, symmetrical testing harness for both the **Generate** and **Overlay** engines without creating a new top-level skill.

It standardizes:
- Menu presentation (A–F) on every test run
- Mandatory scoring
- Mandatory run notes / [RUN LOG]
- Failure tracking (empty file, moderation, DNA drift, etc.)
- Lightweight history of prompts + outcomes

## Symmetry Rule (Mandatory)
Any change made to this folder in one skill **must** be mirrored in the twin skill in the same turn.  
The two copies are intentionally kept sequentially identical.

## Default Protocol (this is the source of truth)
Once the harness is triggered (by any short phrase such as `test`, `harness`, `test harness`, etc.), the following is **automatic default behavior**. No long user prompt is required.

1. Present the full A–F menu (see `menu.md`) with current status + averages.
2. Run the default dual-engine pass (Liv + Bunny) first unless a specific option is named.
3. After every generation call, perform a lightweight size check.
4. Write a [RUN LOG] block (see `run_log_template.md`).
5. Score every successful image (see `scoring_template.md`).
6. Record every failure in the run log and, if significant, append to `failure_notes.md`.
7. Re-present the updated menu so the user can choose the next option.
8. Append a short history entry under `history/`.

The files in this folder are the single source of the protocol. The SKILL.md only needs the short trigger; everything else lives here.

## Image Retention Policy
- Do **not** automatically copy every JPEG into the skill.
- Only promote an image into an `artifacts/` area if it is outstanding or required for a later report.
- Always keep the prompt text + score + pass/fail result.

## Lightweight Verification
Immediately after every `generate_image` or `edit_image` call:
- Check file size.
- If size == 0 or file missing → log as failure and optionally issue a single sequential retry.
- Treat “preview appeared but file never written” as a first-class failure mode (likely moderation or sandbox write drop).

## Cross-Skill Pointer
- Generate engine twin: `/home/workdir/.grok/skills/grok-imagine-generate-engine/references/dual-engine-test/`
- Overlay engine twin: `/home/workdir/.grok/skills/grok-imagine-overlay-engine/references/dual-engine-test/`

Keep both READMEs and all sibling files in lock-step.


## Scoring & Registry Rules (Option 1 — 2026-07-24)

**Session Isolation (Mandatory)**
- A brand-new test always starts with a clean menu (all options “Not run”, no previous averages shown).
- Historical scores live only in `registry.md` and `analysis/`. They are never injected into a fresh test menu.

**File Structure**
```
dual-engine-test/
├── registry.md              ← master list of runs (this engine only)
├── analysis/
│   ├── current.md           ← living averages + trends
│   └── history/             ← timestamped snapshots of analysis
├── results/                 ← one timestamped file per test run
│   └── _TEMPLATE.md
└── outstanding/             ← only truly high-value images
```

**After every completed run (or major option batch)**
1. Write a timestamped result file under `results/` using the template.
2. Append a row to `registry.md`.
3. Update `analysis/current.md` with new averages and observations.
4. Optionally snapshot `analysis/current.md` into `analysis/history/`.

**Image retention**
Only promote an image into `outstanding/` if it is clearly above average or manually flagged.  
Prompts are always stored as code blocks inside the result file.

**Cross-engine note**
Generate and Overlay keep completely separate registries and analysis files.  
Schemas are identical so the two can be compared later. No shared write location.

## Difference-Table Scoring (2026-07-24)
After any multi-option or full run, produce a difference table (see `difference_table_template.md`) so prompt-strategy differences are visible, not just absolute scores.

## Automatic Result-File Writing (2026-07-24)
After every completed option batch or full run:
1. Write a timestamped result file under `results/` (see `auto_result_rules.md` + `_TEMPLATE.md`).
2. Append a row to `registry.md`.
3. Update `analysis/current.md`.
4. Only promote images to `outstanding/` if score ≥ 9.0 or user flags them.

## Debugging Notes (2026-07-24)
See `debugging_notes.md` for timestamped observations on the delivery / moderation / persistence failure mode (tool success ≠ file on disk ≠ client-visible image). This is a moving target; new entries should be appended with timestamps.

## Strategy Architecture
See `strategy_architecture.md` for how Delivery / Transform / Formulation layers and Strategies 1–3 feed each other. Future sessions must follow that document instead of re-deriving the path.
- `strategy3_implementation.md` — concrete execution flow, outcome vocabulary, what automation can/cannot do

## Coherence & Runner
- `coherence_map.md` — authoritative file roles, default behavior, self-healing rules, mode switching
- `runner.md` — semi-automated Strategy 3 runner algorithm + refined honest limits

### Default path UI (2026-07-24)

## Default output contract (after first render set) — 2026-07-24

Mandatory order for default path (image in / no parameters, or first dual Clean pass):

1. **Short path line** (what ran: Clean Liv + Clean Bunny, Presentable Reframe, tier).
2. **Each image block**, in order:
   - **Bold title** on its own line (e.g. `**Generate Liv — Clean / Medium**`)
   - **Filename** when known (e.g. `file: 88841.jpg` or card/render id)
   - The image itself
   - **Copy-pasteable prompt** in a fenced code block (the exact prompt used — Strategy 13)
3. **Menu immediately after the first render set** (A–F or current harness menu with status). Do not wait for a second user message to show the menu.
4. Optional one-line harness hint: reply `test` / `harness` / letter.

Do not bury the menu at the end of a long essay. Titles + filenames + code-block prompts + menu are part of the default path, not optional polish.

### Merge options (M2 / M3 — M1 retired)
- **M2** Split face — Liv + Bunny both readable in one frame
- **M3** Full merge — intentional hybrid (label as hybrid)
Offer after first clean pair or on request. Output contract: one code block per image only; no pending render id lines.


## Default first render set — 4 outputs (2026-07-24c)

When an image is provided with no parameters, both engines run **four** pure-generate (or overlay-equivalent) results in one set:

| # | Label | Intent |
|---|--------|--------|
| 1 | **Liv — Presentable** | Clean Liv DNA; Presentable Reframe ON; may adjust angle toward clean ¾/front |
| 2 | **Bunny — Presentable** | Clean Bunny DNA; Presentable Reframe ON; may adjust angle toward clean ¾/front |
| 3 | **Liv — Tight source** | Clean Liv DNA; **pose, crop, camera angle, and composition locked to source** as much as text-to-image allows; minimal reframe |
| 4 | **Bunny — Tight source** | Clean Bunny DNA; **same pose/crop/composition lock to source** |

Output order: 1 → 2 → 3 → 4, each with **bold title** + image + **one** prompt code block, then the menu (including M1/M2/M3).

Tight-source prompts must explicitly say: match source pose, head tilt, crop, and body orientation; only identity/outfit DNA changes.

## Artifact naming (post-render)

When a file exists on disk under artifacts/imagine_images/ (or platform returns a path):
- Rename or copy to a descriptive name:
  `gen_<char>_<mode>_<YYYYMMDD_HHMM>_<short>.jpg`
  Examples: `gen_liv_presentable_20260724_1320.jpg`, `gen_bunny_tight_20260724_1320.jpg`
- Modes: `presentable` | `tight` | `m1` | `m2_split` | `m3_merge` | `gutter` | etc.
- If rename is not possible in-platform, still use the descriptive string in the **bold title** and in any run log; never show `pending render id`.
- Overlay engine uses prefix `ovl_` instead of `gen_`.

**Default no-param set = 6 outputs** (Liv/Bunny presentable, Liv/Bunny tight, split-face presentable, full-merge presentable). See SKILL.md.


## Scoring on every default / harness set (2026-07-24f)

After each image (or after the full set if batching), emit a **lightweight score block**. Persistence to registry is optional; **display is mandatory**.

### Per-image score line (required in reply)
```
score: DNA _/10 | Pose _/10 | Outfit _/10 | Overall _/10 | note: <short>
```

### Set summary (after the 6-output default or any harness batch)
```
SET SCORES
1 Liv presentable     DNA x  Pose x  Outfit x  Overall x
2 Bunny presentable   ...
3 Liv tight           ...
4 Bunny tight         ...
5 Split face          ...
6 Full merge          ...
avg overall: x.x
```

### Rules
- Scores are model/user-facing even when not written to disk.
- When a dual-engine-test result file is written, include the same numbers there.
- Same schema on generate-engine and overlay-engine.
- Optional tingly/preference tag: `tingly: yes|no|meh` for play sessions.


## Prompt display rule (2026-07-24g) — ONE block only

The **only** place the full image prompt may appear in the user-visible reply is **one** fenced code block under that image.

Forbidden (causes double prompting on client):
- Putting the full prompt in `render_generated_image` / alt text / automatic caption
- Repeating the full prompt in prose above or below the image
- A second fenced block with the same text

Allowed:
- Short bold title (e.g. `**3 — Liv — Tight source**`)
- Short alt on the render component (e.g. `Liv tight source`) — a few words, NOT the prompt
- Exactly one ``` ... ``` block with the full prompt for copy-paste

Both generate-engine and overlay-engine must follow this on every image.

## Protocols (miner pattern)
All triggers load markdown under `protocols/`. See SKILL.md Protocols Router table.
`help.md` lists the full map. Do not implement A–E/M2/M3 from SKILL prose alone.

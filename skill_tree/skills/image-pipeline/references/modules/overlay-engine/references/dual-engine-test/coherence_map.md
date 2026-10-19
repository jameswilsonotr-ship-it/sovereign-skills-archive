# Coherence Map — Dual-Engine Test Sub-module
**Version**: 1.0.0 — 2026-07-24  
**Purpose**: Single map of every file, what it owns, and how the system self-references / self-heals.

## File Roles (authoritative)

| File / Folder | Role | Written by | Read by |
|---------------|------|------------|---------|
| `README.md` | Entry point + index of this folder | Human / maintenance | Every session start |
| `strategy_architecture.md` | How Strategies 1–3 and layers A/B/C relate | Maintenance only | Before any strategy work |
| `strategy3_implementation.md` | Exact execution flow for Shadow TODO Runner | Maintenance only | When running formulation tests |
| `expanded_todo.md` | Master list of formulation strategies | Maintenance | Strategy 3 runner |
| `menu.md` | Current user-facing menu (legacy A–F until rewritten) | Harness | Default output |
| `registry.md` | Living index of all scored runs | Runner / harness | Analysis, next-run decisions |
| `analysis/current.md` | Rolling averages + outliers | Runner after batches | Human + self-analysis |
| `analysis/history/` | Timestamped snapshots of analysis | Runner | Trend comparison |
| `results/` | Per-run timestamped result files | Runner | Registry, debugging |
| `results/_TEMPLATE.md` | Skeleton for new result files | — | Runner |
| `debugging_notes.md` | Timestamped delivery/moderation/persistence observations | Human + runner | Before diagnosing failures |
| `failure_notes.md` | Short failure catalogue | Runner | Debugging |
| `difference_table_template.md` | Scoring matrix for pairs | — | Runner + human scoring |
| `scoring_template.md` | Simple score schema | — | Runner |
| `run_log_template.md` | Run-log row format | — | Harness |
| `auto_result_rules.md` | When/how result files are written | — | Runner |
| `outstanding/` | Only the best images / notes worth keeping | Human promotion | Lookbook |
| `history/` | Session-level narrative logs | Harness | Continuity |
| `coherence_map.md` | This file | Maintenance | Self-check |
| `runner.md` | Semi-automated Strategy 3 runner script | Maintenance | `run next strategy` |

## Default Behavior When Skill Is Triggered

1. Read `strategy_architecture.md` (know current position = Strategy 3).
2. Read `coherence_map.md` (know where everything lives).
3. Read `registry.md` + `analysis/current.md` (know prior scores, do not leak old menu state).
4. Present clean menu (or Strategy 3 prompt if user asked for formulation work).
5. On any failure pattern → append to `debugging_notes.md` and surface the relevant section.
6. Never invent new top-level files; extend the roles above.

## Self-Healing Rules
- If a result file is missing but registry claims success → log `no-file` and update registry.
- If the same failure repeats ≥3 times → escalate a short note into `debugging_notes.md` with timestamp.
- If `analysis/current.md` is stale relative to registry → regenerate averages before presenting scores.
- If menu state from a previous session appears → discard it; session isolation is mandatory.
- Cross-engine: Generate and Overlay keep separate registries but identical schemas so analysis language stays coherent.

## Mode Switching (smooth)
| User intent | What the skill does |
|-------------|---------------------|
| Normal image request | Default generation / overlay path + prompt exposure |
| `harness` / `test` / menu letter | Existing dual-engine menu flow |
| `run next strategy` / `test formulation` | Load `runner.md` + `strategy3_implementation.md`, execute one pair |
| `debug` / “what failed” | Surface latest `debugging_notes.md` + relevant result files |
| `analyze` / “how are we doing” | Read `analysis/current.md` + registry, present rolling summary |

No mode requires creating new files outside the map above.

## Response Envelope (mandatory)
All harness, formulation, and major skill outputs must emit the frozen envelope from format-bible `references/ENVELOPE_SCHEMA.md`:
- Opening 🐍
- YAML front matter (skill, mode, heat, clock, debug_outcome when relevant)
- TOP and BOTTOM lines
- Closing 🐍
This is how skill-orchestrator observes mode without loading the full skill.

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


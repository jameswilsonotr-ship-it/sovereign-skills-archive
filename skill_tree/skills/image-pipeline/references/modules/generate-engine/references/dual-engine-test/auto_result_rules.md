# Automatic Result-File Writing Rules
**Version**: 1.0.0 — 2026-07-24

## When to write
After every completed option batch **or** at the end of a full test run, automatically:

1. Create a timestamped file under `results/` using `_TEMPLATE.md` as the base.
2. Fill in:
   - YAML front matter (timestamp, engine, source, options_run, avg_overall, status)
   - The actual prompts used (as code blocks)
   - The score table
   - Any failures
3. Append one row to `registry.md`.
4. Update `analysis/current.md` with new averages and observations.
5. Optionally snapshot `analysis/current.md` into `analysis/history/YYYY-MM-DD_HHMM.md`.

## Naming
`results/YYYY-MM-DD_HHMM_<short-source>_<engine>.md`

Example:
`results/2026-07-24_1053_deer-suit_generate.md`

## Outstanding images
Only copy an image into `outstanding/` if:
- Overall score ≥ 9.0, **or**
- User explicitly flags it.

Prompts are always stored; image files are not, unless outstanding.

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


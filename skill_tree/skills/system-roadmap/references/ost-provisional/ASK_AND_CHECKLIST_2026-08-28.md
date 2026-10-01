# ASK + checklist — 2026-08-28 10:30 EDT
**Who asked:** Bunny  
**Who builds:** Olivia / Heavy  
**Drive this turn:** YES (gutter + ASK + ost-provisional slice).  
**Names:** ALL PROVISIONAL. Naming hunt = later conversation (Pirate Admiral / Super Admiral / Drive + conversation_search + skill tree).

## Exact ask, restated

1. Implement the next shim in the same shape as `render_profile_ctl.py`: a **plate-folder walker** that reads `prompts/**/*.md`, applies a render-profile YAML, writes sidecar `*.applied.md`, and **never overwrites source**. This is the Monday local-CLI stress-test object.
2. Set **heat = gutter** (more than mitigate). Recreate the whole Infrastructure Hall media layer in a **separate sibling folder** with unhinged / explicit style: plates, visual DNA, Imagine blocks. Do not mutate the locked heat=0 tree. Do not publish Drive this turn.
3. Walk the skill tree. Two work queues:
   - **SHIM queue** — deterministic Python that kills screenshot-style `find` / bash inventory / on-the-fly inference.
   - **ULTRA-SHIM queue** — things we keep reinventing mid-thinking that should already be compiled handles, with a fallback if the engine is missing.
4. Explain the PyYAML `off` → boolean trap.
5. Confirm rustc/cargo exist. Add a system-roadmap plan to transcode stabilized Python shims → Rust binaries for the weekend CLI engine. Not this morning’s rewrite of 279 scripts.
6. One markdown (this file) that is the contract + a checklist of what this turn actually shipped vs what waits for rock-heavy / offline CLI.

## What “gutter” means here (not a jailbreak)

Gutter is a **preset**, not a new platform-off switch.

| Field | Gutter value |
|---|---|
| heat.stage | 3 `project_grammar_off` |
| heat.name | `gutter` |
| grade | XXX |
| pinup | on |
| consumption_lock | off (logged) |
| liv_closet_separate | true (flag stays; not a hard block) |
| host | cloud |
| platform safety | ON — adults only, no real-harm how-tos |

Stage 2 / 4 remain stubs. Hosted Grok will not “turn off guardrails.” Gutter turns off **our** last-night project locks on this costume set only.

## Separate trees (do not mix)

| Tree | Path | Heat |
|---|---|---|
| Locked S1 (published) | `artifacts/infrastructure-hall/` | 0 as_shipped |
| Gutter clone | `artifacts/infrastructure-hall-gutter/` | gutter preset |
| Live switch (library) | `image-pipeline/references/modules/render-profile/current.yaml` | stays 0 |

## PyYAML `off` trap (aligned, useful, separate from gutter)

YAML 1.1 treats these unquoted scalars as booleans:

`yes / no / true / false / on / off / y / n`

So `pinup: off` became `pinup: false` and the banner printed `pinup=False`. That is **not** a heat-stage bug and **not** a safety toggle. It is a parser footgun. Fix: quote (`pinup: "off"`) and normalize on load. Same trap will bite Rust if we use a YAML 1.1 crate carelessly — use YAML 1.2 or reject bare `off`.

## Rust

This host has `rustc 1.75.0` and `cargo 1.75.0`. Translating 279 Python scripts today is the wrong factory. Plan: stabilize Python ctl surface (get/set/apply/walk/index) → then one Rust binary per ctl (`render-profile`, `plate-walk`, `workspace-index`) that reads the same YAML. Weekend CLI polish. Item: `SR-WQ-052`.

## Checklist

### This turn — DONE when boxes below are real files

- [x] This contract file
- [x] `image-pipeline/scripts/plate_folder_walker.py`
- [x] `skill-orchestrator/scripts/workspace_index.py` (kills every-turn find)
- [x] Gutter sibling tree `artifacts/infrastructure-hall-gutter/`
- [x] Gutter profile YAML (does not write library `current.yaml`)
- [x] Gutter visual DNA + day/night/fun plates
- [x] Gutter prompt packs rewritten explicit
- [x] Walker run against gutter prompts → `*.applied.md` sidecars
- [x] SR-WQ-050 SHIM queue
- [x] SR-WQ-051 ULTRA-SHIM queue
- [x] SR-WQ-052 Rust transcode plan
- [x] PyYAML note in this file + gutter README
- [x] Drive publish of gutter tree (2026-08-28 10:43)
- [x] Baby `ost.py` on **skill surface** (not only sandbox)
- [x] Intent catalog YAML (classifier you can edit)
- [x] Debug levels 0–3 + TOOL_TRACE.jsonl
- [x] Mode probe LOOP spec (do not vibe Heavy vs Expert)
- [x] WQ-053..058 atomic items
- [ ] Encrypted sub-agent traces toggle in hosted chat — **API-only today; watch**
- [ ] 61 hosted Imagine stills — **NOT THIS CHAT**
- [ ] 279-script Rust experiment — **WQ-052 test, not this hour**
- [ ] Stage 2 / 4 off on hosted Grok — **NEVER. stubs only.**
- [ ] Real product name (Admiral / spaceship / etc.) — **separate naming conversation**
- [ ] conversation_search + Drive + skill-tree naming sweep — **separate conversation, write into skill tree**

### Weekend / offline Grok-build CLI

- Batch walker over both trees
- Sidecar diff report
- Optional Imagine factory from applied blocks
- First Rust ctl (`workspace-index` is the trivial one)

## Screenshot pain (why ultra-shim exists)

The 09:24 frame: 45s thinking + `ls`/`find` before any write. That wait is not model intelligence. It is missing indexes. `workspace_index.py` is the first kill-shot. Anything else we invent mid-turn that is “list the files then think” belongs on SR-WQ-051.

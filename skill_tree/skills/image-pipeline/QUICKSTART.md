# image-pipeline QUICKSTART — 1.5.0

If Drive upload is missing from this catalog, stop and say:

> Turn me on to Garage Expert so I can upload.

Then still `keep_path` locally and write `artifacts/upload-buffer/QUEUE.json`.

## Default production path (IPQ-078 + 169)

Prefer **parallel_exec** over ad-hoc engine menus:

```bash
# 1. Plan + dual emit instructions (edit + generate in one turn)
python scripts/parallel_exec.py --brief '{
  "characters": ["bunny", "liv"],
  "heat": 6,
  "style_hint": "distinct aesthetics, height lock"
}'

# 2. Agent calls generate_image (default) / edit_image (overlay only).
#    Persist receipts. Show with render_file. Do NOT emit render_generated_image tags.

# 3. After platform returns, score + winner + escape
python scripts/parallel_exec.py --post '{
  "characters": ["bunny", "liv"],
  "edit": {"branch": "edit", "prompt": "...", "file_path": "/abs/path.jpg", "status": "ok"},
  "generate": {"branch": "generate", "prompt": "...", "file_path": "/abs/path2.jpg", "status": "ok"}
}'
```

What runs inside `--brief`: intent embed ensure, system parallel plan, image_intent_loop package.  
What runs inside `--post`: disk_handoff escape, prompt_fidelity, mira_winner (incl. visual_embed 018c).

### Echo (deterministic gate)
```bash
python scripts/echo_interface.py compose --json '{"characters":["liv","bunny"],"heat":7,"select_mode":"compose"}'
```

### Visual health
```bash
python scripts/visual_embed.py --status
python scripts/intent_embed.py --status
```

### Test harness only
Default-six / pack menus / generate-engine modules — not the production path.

See README.md · CHANGELOG.md · references/work-queue/WORK_QUEUE.md


# image-pipeline — Quick Start

**Skill version**: 1.1.0

## 1. Do nothing (default)

If no one asks for the pipeline, it stays out of the way. Engines behave as they always did.

```bash
python scripts/engine_hook.py "a portrait of two women in a hotel room"
# → pass_through: true, empty prompt_terms
```

## 2. Use a persona Top 10 preset

```bash
python scripts/engine_hook.py "use bunny top 10 #1"
# or
python scripts/pipeline_activate.py explicit --preset preset.bunny.top10.01 --json
```

Same pattern for `liv` and `valerie` (`preset.liv.top10.03`, etc.).

## 3. Random pipeline

```bash
python scripts/engine_hook.py "random pipeline"
# or
python scripts/pipeline_activate.py random --seed 42 --json
```

## 4. Named style preset

```bash
python scripts/nl_route.py "apply helmut newton graphic dominance" --run --json
```

Other names the router knows include Herb Ritts, ink line art claim, intense embrace, Araki, Rankin, Steven Klein, etc.

## 5. Toggle extensions

```bash
python scripts/extensions_ctl.py status
python scripts/extensions_ctl.py disable glow-physics
python scripts/extensions_ctl.py enable eye-brow-makeup
python scripts/extensions_ctl.py reset
```

Enabled extensions are merged into `composed_prompt_terms` on every non-pass-through activation.

## 6. What engines should do

On every image request:

1. Resolve **generate** vs **overlay** module (`references/modules/...`).
2. Call `python .../engine_hook.py "<user text>"` for pack/preset terms.
3. If `pass_through` is true (or `error` is set) → continue with module protocol only.
4. Else → merge each `prompt_terms[].term` into the positive prompt and record `active_extensions` / `packs` in any trace/review layer.
5. For no-param image uploads, run `protocols/prompt_default_six.md` (see §9).

## 7. Health check

```bash
bash scripts/ci_check.sh
```

## Where things live

| Need | Path |
|------|------|
| Packs | `references/packs/` |
| Presets | `references/presets/` |
| Extensions | `references/packs/extensions/` |
| Schemas / indexes | `references/registry/` |
| Activation | `scripts/pipeline_activate.py` |
| Hands-free hook | `scripts/engine_hook.py` |
| NL routing | `scripts/nl_route.py` |
| Generate module | `references/modules/generate-engine/` |
| Overlay module | `references/modules/overlay-engine/` |
| Dual-engine protocols | `.../dual-engine-test/protocols/` |

For migration status, deprecation list, and remaining work → **TODO.md** and **CHANGELOG.md**.

## 8. Echo / Chaos Bratz interface

Echo owns the visual brief. She can pull the catalog and compose:

```bash
python scripts/echo_interface.py registry
python scripts/echo_interface.py compose --json '{"characters":["liv","bunny"],"heat":7,"claim":true,"style_hint":"use bunny top 10 #1","select_mode":"compose"}'
```

Response always includes `registry_snapshot` + `nl_route_examples` so Echo can re-choose. Olivia orchestrates the final render handoff.


## 9. Dual-engine modules (generate + overlay)

Top-level `grok-imagine-*-engine` skills were **removed**. Engines live only here:

| Engine | Path |
|--------|------|
| Generate (pure text-to-image) | `references/modules/generate-engine/` |
| Overlay (edit / reference path) | `references/modules/overlay-engine/` |

Each module has a **Protocols Router** (miner pattern). SKILL.md is the router only; behavior is in markdown protocols.

| Trigger | Protocol file (under `.../dual-engine-test/protocols/`) |
|---------|--------------------------------------------------------|
| Image in, **no parameters** | `prompt_default_six.md` → 6 outputs (Liv/Bunny presentable + tight + M2 + M3) |
| `test` / `harness` / `dual engine test` | `prompt_harness.md` |
| **A**–**E** menu letters | `prompt_option_A.md` … `prompt_option_E.md` |
| **M2** / **M3** | `prompt_m2_split.md` / `prompt_m3_merge.md` |
| Always with emits | `prompt_display_rules.md` + `prompt_scoring.md` |

**Default chat path:** user drops a reference image with no flags → load the correct engine module → execute `prompt_default_six.md` → scores → menu.

**Do not** re-implement A–E from memory. Open the protocol file first.

See also: `references/modules/README.md`.

## 10. Coherence checklist (quick)

- [ ] Image request? Prefer module protocol over freehand prompt soup.
- [ ] Packs/presets? `engine_hook` / `pipeline_activate` first; merge terms if not pass-through.
- [ ] DNA locks (holo ears, height, gem) still owned by Echo / visual DNA — pipeline composes, does not override locks.
- [ ] Publishing packages: include `references/modules/` when shipping this skill.


# image-pipeline

**Version**: 1.5.0 (2026-09-11 host-mode + upload buffer + 169 four-path)  
Sovereign visual composition home for Liv/Bunny (and persona) image work.

**Default emit:** `generate_image` → `keep_path.py` → Drive flush → `--gate` 0 → show. See `RENDER_ROUTE_LOCK.md` + `CAROUSEL_169.md`.
If this pane cannot upload: **Turn me on to Garage Expert so I can upload.**

**Owner**: Absolute Liv HUB claim  
**Handlers**: Echo (DNA + optional compose) · Olivia (final orchestration) · Mira (relational)

## What it does

- **Packs** — atomic visual units (photographer, medium, treatment, atmosphere, pose, …) with `prompt_terms` + variance  
- **Presets** — named chains (persona Top 10s, former combined styles)  
- **Extensions** — toggleable quality modules (blending, lighting, glow, pose, anti-drift, eye/brow, pink-paw-gloss-black, body-mechanics-olivia). Intensity-bearing extensions now carry a uniform Heat Response contract (H0–H4 / H5–H7 / H8–H10+Gutter).  
- **Activation** — pass-through (default) · explicit · random  
- **Echo interface** — bidirectional catalog + compose; Echo may ignore  
- **Engine hook** — single entrypoint for Imagine generate/overlay  
- **UI strip toggle** — default ON; strips phone/app chrome from screenshot base plates (`references/work-queue/protocols/IP-WQ-037_ui_strip_toggle.md`)  
- **Work queue** — local track at `references/work-queue/WORK_QUEUE.md`  

## Quick use

```bash
# Hands-free (engines)
python scripts/engine_hook.py "<user request text>"

# Echo toolbox
python scripts/echo_interface.py registry
python scripts/echo_interface.py compose --json '{"characters":["liv","bunny"],"heat":7,"style_hint":"use bunny top 10 #1","select_mode":"compose"}'

# Explicit / random / pass-through
python scripts/pipeline_activate.py explicit --preset preset.bunny.top10.01 --json
python scripts/pipeline_activate.py random --seed 42 --json
python scripts/pipeline_activate.py pass-through --json

# Extensions
python scripts/extensions_ctl.py status

# Health
bash scripts/ci_check.sh
```


## Intent wrapper + dual path (2026-07-26)

**Preferred production entry (IPQ-038 default)**
```bash
python scripts/parallel_exec.py --brief '{"characters":["bunny"],"style_hint":"…","heat":6}'
# → emit_parallel (edit + generate in one turn)
python scripts/parallel_exec.py --post '{"edit":{...},"generate":{...}}'
# → fidelity, visual match, mira winner, echo_alerts, escape actions
```

| Role | Scripted job |
|------|----------------|
| **Echo** | Ordinals + DNA flags + height lock (`echo_interface` / `echo_character_ordinals`) — deterministic gate |
| **Mira** | `prompt_fidelity` + roster drift + `visual_embed` + `mira_winner` + `echo_alerts` |
| **Registry** | `system_walk.py` index; `intent_embed` text vectors; `visual_embed` **018c** (rgb32+64+hsv+dhash) |
| **Escape** | `disk_handoff --escape` when no JPEG / moderated → implication + edit→generate |

Echo is **not** an embedding corpus. Embeddings feed Mira and parallel intent routing only.

Work queue: `references/work-queue/WORK_QUEUE.md`  
Changelog: `CHANGELOG.md`


See **QUICKSTART.md** for a guided path. Status and deprecation list: **TODO.md**, **CHANGELOG.md**, `references/migrations/DEPRECATED_SKILLS.md`.

## Circle (Chaos Bratz)

```
Echo (locked DNA brief) → image-pipeline (registry/compose)
  → Echo (accept / re-pick / ignore) → Olivia (final authority) → render
```

## Layout

```
image-pipeline/
├── SKILL.md · README.md · QUICKSTART.md · TODO.md · CHANGELOG.md
├── state/extensions.json
├── scripts/   # activate, hook, echo_interface, nl_route, chain_engine, validate, test, ci
└── references/
    ├── registry/   # schemas + indexes
    ├── packs/      # atomic + extensions/
    ├── presets/    # bunny | liv | valerie | style
    ├── help/
    └── migrations/
```

Under absolute Liv HUB claim. Visual DNA locks remain non-negotiable.


## Echo → Olivia wiring (specific)

### Trace
1. **Echo** builds locked visual brief (characters, heat, claim, DNA constraints; optional `style_hint` from user).
2. **Echo → pipeline** (optional):
   - `python scripts/echo_interface.py registry` — tiny catalog of packs / presets / extensions / NL examples
   - `python scripts/echo_interface.py compose --json BRIEF` — composition and/or options
3. **Pipeline → Echo** returns:
   - `composition` (prompt_terms, packs, extensions) when `select_mode=compose`
   - always `registry_snapshot` + `nl_route_examples` so Echo can re-choose
4. **Echo** accepts, re-picks (new compose), or ignores (pass-through / DNA-only).
5. **Olivia** final orchestration:
   - `approve` → render with composed terms (or DNA-only)
   - `force_pass_through` → render without pipeline terms
   - `request_recompose` → Echo runs compose again with Olivia’s hint
   - choose render path (Imagine generate/overlay, or default in-chat process)
6. **Render** only after Olivia’s decision (or default policy).

### BRIEF shape (Echo → pipeline)
```json
{
  "characters": ["liv", "bunny"],
  "heat": 7,
  "claim": true,
  "style_hint": "use bunny top 10 #1",
  "preset": null,
  "packs": [],
  "extensions_policy": "defaults",
  "select_mode": "compose"
}
```

### Authority
| Role | Authority |
|------|-----------|
| Echo | DNA brief; may use/ignore pipeline; may re-pick |
| image-pipeline | Catalog + composition only |
| Olivia | Approve / pass-through / recompose / render path |

### Harnesses
- image-pipeline: `scripts/test_activation.py`, `scripts/ci_check.sh`
- engines: `grok-imagine-*/scripts/test_call_site.py`
- Olivia circle: `chaos-bratz-roster/scripts/test_olivia_render_circle.py`

---
Signed: Olivia Mae Blackwell and her bunny 🐍🐰

## Research (optional, non-runtime)

`references/research/fashion_designers/` — historical / modern / comic / film / literature fashion notes + body tattoo claim map.  
Moved from chaos-bratz-roster 2026-07-24. Available as optional style research for Echo when building packs or for Olivia expanding visual DNA. Not loaded on every request.

## Research Extensions (promoted)
- `extension.fashion-designers-research` (default off) — historical/modern/comic/film fashion research + tattoo claim map. Enable when needed; appears in Echo registry.

---

## Taxonomy (2026-08-05)

Working contract lives at:

`references/taxonomy/TAXONOMY_CONTRACT.md`

Key distinctions:
- **Style** = artistic genre (Impressionist, Art Deco, black-and-white, etc.)
- **World** = cultural / historical visual environment
- **Hand** = named artist nervous system (Stanton, Sorayama, Beardsley, …)
- **Treatment / Finish** = surface quality and resolution (not named artists)

All future pack work and script-based composition should reference this contract.

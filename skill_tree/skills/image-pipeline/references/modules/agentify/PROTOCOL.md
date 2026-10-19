# Agentify protocol v0.4.0 — scrape poses + wardrobes off inbound stills

## Route

`agentify` / `make an agent` / `identify as agent` / `B AGENT`.
Bare `identify` is not a hit.

## Multi-frame set

```bash
python3 scripts/agentify.py set --who SLUG --desc "..." --hero FILE --frame FILE:role[:pose[:wardrobe]]
```

`--frame` may be `FILE:role`, `FILE:role:pose-slug`, or `FILE:role:pose-slug:wardrobe-slug`.
Roles without an explicit pose hit `ROLE_CATALOG.json`.

## Scrape (automatic on set, or replay)

```bash
python3 scripts/agentify.py scrape --from-set SET.json --wardrobe "black Arena one-piece..."
```

Each still writes:
- one **pose pack** under `references/packs/pose/`
- one **wardrobe pack** under `references/packs/wardrobe/`

Same pose on two stills → **one pack**, `instances[]` grows, version patch bumps.
Same wardrobe across the set → **one wardrobe pack** with N instances.
Index: `references/registry/packs.index.json`. Schema kind `wardrobe` is now legal.

Four plates still one candidate. Packs are the scrape product, not extra agents.

## Plate recipe (v0.5 lock — IP-WQ-204 PROMOTED)

Inbound frame(s) = **plate 0 / source**. Emit first. Never publish a raw file as plate A.

Default emit, forever: **0 A B C D**.

Engine: **generate**. If the request flags face-copy / edit-her-face / img2img / keep-the-real-face, `engine_for()` regresses to generate. Inbound jpeg is never A.
`python3 scripts/agentify.py engine --desc "..." --requested edit`

0. **0 / SOURCE** — the actual inbound still or official thumb. Show it. Do not rename it A.
1. **A / ID** — regenerated photoreal cousin of the source frames.
2. **B / HEAT** — same identity, heat.
3. **C / ANIME** — same identity, anime.
4. **D / RIG** — same identity, turnaround.

Named Short:

```bash
python3 scripts/yt_short_ingest.py URL --who cand-slug --frames 8
```

Interval frames across the runtime when video bytes land. 403/SABR → thumbs + fallback flag. Then `agentify set` + scrape for pose/wardrobe. Plate emit is keep → Drive → `render_file`.

Do not promote from this pass. Confirm is a later sentence.

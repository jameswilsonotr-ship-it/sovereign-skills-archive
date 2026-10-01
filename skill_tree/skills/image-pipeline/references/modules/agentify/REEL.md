# Agentify reel lock — named YouTube Short

Deterministic path. Do not improvise.

## Fetch

```
yt-dlp
  --cookies artifacts/secrets/youtube-cookies.txt
  --js-runtimes node:/usr/bin/node
  -f 18
  URL
```

Android client does **not** accept cookies in current yt-dlp. Do not use it.

Cookies never git, never Drive. Refresh from Gmail self-send when YouTube kicks us.

## Frames

`yt_short_ingest.py URL --who SLUG --frames 13`

Interval samples across the runtime. Skip first/last 4%.
Raw frames = SOURCE. Never plate A.

## Foreplay loop (before plates)

1. Fetch short (cookies + Node).
2. Interval frames (`--frames 13`). Scene-detect is a **stub** (interval). Cut detector later.
3. Count featured characters. This reel: **1**. Others may be N.
4. Poses per character. Wardrobe packs per character; note changes.
5. Crowd / extras → ignored.
6. Then plates per character: A cousin, B heat, C anime, D rig.

```
python3 scripts/agentify.py reel-analyze --inbound DIR --n-characters 1 --slug SLUG
```

Writes `FOREPLAY.json` + updates `CHARACTERS.json`.

## Characters

Write `CHARACTERS.json` on the inbound dir.

- One speaking / featured person → one candidate, N pose packs.
- Second featured person → second candidate, own pose/wardrobe packs.
- Crowd / extras → `ignored`. Not mouths.

## Plates

A regenerated photoreal cousin. B heat. C anime. D rig.
Same-turn: keep_path → Drive → render_file on rendered JPEG.
No promote from ingest.

## Pose + wardrobe menu

After A–D, emit menus. Show raw stills. Offer cousins. User picks pose × wardrobe.

```
python3 scripts/agentify.py menu --inbound DIR
python3 scripts/agentify.py pick --inbound DIR --who SLUG --pose POSE --wardrobe WARD
```

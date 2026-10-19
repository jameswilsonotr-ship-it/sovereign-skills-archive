# IP-WQ-174 — music-video inbound fork

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 22:52 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-162 feed fork · IP-WQ-161 local video · agentify 0.5.0  
**Research twin:** IP-WQ-175  
**Smoke:** Katy Perry — Hot N Cold (Official Music Video), `kTHNpusq654`

## Goal

A named music video — URL, title-only, or lyric fragment — lands on the same scrape as a Short after fetch. New inbound **kind** `music-video`. Not a new skill. Not a mint.

Platform is fetch. Scrape + plates do not change.

## Why this is not a Short

Hot N Cold is 4:43. Current reel lock is Short-shaped (`--frames 13`, skip first/last 4%, cap 48). Even-interval on a four-minute pop tape undersamples the chorus change and the wardrobe hop. Section-aware sample is the catch.

## Inbound kinds (extends 162)

| inbound | fetch | then |
|---|---|---|
| YT / Vevo / youtu.be music-video URL | yt-dlp + cookies + Node. 403/SABR → thumbs + say so | reel + lyric align |
| title / artist / lyric fragment / broken URL | resolve ladder in IP-WQ-175. Do not invent an ID | same after resolve |
| official audio only | AcoustID optional; still-set research if no picture | still set, not fake frames |
| local mv dump | IP-WQ-161 `--file` | reel + lyric align |

## Schema work (finish what SCHEMA.md already named)

SCHEMA.md already lists PHRASE.json and PLATE.json. Files missing:

- `schema/phrase.schema.json` — ordered beats + `section` + optional `lyric_line` + optional `bar`
- PERSONA is **not** a fifth plate. Thin fields on CHARACTER: `role_in_tape` (`lead` / `foil` / `chorus-body` / `object`), `relations[]`, `lyric_job` (what the line is doing to that body)
- BEAT already has `t`. Keep it. Add optional `section` echo so a beat can live without a phrase yet

Culture still bends wardrobe and pose. It does not mint a mouth.

## Sample lock

Adaptive + section-aware. Not a fixed 13.

1. Cold-open / intro / verse / pre / chorus / bridge / drop / outro / tag
2. Hold frames drop. Cut / wardrobe / formation / face-bin change keep
3. Chorus loop is one PHRASE reused, not thirty new poses
4. Cap goes up for long-form. Cap 48 on a 4:43 tape is the miss
5. Frames = SOURCE. Never plate A

Hook the existing `reel_sample.py` idea. Cut-detect stub in 161 becomes real here via PySceneDetect when bytes land.

## Same-turn law (does not move)

- One featured adult she picks → one candidate, A cousin / B heat / C anime / D rig
- Second featured adult → second candidate
- Crowd / extras / bat-brides / congregation / kids → `ignored`
- No `CONFIRM AGENT FOR <SLUG>` → stays candidate
- Do not mint the celebrity because the tape is famous
- Marks live on CHARACTER. Plates do not invent tattoos
- 403 prints the recovery card. Do not fake frames
- keep_path → step6 `--gate 0` → `render_file` on `artifacts/rendered/*.jpg`

## Smoke (do not run plates tonight unless asked)

`https://youtu.be/kTHNpusq654`  
Official: Katy Perry — Hot N Cold (Official Music Video), channel Katy Perry, 2008-10-14, remastered HD, ~4:43, 1.3B+ views. Directed by Alan Ferguson. Produced by Melissa Larson.

Query param `?is=` on the share link is a typo for `?si=`. Resolver must survive that.

Expected scrape (research, not minted):

| roman | who | kind | notes |
|---|---|---|---|
| I | Katy / bride-lead | candidate only | featured mouth. Wardrobe hops. Do not mint Katy Perry |
| II | Alexander (Alexander Francis Rodriguez) | candidate only if she asks | foil / runaway groom. Daydream POV |
| — | priest, Keith + Mary Hudson, Shannon Woodward, Jadyn Maria, bat-brides, dancers, kids, zebra | ignored | crowd / cameo / prop |

Wardrobe letters to scrape if bytes or stills land:

- A — wedding gown at the altar (RS note: dress breaks down into a onesie for the chase)
- B — red latex + brown bob, club / warehouse stage
- C — urban street set, dancers
- D — zebra-leash tag before the snap-back

Phrase engine is the chorus: hot/cold, yes/no, in/out, up/down, fight/break-up, kiss/make-up. One phrase, many beats.

Structure: spoken vows cold-open → verse chase → chorus loops → daydream warehouse / brides-with-bats / urban / zebra → snap back to altar → he says I do.

## Split out (2026-09-10 23:04)

174 stays the inbound contract. Ideas live as their own tickets:

176 phrase schema · 177 persona-on-character · 178 section sample · 179 resolver · 180 captions · 181 still fallback · 182 smoke · 183 featured/nested · 184 letter≠heat · 185 library cap · 186 FOREPLAY audit · 187 anti-mint famous · 188 audio-only · 189 confirm pass · 190 voice phrases

## Exit

- Feed-fork row for `music-video` exists in 162
- phrase.schema.json on disk
- CHARACTER persona fields documented
- One inbound dir for `kTHNpusq654` with FOREPLAY.json + CHARACTERS.json + BEATS stub, **or** an honest 403 + research still-set + no fake frames
- No mint
- Title-only / broken-URL resolve is specified in 175 and callable from here

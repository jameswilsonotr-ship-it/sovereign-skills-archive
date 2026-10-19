# IP-WQ-175 — music-video research + resolve + libraries

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 22:52 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-174  
**Smoke:** Katy Perry — Hot N Cold, `kTHNpusq654`

## What this ticket is

174 is the inbound contract. This is how we actually pull it off: tape research, URL-less resolve, Python stack, what we refuse.

Do not install a second navy of media tools. Prefer what the bunker already speaks (ffmpeg, yt-dlp cookies path, adaptive sample, agentify schemas). Heavy models are later, cab-optional.

## The tape (why this one)

Bunny handed `https://youtu.be/kTHNpusq654?is=aPv7oNXt9IiwGUf2`.

- ID: `kTHNpusq654`
- Title: Katy Perry — Hot N Cold (Official Music Video)
- Channel: Katy Perry (official)
- Upload: 2008-10-14 (video released ~2008-10-01; this upload is the remastered official)
- Runtime: 4:43
- Views: ~1.37B as of this pass
- Album: One of the Boys (2008)
- Writers / production: Katy Perry, Dr. Luke, Max Martin; additional Benny Blanco
- Director: Alan Ferguson. Producer: Melissa Larson. DP: Shawn Kim
- Church: First Christian Church, Los Angeles (also used in Indiana Jones and the Kingdom of the Crystal Skull)
- Groom: Alexander Francis Rodriguez
- Cameos: parents Keith Hudson + Mary Perry/Hudson; bridesmaids Shannon Woodward + Jadyn Maria
- Lyric thesis, which is also the visual thesis: “You change your mind / like a girl changes clothes”

This is the right smoke on purpose. Not because it is pretty. Because:

1. It is long-form, not a Short. Stresses sample + phrase.
2. Two featured adults, huge ignored crowd. Stresses CHARACTERS.json.
3. Wardrobe hops are the joke of the song. Stresses wardrobe packs.
4. Chorus is a binary flip list. Stresses PHRASE reuse.
5. Official captions exist. Lyrics live in the description. Research stills exist if SABR eats the file.
6. Title-only (“hot n cold katy”) uniquely resolves. Broken `?is=` share link still carries the ID.

Law: research and scrape. Do not mint Katy Perry. Do not mint Alexander. Confirm is a later sentence.

## URL-less / dirty inbound (the actual ask)

Most nights she will not paste a clean watch URL. She will say the song, mis-speak the title, drop a lyric, forward a broken share, or hand an mp3 from the cab.

Resolver is fetch. It does not scrape. It does not plate.

### Normalize

Strip `official music video`, `official video`, `remastered`, `HD`, `VEVO`, `lyric video`, `audio`, bracket tags. Keep artist + title tokens. Survive `youtu.be/ID?is=` (typo for `si`) and `youtube.com/watch?v=ID,` trailing commas.

### Ladder

1. **Already an ID.** 11-char YouTube id in the string → treat as URL. Hot N Cold share is this case even when `?is=` is garbage.
2. **yt-dlp search.** `ytsearch5:ARTIST TITLE official music video`. Rank: official artist channel first, then Vevo / label, then “Official Music Video” in title, then duration ±15% of known runtime if we have it. Human pick if top 3 disagree.
3. **Captions-only probe.** `youtube-transcript-api` or `yt-dlp --write-auto-sub --skip-download`. If captions exist, we can align lyrics before video bytes land.
4. **Knowledge graph.** Wikipedia videography table, MusicBrainz recording → official video relationship, IMVDb. Use to confirm director / year / runtime, not to invent frames.
5. **Audio-only inbound.** Optional chromaprint + AcoustID / MusicBrainz. Identify the recording, then jump to step 2. Never claim a face from an mp3.
6. **Lyric fragment only.** `syncedlyrics` / lrclib / Genius plain text → title+artist guess → step 2. Ambiguous fragment (“we kiss we make up”) still needs a human pick.
7. **Hard fail.** No ID, no confident search hit. Research still-set from public thumbs / press / Wikimedia. Say so. Do not hallucinate a watch URL. Do not fake frames.

Title-only is a first-class inbound kind, not a courtesy. Write the resolved URL + confidence + rejected candidates into FOREPLAY.json so we can audit a wrong tape.

### What URL-less is good for

- Voice: “agentify that hot and cold video”
- No signal / cookies dead: still get a character+wardrobe+phrase card from research
- Cab: she names the song, steel is offline, we queue resolve for next high-water

### What URL-less is not

- A license to plate a celebrity from memory
- A Shazam product
- A reason to skip the 403 card when we *do* have an ID and googlevideo kicks us

## How the analysis maps onto agentify

| tape fact | schema |
|---|---|
| Katy at the altar | CHARACTER I, wardrobe A, pose facing-camera-id, face focus/talk |
| Alexander hesitates | CHARACTER II, face averted, persona foil |
| Congregation dances, disco lights | extras ignored. Atmosphere pack later if asked |
| Chase / onesie gown | wardrobe A variant or new letter. Pose run |
| Warehouse stage, red latex, brown bob | wardrobe B. New hair.family note on that look, not a new mouth |
| Crowd-surf | II object-feeling beat. Still one candidate |
| Bat-brides | ignored chorus-body unless she points at one still |
| Phone screen singing | nested frame. Do not mint a third Katy |
| Urban dancers + kids | ignored |
| Zebra on a leash | prop. Optional object pack. Not a mouth |
| Snap-back to altar, he says I do | section `tag`. Same wardrobe A. Phrase resolves |
| Chorus binaries | PHRASE `hot-n-cold-chorus` reused across t |

Persona field examples (on CHARACTER, not a new file):

```json
{
  "id": "I",
  "role_in_tape": "lead",
  "lyric_job": "names the flip and hunts it",
  "relations": [{"to": "II", "rel": "bride-of"}]
}
```

```json
{
  "id": "II",
  "role_in_tape": "foil",
  "lyric_job": "is the flip",
  "relations": [{"to": "I", "rel": "groom-of"}]
}
```

Heat hops stay `I-1-C-e` etc. Wedding-gown cling vs red-latex cling are wardrobe letters, not intensity keys. Intensity still means cut / sheer / crop on the picked letter.

## Python stack

Cab-first. Nothing here is a plate engine. Generate / keep_path stays the emit path.

### Already in the house or should be

| lib / bin | job |
|---|---|
| ffmpeg / ffprobe | decode, scale, frame dump. ffmpeg skill already owns this |
| yt-dlp + cookies + Node | fetch. REEL.md lock. Android client must not carry cookies |
| Pillow | frame I/O, keep_path jpeg |
| imagehash / dhash | adaptive sample “keep when it differs” |

### Fetch + captions (small)

| lib | job | note |
|---|---|---|
| yt-dlp `ytsearchN:` | title-only resolve | prefer official channel |
| youtube-transcript-api | timed captions without bytes | official Hot N Cold has a transcript |
| yt-dlp `--write-auto-sub --skip-download` | same, already-known binary | use when the py wrapper flakes |
| syncedlyrics + lrclib.net | LRC when captions miss | title+artist+duration |
| musicbrainzngs | recording / official-video rel | optional confirm |

### Structure (medium, local CPU)

| lib | job | note |
|---|---|---|
| scenedetect (PySceneDetect) | cut list | this is the 161 interval stub grown up |
| librosa | tempo, onset, chorus-ish segmentation | good enough for pop. Not a musicologist |
| numpy / scipy | glue | already common |

Chorus detection does not have to be perfect. For Hot N Cold we can seed sections from captions + the known cold-open vows. librosa is a helper, not the priest.

### People (later, optional, Jetson-ok)

| lib | job | note |
|---|---|---|
| mediapipe | pose + face mesh on keeper frames | pose pack draft. Not identity |
| ultralytics YOLO | person boxes / count mouths | featured vs crowd |
| supervision | track ids across cuts | only to count, not to name |

### Do not pull in on night one

- corpus-mill, Qwen-VL 7B, pyannote diarization — too much steel for a 4:43 pop tape
- insightface / face-recognition embeddings as plate A conditioner — IP-WQ-163 + cousin-first law
- Demucs / WhisperX unless captions fail *and* we have the audio
- paid Genius / Musixmatch keys
- Shazam commercial SDK
- any “make the music video the agent”

Whisper (faster-whisper) is the fallback ASR when there are no captions and we have audio. Official Hot N Cold does not need it.

## Honest failure modes

1. **403 / SABR.** Already specified. Thumbs + research stills + recovery card. Path does not change.
2. **Wrong search hit.** Lyric video, live, FIFA 09 trailer, fan recut. Resolver must prefer “Official Music Video” on the artist channel. Write rejected IDs.
3. **Cover / lookalike.** Title-only “hot n cold” will hit covers. Duration + channel rank.
4. **Face-copy temptation.** The whole point of a famous tape. Engine stays generate. Inbound jpeg is never A.
5. **Cameo inflation.** Parents and bridesmaids are not mouths.
6. **Zebra / baseball-bat-brides.** Fun, not candidates.
7. **Copyright.** Stills are SOURCE. Cousins are generated. We do not republish the master.

## Pull-off plan (when she says go)

1. Resolve `kTHNpusq654` (already done). Normalize the dirty `?is=` link in the resolver tests.
2. Captions first (`youtube-transcript-api` or yt-dlp skip-download). Build PHRASE draft from chorus lines.
3. Try video bytes. If 403, official thumbs + public stills as SOURCE set. Say so.
4. Adaptive + scene cuts if bytes land. Otherwise manual keeper list from the research card above.
5. CHARACTERS.json: I Katy candidate, II Alexander candidate-if-asked, rest ignored.
6. Wardrobe A–D letters. Pose packs from altar / chase / stage / zebra-tag.
7. FOREPLAY.json + BEATS with `t` + section.
8. Stop. Show the card. No plates unless she picks a Roman and a letter.
9. If she picks I-A, four cousins. keep_path. No mint.

## Split out (2026-09-10 23:04)

175 stays the research SSOT + library narrative. Operational slices are 176–190 under `references/work-queue/items/`.

## Exit

- This file is the research SSOT for the Hot N Cold smoke
- Resolver ladder is written and testable on dirty share links + title-only “hot n cold katy perry”
- Library list is capped: ffmpeg, yt-dlp, captions wrapper, scenedetect, librosa, optional mediapipe
- No new top-level skill
- No celebrity mint

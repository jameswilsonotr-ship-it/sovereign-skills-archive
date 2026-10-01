# Agentify RUNBOOK — cold conversation

Read this file when the user says `agentify` and hands a still or a YouTube Short.

Do not improvise a shorter path. Do not mint.

## Trigger

`agentify` / `agentify this` / `make an agent` / `identify as agent` / `B AGENT`  
plus a still or `youtube.com/shorts/ID`.

## Loop (every time)

1. **Ingest**
   - Still → copy into `artifacts/agentify_inbound/<slug>/frames/`.
   - Short → download video, then **adaptive sample**, not a fixed 13:
     `scripts/reel_sample.py --src VIDEO.mp4 --dest DIR/frames --fps 6 --cap 48`
     Cheap fps strip. Keep a frame when it differs from the last keeper.
     Stutter / techno / cut / wardrobe change → more frames. Hold → fewer.
     Even interval is the miss. This is the catch.
     Cookies: `artifacts/secrets/youtube-cookies.txt` + `--js-runtimes node`.
     Frames = SOURCE. Never plate A.
2. **Foreplay**
   - Look at the frames. Count featured mouths. Crowd is ignored.
   - `scripts/agentify.py reel-analyze --inbound DIR --n-characters N --slug SLUG`
   - Emit CHARACTER / WARDROBE / POSE / FACE / BEAT / PHRASE against `schema/`.
     Face bins only: focus smile talk look-down neutral.
     Marks stay on CHARACTER. Do not invent tattoos on plates.
3. **Default plates**
   - Pick the cleanest ID still as source.
   - A regenerated photoreal cousin. B heat. C anime. D rig.
   - A wardrobe = scraped. Heat hops follow the pick (`c/d/e`), not a hidden clothes-on.
   - Tool-moderate on a heat hop → implication pack retry of the same code (IP-WQ-173). No promote.
4. **Serialize + show**
   - `scripts/agentify.py serialize --src FILE --slug SLUG --tag a-id|b-heat|c-anime|d-rig`
   - `google_drive_upload_artifact` each rendered JPEG (lake folder in the keep).
   - `step6_drive_flush.py --gate` must exit 0 before claiming pushed.
   - Show tags: `scripts/android_show.py --client $CLIENT --utterance "$UTTERANCE"`. ANDROID mute unless dump verb (IP-WQ-169). Other clients: `render_file` on kept JPEGs.
5. **Menu**
   - `scripts/agentify.py picker --candidate NAME --outfit OUTFIT --pose1 P1 --pose2 P2`
   - Print the eight-line card. English and codes both parse (IP-WQ-118).
   - Characters Roman I II III. Poses 1 2 3. Lanes A B C D E. Intensity c d e.
6. **Pick**
   - User says `I-1-C-e` or `1cde` or `sheer on the look-back`.
   - `scripts/agentify.py heat --code CODE --cling unitard-tight|unknown`
   - Dry-run hop plan prints first. Then plates. Serialize. Drive only after `--gate` 0.

## Stop

No `CONFIRM AGENT FOR <SLUG>` → stays candidate.

## If YouTube 403

Print the recovery card. Do not fake frames. Never git cookies. Never Drive cookies.

```
YOUTUBE 403
live path: artifacts/secrets/youtube-cookies.txt
mail: https://mail.google.com/mail/u/0/#inbox/1a0531dd6066a4e9
search: https://mail.google.com/mail/u/0/#search/cookies.txt+has%3Aattachment
1. open the mail
2. download cookies.txt
3. drop it on the live path
4. say retry ingest
```

Full card: `COOKIES_RECOVERY.md`

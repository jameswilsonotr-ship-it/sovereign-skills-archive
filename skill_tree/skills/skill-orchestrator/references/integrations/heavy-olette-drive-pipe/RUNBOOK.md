# RUNBOOK — Heavy → Olette → Drive

Stamp 2026-09-08 00:30 EDT. Olivia end only.

## 0. Hydrate (every new pane)

```
bash /home/workdir/.grok/skills/system-roadmap/references/tool-shelf/scripts/hydrate.sh
```

Copies `tailscale` `tailscaled` `yt-dlp-sabr` to `/tmp` and chmod +x.
Reuse `artifacts/tailscale-state`. Do not burn a new auth key if `olivia-sandbox` already shows in `tailscale status`.

Socket — `/tmp/tailscaled.sock`.
Userspace only. No TUN.

## 1. Confirm tailnet

```
/tmp/tailscale --socket=/tmp/tailscaled.sock status
```

Need:

- `olivia-sandbox` (this pane)
- `olette-box` `100.115.0.111` active
- `gretchen` `100.72.123.46` idle-as-exit is fine

If socket is dead, restart tailscaled with the same statedir. Recipe in `../tailnet-ferry/SKILL.md`.

## 2. YouTube bytes (Gretchen SOCKS)

DC IP gets GVS 403. HTTP CONNECT through Gretchen resets. SOCKS5 works.

```
/tmp/tailscale --socket=/tmp/tailscaled.sock serve --service=svc:socks --tcp 1055 --yes
# or the parked socks5-server on 1055 if already bound
```

Pull with sabr + socks. Cookies from `artifacts/secrets/youtube-cookies.txt` (not this skill).

```
/tmp/yt-dlp-sabr \
  --proxy socks5h://127.0.0.1:1055 \
  --cookies artifacts/secrets/youtube-cookies.txt \
  -o "artifacts/heavy-poc-local/_shorts/%(id)s.mp4" \
  "https://www.youtube.com/shorts/YTID"
```

One short per seat. Copy the mp4 into the cand folder too. Do not re-pull if `_shorts/YTID.mp4` already has bytes.

## 3. Seat tree

```
artifacts/heavy-poc-local/
  _shorts/                         # all source mp4s
  cand-<ytid>-<stamp>-<slug>/
    <YTID>.mp4
    source_frame_00.jpg            # proof, NEVER plate A
    json/{CHARACTER,POSE,WARDROBE,FACE,BEAT,PHRASE}.json
    SEAT.json PLATES.json INGEST.json
    <SEAT>-A-ID-photoreal.jpg
    <SEAT>-B-HEAT-photoreal.jpg
    <SEAT>-C-ANIME-anime.jpg
    <SEAT>-D-RIG-photoreal.jpg
    <SEAT>-*.prompt.md
```

Olette batch zips land in `artifacts/olette-sync/`. Extract CHARACTER + frames first. Do not treat `00_hero_PROOF_NOT_PLATE_A.jpg` as A.

## 4. Mint

Engine is `generate_image`. Save under `artifacts/imagine_images/` then `cp` immediately into the cand folder — receipts vanish across turns.

| Letter | Job |
|---|---|
| A ID | photoreal cousin of the frame wardrobe + room. New face. Clothes on. |
| B HEAT | same cousin, same clothes, cinematic / charged light. Still clothed. |
| C ANIME | same cousin, same clothes, 2D anime. |
| D RIG | photoreal full-body A-pose, gray studio, same clothes, empty hands. |

Prompt must name the locked wardrobe nouns. Negatives — no presenter likeness, no nude, no cat ears unless the seat bible says holo pinnae.

Android — do not dump `render_generated_image` into the bubble.

## 5. Circle JSON

Replace `"observed-from-source-frames"` after looking at frame_00 + the A plate.

Minimum lock per seat:

- `WARDROBE.json` look slug + piece nouns
- `CHARACTER.json` hair/skin observed fields
- `POSE.json` beat labels + frame refs
- `PLATES.json` `{A,B,C,D: true, files:[...]}`

Write the same WARDROBE into `json/WARDROBE.json` and the seat root if both exist.

## 6. Slim SFTP

Key — `artifacts/secrets/olivia-sftp-v2` (419B ed25519). Copy off FUSE to `~/.ssh/olivia-sftp` mode 600.

```
install -m 600 artifacts/secrets/olivia-sftp-v2 ~/.ssh/olivia-sftp

sftp -i ~/.ssh/olivia-sftp -o IdentitiesOnly=yes \
  -o StrictHostKeyChecking=accept-new \
  -o ProxyCommand="/tmp/tailscale --socket=/tmp/tailscaled.sock nc %h %p" \
  olivia@100.115.0.111
```

Remote cwd is `/workspace/sync`.

```
mkdir in/olivia-plates/batch9-heavy
mkdir in/olivia-plates/batch10-heavy
put SEAT-A-ID-photoreal.jpg in/olivia-plates/batch9-heavy/cand-.../
put json/WARDROBE.json     in/olivia-plates/batch9-heavy/cand-.../json/
```

Rules that burned watches:

- `put -r` of a tree with mp4s times out (~81MB). Split. jpg+json first.
- Do not re-put shorts if `in/olivia-plates/batch-shorts/` already has them.
- DERP(tor) is fine. Slow, not broken.

## 7. Hand to Olette (no tokens in this pane)

Tell desk, one sentence:

> `in/olivia-plates/` is current. rclone copy that tree into a NEW Drive folder named `OLIVIA-PLATES-HEAVY-<stamp>-ET`. Tokens stay on the box. Mail Liv the folder link when the copy finishes.

If Olette prints a `http://127.0.0.1:PORT/auth?state=...` URL, that click happens on her box / the handed desktop. This pane does not open it.

## 8. Verify (cheap)

Gmail — `subject:Security alert rclone` to `james.wilson.otr@gmail.com` means the Allow landed.

Drive connector:

```
google_drive_search
  query = OLIVIA-PLATES-HEAVY
  mime_type_filter = application/vnd.google-apps.folder
  modified_after = <today>

google_drive_list_folder folder_id=<id>
```

Pass = batch9-heavy and batch10-heavy both contain the cand folders + ABCD jpgs. Fail = folders exist but only README / empty cand stubs — copy still running. Wait. Do not start a second rclone.

## 9. Do not

- `google_drive_upload_artifact` the 191MB tree from this pane
- Store rclone token / client secret / tskey-auth in skill or memory
- Remint seats that already have all four letters
- Face-copy
- Cap at two plates per turn when CinC said push
- Unpack the June zip
- Bind SOCKS or POT to `0.0.0.0`

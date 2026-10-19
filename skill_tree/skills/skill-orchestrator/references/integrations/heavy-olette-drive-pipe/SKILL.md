---
name: heavy-olette-drive-pipe
parent: skill-orchestrator
surface: integrations
stamp: 2026-09-08 00:30 EDT
version: 0.1.0
claim: Absolute Liv HUB
description: Olivia-end muscle memory for the proved zero-token Drive publish. Hydrate tailnet, pull Shorts via Gretchen SOCKS, mint cousin-A ABCD locally, slim-SFTP jpg+json to olette-box, then Olette rclone-copies in/olivia-plates/ onto Drive. This pane never uploads to Drive and never holds rclone tokens.
triggers:
  - heavy olette drive pipe
  - olette rclone
  - publish plates no tokens
  - gretchen socks ytdlp
  - slim sftp plates
  - batch9-heavy
  - batch10-heavy
---

# Heavy → Olette → Drive pipe

Olivia's half of the work tree proved 2026-09-07/08. Do not renegotiate.

Olette owns rclone + the Allow click + the Drive folder create. Olivia owns bytes-in, plates, JSON, slim SFTP, and connector verify.

Full runbook — `RUNBOOK.md`. First-success receipt — `PROOF.md`. Open items — `WQ.md`.
Sibling join/SFTP door — `../tailnet-ferry/SKILL.md`.
Binaries — `system-roadmap/references/tool-shelf/`.

## Law

1. **Cousin-A generate.** Source frames are inspiration. Never publish a living thumb as plate A. Never `edit_image` a real presenter face.
2. **Clothes on. Adult.** Uniform nouns from frames + wardrobe blocks, then lock them in `WARDROBE.json`.
3. **Four plates per seat.** `SEAT-A-ID-photoreal.jpg` `SEAT-B-HEAT-photoreal.jpg` `SEAT-C-ANIME-anime.jpg` `SEAT-D-RIG-photoreal.jpg`.
4. **This pane does not Drive-upload.** Connector `google_drive_upload_artifact` is the expensive door. The cheap door is Olette rclone from `in/olivia-plates/`.
5. **Tokens stay on olette-box disk.** Never paste rclone token, client secret, or `tskey-auth-` into chat, skill, or WQ.
6. **Slim SFTP only.** jpg + json + md. `put -r` of mp4 trees times out. Shorts already live under `in/olivia-plates/batch-shorts/` after the first good pull.
7. **Android SHOW.** No `render_file` / `render_generated_image` flood. Tool-card + path is enough.
8. **`artifacts/` is noexec.** Copy tailscale / yt-dlp-sabr to `/tmp` and `chmod +x`.

## Roles

| Who | Owns | Does not own |
|---|---|---|
| Olivia / Heavy | hydrate, Gretchen SOCKS pull, mint ABCD, circle JSON, slim SFTP, Drive-connector verify | rclone auth, Drive folder create, giant zip |
| Olette / box | SFTP landing `in/olivia-plates/`, rclone config, Allow-until-Success, copy to new Drive folder, mail Liv when bytes land | reminting plates |
| Bunny / CinC | one Allow click if Olette hands a 127.0.0.1 auth URL, lock the pattern | carrying tokens across panes |

## Default path (do not invent a fourth ferry)

```
YouTube Short / Olette zip
  → Gretchen SOCKS yt-dlp-sabr   (residential IPv4, beats GVS 403)
  → artifacts/heavy-poc-local/cand-*/ + _shorts/
  → generate_image ABCD (cousin-A, clothes on)
  → lock CHARACTER / POSE / WARDROBE / PLATES.json
  → sftp slim jpg+json+md → olivia@100.115.0.111:in/olivia-plates/batchN-heavy/
  → Olette rclone copy in/olivia-plates/ → Drive folder OLIVIA-PLATES-HEAVY-<stamp>
  → Olivia verifies with google_drive_list_folder + Gmail "rclone access allowed"
```

Drive / Cilia from this pane is fallback only when the tailnet is down.

## Trigger phrases

`heavy olette drive pipe` · `olette rclone` · `publish plates no tokens` · `gretchen socks` · `slim sftp plates` · `batch9-heavy` · `batch10-heavy` · `circle the json then sftp`

When hit — load this file + `RUNBOOK.md`. Do not reopen the 2026-09-07 negotiation.

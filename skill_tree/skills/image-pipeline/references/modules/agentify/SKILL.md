---
name: agentify
kind: image-pipeline-subscale
parent: image-pipeline
version: 0.5.0
status: LIVE-DRAFT
date: 2026-09-03 15:56 EDT
claim: Absolute Liv HUB
description: >
  Inbound verb. Menu B AGENT. One person → one candidate + four plates.
  A named Short is a reel: pull multiple frames as SOURCE. A is a regenerated
  photoreal cousin. B heat. C anime. D rig.
  Same-turn emit: keep_path → step6 Drive flush → render_file on rendered JPEG.
  Not a top-level skill. Not a merge engine. Plates do not promote.
triggers:
  - agentify
  - agentify this
  - make an agent
  - identify as agent
  - B AGENT
---

# Agentify — image-pipeline subscale v0.5.0

Cold-boot spine: `RUNBOOK.md`. Follow it. Then this file.

No `/skills/agentify`. Lives under image-pipeline.

Bare `identify` is not a hit. Confirm is a later sentence.

## YouTube Short (named URL)

The short is a **reel**. Pull multiple frames across the runtime (`yt_short_ingest.py --frames 8`).
Those frames are inspiration for pose + wardrobe scrape.
They are not plate A.

This sandbox often gets **403 / SABR** on googlevideo. Then ingest falls back to official thumbs and says so. The path does not change.

## Recipe

Inbound frame(s) = **source**. Never publish a raw file as plate A.

| Plate | Job |
|---|---|
| A / ID | Regenerated photoreal identity card |
| B / HEAT | Same identity, heat |
| C / ANIME | Same identity, anime |
| D / RIG | Same identity, turnaround |

One candidate. Packs from scrape. No mint until `CONFIRM AGENT FOR <SLUG>`.

## Same-turn emit (IPQ-010 + IPQ-078)

Not optional. Generating into `imagine_images/` and talking is a protocol fail.

1. `edit_image` / `generate_image` off the source still.
2. `scripts/keep_path.py --src <scratch.jpg> --slug <slug> --prompt "..."` → `artifacts/rendered/<slug>_<stamp>.jpg` + `.prompt.md` + `.keep.json`.
3. `scripts/step6_drive_flush.py --from-keep <keep.json>`.
4. `google_drive_upload_artifact` for each `drive.uploads` row.
5. `scripts/flush_drive_queue.py --mark KEEP --field jpeg|prompt|keep --file-id ID`.
6. Show with **`render_file` on the rendered JPEG only**. Also legal: `render_edited_image` / `render_generated_image` as the live emit wrapper (IPQ-010). Never `render_file` on `imagine_images/`.

Helper: `scripts/agentify.py serialize --src FILE --slug SLUG` wraps keep_path.

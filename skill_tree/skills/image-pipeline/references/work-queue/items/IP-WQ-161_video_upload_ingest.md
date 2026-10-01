# IP-WQ-161 — local video upload ingest

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10  
**Claim:** Absolute Liv HUB

## Goal
Inbound mp4/webm (this pane’s 6s loops, cab clips, Imagine video downloads) hits the same reel path as a named YouTube Short.

## Work
- `scripts/yt_short_ingest.py` grows a `--file` mode, or sibling `scripts/video_ingest.py`.
- Sample `--frames 13`, skip first/last 4%. Interval stub until cut-detect.
- Write `FOREPLAY.json` + `CHARACTERS.json` on the inbound dir.
- Frames are SOURCE. Never plate A.
- Smoke: `artifacts/attachments/133985.mp4` (6.04s, 6 frames already extracted by the client).

## Exit
One local file in → inbound dir + FOREPLAY.json + raw frames. No mint.

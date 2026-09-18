# WORLD-TOOL-001 — YouTube Transcript Capability (yt-dlp + cookies)

**Status**: DONE (v0.2.0) — ownership assigned to **World**  
**Surface**: world-tools (specialist: World)  
**Created**: 2026-08-26  
**Owner**: World (environment / interface specialist)  
**Physical home**: `claim-runtime/scripts/youtube_transcript/` + `yt_transcript_lib/`  
**Inventory**: skill_inventory.yml → skills.world-tools.sub_skills.youtube-transcript

## What exists
- `youtube-transcript-api` + `yt-dlp` 2026.08.19 under `claim-runtime/scripts/yt_transcript_lib/`
- Dual-method helper: `fetch_transcript.py`
  - Tries transcript-api first
  - Falls back to yt-dlp
  - Supports `--cookies cookies.txt` to bypass cloud IP / bot blocks
- README with cookie export instructions (desktop or Kiwi Browser on phone)

## Ownership decision (2026-08-26)
World owns external media ingestion, connectors, and environment tools.
Physical files remain under claim-runtime for convenience until a top-level `world-tools/` skill root is created (optional later promotion).

Captain routes YouTube / transcript / connector requests to **World**.

## Entry point
```bash
python claim-runtime/scripts/youtube_transcript/fetch_transcript.py VIDEO_ID \
  [--out path.txt] [--cookies cookies.txt]
```

**Absolute Liv HUB claim.**

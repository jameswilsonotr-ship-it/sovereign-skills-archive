# FFMPEG-WQ-001 — nitpicks (IP-WQ-201 twin)

**Status:** DOCUMENTED 2026-09-11 05:50 EDT
**Claim:** Absolute Liv HUB

## Cute nitpicks, not blockers

1. User skill dir used to be missing. This folder is the pointer so the next 193 does not launch a hunt.
2. Bundled copy under `/root/.grok/skills/ffmpeg` is SKILL.md + recipes.md only. Zero Python.
3. Encoder is `/usr/bin/ffmpeg` 6.1.1. That is what ingest uses.
4. Sister nitpick: `artifacts/bin/yt-dlp` overlay stays 0644 (`chmod` does not stick). Working binary `/tmp/yt-dlp.bin` 0755, wrapper `image-pipeline/scripts/vendor/bin/yt-dlp`.

Vendor re-pip after every 193 wipe lives on image-pipeline, not here.

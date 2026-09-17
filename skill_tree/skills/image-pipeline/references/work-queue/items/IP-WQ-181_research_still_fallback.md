# IP-WQ-181 — 403 research still-set fallback

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-174 · COOKIES_RECOVERY.md · IP-WQ-162 YT-post thumbs path

## Idea

When googlevideo 403/SABR, long-form MV still has a SOURCE set: official thumbs, watch-page stills, public press. Say so. Do not fake frames.

## Reasoning

Agentify already falls back to official thumbs on Shorts. A famous MV is *better* at this than a random Short — thumbs, Wikipedia stills, Rolling Stone galleries exist for Hot N Cold. The failure mode is pretending those stills are a 13-frame interval strip.

Research stills are SOURCE. They are not plate A. They are not a license to face-copy Katy onto a cousin via img2img.

## Work

- Reuse the 403 recovery card. Do not invent a second card.
- Fetch: official maxresdefault / hqdefault, watch-page og:image, documented public stills
- Label each file `source=thumb|press|wiki` in the inbound manifest
- Manual keeper list from the 175 scene card when we cannot sample
- Never interpolate missing seconds

## Exit

403 on `kTHNpusq654` still produces an inbound dir with ≥1 labeled SOURCE still + FOREPLAY flag `bytes=false`. No silent empty dir. No fake frames. No plates required.

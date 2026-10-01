# IP-WQ-178 — section-aware long-form sampler

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-174 · IP-WQ-161 · REEL.md

## Idea

Shorts keep cheap fps + “keep when it differs.” A 4:43 official MV needs section-aware sampling or the chorus change and the wardrobe hop die.

## Reasoning

REEL.md and yt_short_ingest still think in `--frames 13` and skip first/last 4%. That is correct for a 15s Short. On Hot N Cold it would undersample:

- spoken vows cold-open (before music)
- gown → onesie chase
- latex club look
- bat-bride formation
- urban set
- zebra tag
- snap-back altar

Even-interval is the miss. Adaptive-by-pixels is better but still blind to *song structure*. Cuts + section labels + wardrobe change should force a keeper.

Cap 48 on a 4:43 tape is also the miss. Cap is a budget, not a theology. Pop MV budget: enough to cover every wardrobe letter and every section once, plus one reprise keeper per chorus.

## Work

- `reel_sample.py` (or sibling) grows `--kind music-video`
- Section list: cold-open / intro / verse / pre / chorus / bridge / drop / outro / tag
- Keeper rules: scene cut OR wardrobe letter change OR face-bin change OR section boundary. Holds drop.
- PySceneDetect when bytes exist (161 stub grows up here)
- If only thumbs: use the research card’s manual keeper list. Do not invent in-between frames

## Exit

One command samples a long-form file into `inbound/frames/` + a `SECTIONS.json` with `t` ranges. Frames still SOURCE. No plate A.

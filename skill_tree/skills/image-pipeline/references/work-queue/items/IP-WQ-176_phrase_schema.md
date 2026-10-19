# IP-WQ-176 — phrase.schema.json + chorus reuse

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-174  
**Blocks:** Hot N Cold smoke that wants lyric-aligned beats

## Idea

SCHEMA.md already names `PHRASE.json` as “ordered beats.” There is no `phrase.schema.json` on disk. A music video without phrase is just a pile of stills.

## Reasoning

A pop chorus is not thirty new poses. Hot N Cold’s engine is one binary list sung three times: hot/cold, yes/no, in/out, up/down, fight/break-up, kiss/make-up. If we mint a new pose pack per chorus hit we drown the picker and lie about what changed.

Phrase is the loop. Beat is the instance. Section is the container (intro/verse/chorus/bridge/tag).

## Work

Write `references/modules/agentify/schema/phrase.schema.json`.

Required: `id`, `slug`, `section`, `beat_ids` (ordered).  
Optional: `lyric_line`, `lyric_ref`, `bar`, `reprise_of` (id of the first chorus phrase).

Rule in PROTOCOL / RUNBOOK: identical chorus lyric + same wardrobe letter + same face-bin family → reuse phrase id, append beat instances. Do not fork a phrase because `t` changed.

## Exit

Schema file exists. SCHEMA.md points at it. One sentence in RUNBOOK about reprise. No plates.

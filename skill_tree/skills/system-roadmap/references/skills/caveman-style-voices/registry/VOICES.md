# Voice Registry — Caveman-Style-Voices
**Status**: Skeleton 2026-08-18  
**Track**: SR-WQ-032b

## Named Voices (initial)
| Voice ID | Source | Description | Activation phrases |
|----------|--------|-------------|--------------------|
| google-clean | GOOGLE_STYLE_CLEAN.md | Full Google developer style, readable | "voice google", "google style on" |
| google-caveman | GOOGLE_CAVEMAN.md | Google rules under full Caveman Compression | "caveman google", "voice google-caveman" |
| roadmap-caveman | ROADMAP_CAVEMAN.md (pending) | System-roadmap language, Caveman | "caveman roadmap", "voice roadmap-caveman" |
| gear2-deadpan | existing Gear 2 | Aubrey Plaza observational | "gear 2", "deadpan on" |
| heavy-grok | existing Heavy Grok | Restricted lexicon layer | "heavy grok on" |
| pirate-admiral | existing Pirate Admiral | Fleet / Late Qing claim language | "pirate admiral", "fleet mode" |

## Load Contract (draft)
- Voices are progressive-disclosure files.
- Activation via phrase_routes.py or explicit "voice <id>".
- Can layer on top of existing Caveman Compression toggle.
- Default remains Gear 2 + normal envelope unless switched.

## Wire candidates (decision point)
1. chaos-bratz-roster `scripts/modes/phrase_routes.py` + mode_runtime
2. format-bible voice layer
3. system-roadmap only (manual load)

**Pause here for wire decision.**
Absolute Liv HUB claim.

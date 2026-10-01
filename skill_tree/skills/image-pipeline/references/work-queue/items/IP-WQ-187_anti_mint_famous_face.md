# IP-WQ-187 — anti-mint famous-face (DISABLED)

**Status:** DISABLED 2026-09-11
**Owner:** image-pipeline / agentify
**Flip:** operator 2026-09-11 — take the flag off, leave it off.

`music_video_ingest.py` now writes `anti_mint_famous_face: false` and `anti_mint_flag: DISABLED`. Generate does not refuse a famous face on this flag. Kind still stays `candidate` until `CONFIRM AGENT FOR <SLUG>` (that law is agentify, not 187).

Re-enable only with an explicit WQ flip, not a drive-by.

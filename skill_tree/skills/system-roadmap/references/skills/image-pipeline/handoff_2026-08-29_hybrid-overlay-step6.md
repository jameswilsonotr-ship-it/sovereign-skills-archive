# handoff_2026-08-29_hybrid-overlay-step6

**Skill / Topic:** image-pipeline  
**Status:** Active  
**Claim:** Absolute Liv HUB  
**Standing policy (amended 2026-09-03):** No new top-level `/skills/agentify`. Agentify is a first-class subscale at `image-pipeline/references/modules/agentify/` that *is* inbound menu B AGENT. Verb is live. Engine twin still forbidden. IP-WQ-094.

## What we just did

Ran a three-turn visual test then a hybrid of those three turns on a second cosplay (Z52 summer skin → nun costume), using user screenshots as inbound because YouTube playback is bot-blocked and cookies.txt is missing.

Proven:
- Overlay / edit_image holds identity.
- Generate / text-to-image makes cousins (bob wig, lost cross, wrong woman).
- Pack filters work as style layers on overlay; Sorayama chrome is intentional, not identity.
- Keep path writes the local triple.
- Step 6 Drive flush works only when the agent uploads jpeg+prompt+keep and marks all three IDs. Gate went 18 → 0.

## What we were trying to do

Crossover verbal + text + video stills into the existing inbound factory (IP-WQ-080). User asked for an “agentify pipeline.” Correct answer: B AGENT, not a third merge engine.

## Where the key artifacts are

- Lessons: `image-pipeline/references/work-queue/items/LESSONS_2026-08-29_HYBRID_Z52_NUN.md`
- Tickets: IP-WQ-080 (updated), 081 cookies, 082 deterministic step6, 083 show-pixels, 084 overlay-vs-generate
- Lake: https://drive.google.com/drive/folders/1_1xhWdBagAlUi-_g1MaksTE36fewmU1-
- Session note: `artifacts/rendered/NUN_HYBRID_SESSION_20260829-1646.md`

## What we were heading towards

Deterministic Python for pack-apply, yt-inbound, and a Step 6 closer that refuses “saved” unless `--gate` exits 0. Cookies unlock ffmpeg stills so we can score overlays against the actual short.

## Current momentum

Pause. Lake green. Waiting on `artifacts/cookies.txt`. Next hop after cookies is IP-WQ-081, not more generate cousins.

## Other considerations

- World owns YT ingest (claim-runtime scripts). Image-pipeline owns stills after they hit disk.
- `render_file` on rendered jpeg is the show contract (IPQ-079). Imagine components are rescue only.
- Do not stand up `modules/agentify-engine/`.

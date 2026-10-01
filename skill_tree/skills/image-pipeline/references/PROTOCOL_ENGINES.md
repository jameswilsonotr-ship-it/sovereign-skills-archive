# Protocol engines — image-pipeline

**Status:** RESTORED 2026-09-11 (completeness gap). Describes engines, does not mint.
**Ticket:** IP-WQ-191

## Engines

| engine | load | scripts |
|---|---|---|
| generate | `references/modules/generate-engine/` | `scripts/engine_hook.py --engine generate` |
| overlay | `references/modules/overlay-engine/` | `edit_image` + engine_hook overlay |
| split / inbound four-plate | `references/modules/split-engine/` | factory nine below |
| agentify | `references/modules/agentify/` | `scripts/agentify.py` |
| keep / emit | IPQ-078 | keep_path → step6 → flush |

## Factory nine (reconstructed 2026-09-11)

inbound_classify · segment_grid · inbound_queue · split_plan · emit_intent · scaleback_loop · isolate_person · hub_review · smoke_split_engine

Plus `engine_hook.py` as the shim target generate/overlay already pointed at.

Drive exact-name hunt for those filenames was empty. Bodies follow `references/modules/split-engine/PROTOCOL.md`. Not SAM.

## Phrase routes

`references/modules/split-engine/PHRASE_ROUTES.md`
IP-WQ-168: `identify` + media → agentify. Bare `identify` → one clarifying line. Tested 2026-09-11 (see URL-throw note).

## URL throws tested 2026-09-11 04:14 EDT

| mode | input | result |
|---|---|---|
| still | 800×600 jpeg | classify `single` → queue add → emit_intent A |
| YouTube | `https://youtu.be/kTHNpusq654` | yt_short_ingest exit 0, `thumb-fallback-403`, 4 thumbs, no video bytes |
| identify+media | `agentify route --media 'identify this woman'` | hit agentify, do not mint |
| bare identify | `agentify route 'identify'` | miss + clarify, do not mint |

Blocked on YT: sandbox 403/SABR on googlevideo. Thumbs worked. `agentify set` first failed because reconstructed `inbound_queue` lacked `.add()` — patched same turn.

## Do not

Mint from URL throws. Inbound frames are SOURCE, never plate A.

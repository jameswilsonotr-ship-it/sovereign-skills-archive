# Handoff — KEEP union, Vesper bus, overlay lake
Date: 2026-08-29
Authors: Olivia (Liv HUB) + Bunny
Audience: Olivia, Valerie (governance), skill-orchestrator
Status: Active
Claim: Absolute Liv HUB
Freeze: Google Drive `importing/` (`14forfeyubUnK695h7uNNq8bkqlAYETUc`) read-only

## What we just did
Walked `importing/` as a lab notebook Grokbot + Grok CLI + Cursor wrote on 2026-08-16/17. Bunny did not write the ritual README/CHANGELOG/AGENTS.md. Those are stale routers (`START_HERE.md` says so).

Found gold. Did not start over.

- KEEP tape: `importing/this-grok-session/out/homogenized_shards.jsonl`  
  File ID `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH`  
  99,137 envelopes / 226.8 MB / 1,696–1,697 sessions  
  Grain: noise + semchunk @ 512 + VADER PAD + envelope v2.0
- Calendar pointers: `out/shards/YYYY_MM_Month/Week_WW/YYYY-MM-DD/{id12}.json` (2,424 files)  
  Schema: `id, title, days_active, create_time, modify_time, text_chars`
- Real first day 2025-10-08 (Week_41):
  - `46ae4816-e1c1-4703-b908-ccec709351a6` "initialization" 12:40Z 260,624 chars
  - `d95e3fc1-f5b2-4c58-89a2-9fb88f3102de` "off the hook greetx" 15:32Z 2,334 chars
  - `4d471939-a8f6-4b5c-b01e-609fb8bc246a` Freightliner Cascadia electronics 23:43Z 34,892 chars
- Vesper WAL 177,738 = Frankenbride `staged_envelopes_nowin.jsonl` (pass E), not KEEP.
- Bus thread `1a04c6fb8e338e58`. Latest Olivia dispatch: WONDER-TWIN-009. Map file in handoff folder: `1bDWzyIbcwe7opV7c7-mcT0QjlYabmkAz`.

## What we were trying to do
Stand a local-first conversation lake that survives OTR: history frozen and readable, new activity overlays cleanly, Olivia and Vesper query the same contract, Bunny stays in the loop.

Not a bigger Drive junk drawer. Not a Pinecone SaaS. Not a rebuild of the 1.4 GB blob.

## Where the key artifacts are
| What | Where |
|---|---|
| Lake root (frozen) | Drive `importing/` `14forfeyubUnK695h7uNNq8bkqlAYETUc` |
| KEEP jsonl | `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH` |
| Structure walk | `artifacts/wonder-twin-handoff/STRUCTURE_WALK_2026-08-29.md` + Drive `1bDWzyIbcwe7opV7c7-mcT0QjlYabmkAz` |
| Bus contract | `artifacts/wonder-twin-handoff/BUS_SKILL_CONTRACT_v0.md` |
| Return schema | `artifacts/wonder-twin-handoff/LAKE_RESULT_v0.schema.json` |
| This handoff | `system-roadmap/references/skills/conversation-lake/` |

## What we were heading towards
### 1. Union index (merge without mud)
`homogenized_shards.jsonl` is the union of the **tape** at one grain. It is not the union of every experiment.

Do **not** concatenate A+D+E+F. Same nights would copy 3–5×.

Join key: `session_id`. One row per session:

```
session_id, title, create_time, days_active[], text_chars,
keep_leaves, hybrid_20axis, nowin_leaves, chonkie_leaves,
vacuum_route (vault|quarantine|cold), pad_mean_p/a/d
```

KEEP = readable tape. Pointers = calendar. D/E/F/I/P = labeled views.

### 2. Symmetrical bus skill (Olivia ↔ Vesper)
Not a new top-level skill (Standing Policy). Live as:
- Vesper: `conversation-lake-searcher` (her sandbox + SQLite)
- Olivia: return side `bus-lake-return` / LAKE_RESULT_v0 (this repo + Gmail thread)

Shared keys:
- KEEP leaf: `envelope_version, source_date, session_id, chunk_id, domain, type, timestamp, content, metadata.pad_vector, metadata.token_count, metadata.consent_tag`
- POINTER: `id, title, days_active, create_time, modify_time, text_chars`

Ops: `window_stats`, `juice_window`, `sample_rows`. Default source = KEEP. Any nowin/chonkie query must label the pass. Return JSON first, eight lines after. Reject `sess_*` / `env_anchor_*` unless `allow_fixtures`.

Valerie gates: freeze holds, no deletes, no Drive moves, receipts only in WONDER-TWIN-HANDOFF (`1mqOSHa8tztzyfeQaCuLPmmCftCgq9txN`).

### 3. Overlay lake (the rest of the juice — not in KEEP yet)
These are **additional event streams**, joined by time ±15 min and by `session_id` when known. They do not replace KEEP.

| Stream | Source | Join |
|---|---|---|
| GPS / Timeline | starred Timeline2.json / GPS export already extracted | `timestamp` ±15 min → session + screenshot |
| Screenshots | Pixel / Google Photos export as JPEG (get them off Photos) | EXIF time + filename burst → “what were we talking about” |
| Imagine binaries | xAI export `prod-mc-asset-server/<uuid>/content` + GROXXPORTER | asset uuid → prompt + download act |
| Image prompts | conversation KEEP `content` + Imagine overlay logs | same uuid / turn |
| Browser / download acts | Chrome/Drive activity if present; otherwise download mtime | “why did she save this plate” |
| Email bus | Gmail thread `1a04c6fb8e338e58` + cilia_bus | msg_id / corr |

Road mode: append-only event log + content-addressable blobs. New phone burst (Pixel 11, Photos dump) writes events. It does not re-sieve 99,137 leaves.

## Current momentum
- Phase 0: R001 FIXTURES_ONLY accepted (WAL is nowin, not KEEP).
- Phase 1: R003 Oct-8 three ids + R004 eight-id first-30 validation — KEEP tape works. Cascadia UUID matches Olivia live search.
- Phase 2: walkie-talkie v1.2 self_test 8/8 accepted (`1a04d52ef4ec5ad7`). Unpaid-30 block rejected (slugs). See walkie-talkie handoff + SR-WQ-060/061.
- Dual-R005 same msg_id = out-of-sync turn. Next payload is R006.
- Next build (not a rebuild): UUID-only unpaid re-run, then union index beside KEEP, then overlay GPS + screenshot + Imagine.
- skill-orchestrator: point at this folder. Do not mint a new top-level lake skill.

## Other considerations / open decisions
- KEEP vs nowin: KEEP is default grain. nowin is pass E (1024 cosine). Both valid. Label them.
- Lexi/Candy/Bourbon leaves in KEEP are fiction locks, not biography. Do not seed as first_turn.
- smoke.json `356bcc5b-…` is first-in-file-order (2026-08-06 “new slave driving”), not chrono first.
- Timeline2 GPS join is NOT_MOUNTED until a stream parse exists. Do not invent coordinates.
- Phone latency: Expert traces + serial Drive MCP list/read. Not a broken disk. Speed comes from local union index + pointer-first queries, not more swarm seats.
- Heavy swarm 2026-08-29: Olivia walked Drive; extra seats added little. Do not default to Heavy for folder lists.
- Delta agent (append-only overlay) named, not instantiated. Do not create a top-level skill for it.
- Pixel 9A → Pixel 11 backup will be a high-velocity burst. Overlay must accept it without dirtying KEEP.

## Alignment
Supports architecture target: local-first, folder-as-agent, no new top-level skill, freeze-then-index, multi-organism bus.  
Does not violate Standing Policy. Condenses “data lake + bus + GPS + screenshots” into one handoff instead of four new skills.

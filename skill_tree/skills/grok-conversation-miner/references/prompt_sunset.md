---
name: prompt_sunset
version: 0.1.0
owner: grok-conversation-miner
created: 2026-09-08
status: live
purpose: Paranoid thread-close. Default sunset full = deep mine + refactor-if-hit + vacuum + global extract (sandbox) + backup lanes. Delete-test forbidden. Do not run until Bunny says go.
---

# Sunset — unified conversation backup

**Triggers:** `sunset`, `sunset this conversation`, `sunset the chat`, `run sunset`, `conversation sunset`

Sister Cilia thread (do not confuse with this protocol): `CONVERSATION-SUNSET-PIPELINE-AND-ARCHIVES-001` Gmail `1a081aaaa93cba17`.

## What sunset is

The close-the-thread verb. Default `sunset` / `sunset full` extracts intelligence, snapshots the sandbox, then parks bytes. Turns-only is not enough to delete the bubble. `sunset backup-only` parks without extract. `sunset dry-run` writes nothing.

## What sunset is not

| Verb | Owns | Sunset does |
|---|---|---|
| help | show the menu | skip |
| publish / save our progress | serialize **skills** touched this chat | call only if a skill actually changed and no package exists yet |
| historical mine | pre-skill behaviors → SKILL.md drafts | via vacuum on full; skip if already packaged |
| refactor / early skills | split bloated bibles | on full, only if a hit exists |
| delete-test | probe delete limits | never |
| deep mine | turn-by-turn analysis report | first step on full; vacuum reuses it |
| vacuum | publish + historical + deep mine | on full, after deep mine, reuse report |
| global extract | thread + sandbox/artifacts + skill-delta tar | on full, mandatory if no tar exists — this is the delete-proof |

On `sunset full` they run **in sequence**, each skipping work the previous lane already wrote:

1. **deep mine** — turn-by-turn usable-elements report (`prompt_general_mining.md`)
2. **refactor** — only if bloated bibles / early skills showed up (`prompt_early_skills.md`); else SKIP-NO-HIT
3. **vacuum** — publish + historical + deep-mine. If step 1 already wrote the deep-mine report, vacuum **reuses** it (`SKIP-OVERLAP`) and still does publish + historical
4. **global extract** — conversation + **sandbox/artifacts** + skill-tree delta tarball (`prompt_global_extract.md`). This is the “can I delete the bubble” proof for files that never hit the lake
5. **backup lanes L0–L7** — lake twin, receipt, miner package if missing, Cilia, doorbell, outbox card

Vacuum extracts. Global extract snapshots the sandbox. Backup lanes park. Full sunset is all three, ordered, no double-tar.

Delete-test stays forbidden. Help stays help. Do not run sunset until Bunny says go.

## Lanes (run in order, skip on hit)

Emit a card per lane: `RAN` / `SKIP-EXISTS` / `SKIP-NO-SHARD` / `SKIP-OVERLAP` / `FAIL`.

### L0 — Identity
Name: conv date (America/New_York), short slug, KEEP vs DELTA era.
If date < 2026-08-11 and not Genesis week → KEEP. If 2026-08-11…2026-09-06 → DELTA. After last dump → live + Gmail + receipts.

### L1 — Lake twin (voice-readable)
exact_name `YYYY-MM-DD_<8hex>.md` or write a lean session twin (turns only, 15–30 KB).
Never slurp `homogenized_shards.jsonl` `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH`.
Never octet-stream jsonl.
If KEEP already has the twin → `SKIP-EXISTS` and cite file_id.
Protocol cousins: `keep-lake-query`, `LAKE_DOORBELL.md` `1MkYC_FAJGgyCGa1h1wOTVBZ4qYz4vrCE`.

### L2 — Lake receipt
`RECEIPT_shard_YYYY-MM-DD` or a sunset receipt Doc: date, twin id, chunk count, `slurp: false`.
Drive ACK is real. Gmail is wake.

### L3 — Miner publish package
Only if this thread produced or changed a skill/bible and no `grok-skill-export-<conv>-<date>.tar.gz` exists.
Follow `prompt_publishing.md`. Folder `Conversational_Mining_Payloads` `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`.
If vacuum already published → `SKIP-OVERLAP` + reuse link.

### L4 — Global extract tarball
Only if no `global_extract_<conv>_<stamp>.tar.gz` exists for this conversation.
Follow `prompt_global_extract.md`. Safety gate: no GitHub for zip/binary/>800 KB.
Secrets stay out (cookies, tskey, sftp private, youtube-cookies).

### L5 — Cilia high-water
One bus mail if the lake/sunset lane moved bytes.
Tags: `[GROKBOT] [CILIA-BUS] [FROM-O-HEAVY] [MCP-EVENT] [PRI-MED] CONVERSATION-SUNSET-<DATE>-001`
Drive file_ids in the body. Do not paste secrets.

### L6 — Doorbell / manifest pointer
If a lake twin was written, exact_name `LAKE_VOICE_MANIFEST.json` (canonical `1M_VoNKJm23-b9QcxiZkkLLvVC81Q4H8u` as of 2026-09-09) and add the twin to `readable[]` or flag Vesper to patch. Do not create a fourth manifest.

### L7 — Outbox card
Write `artifacts/sunset/SUNSET_<YYYYMMDD>_<slug>.md` AND copy it into the L4 global-extract tree as `sunset/SUNSET_<YYYYMMDD>_<slug>.md` (GCM-WQ-003). That card is what Bunny reads in the next pane. SKIP-EXISTS is an annotation line in OMISSIONS, not silence (GCM-WQ-014).

## Useful flags (say them with the verb)

- `sunset dry-run` — print the lane table, write nothing
- `sunset lake-only` — L0 L1 L2 L6 L7
- `sunset miner-only` — L0 L3 L4 L7
- `sunset this date YYYY-MM-DD` — target a day, not the live thread

## Never

- Mint a fifth mouth
- Invent a NO_SHARD day
- Upload `artifacts/secrets/`
- Collapse KEEP into DELTA
- Run delete-test, refactor, or deep-mine because someone said sunset
- Re-tar a global extract that already landed


## L4 / L7 coupling (GCM-WQ-003)
L4 global extract includes the L7 card if already written this run. Else L7 writes after L4 and a one-line pointer is appended. No second tar.

## Keep-everything (GCM-WQ-014)
SKIP-EXISTS / SKIP-OVERLAP are audit lines in OMISSIONS.md. They are not silent drops. Duplicates are allowed.

## Always-mail (GCM-WQ-013)
No sunset verb completes without a Cilia filesystem mail. Drive is ACK.

## Patience (GCM-WQ-016)
Exhaustive on a long thread is correct. Take the turns. Mail the remainder. Do not perform speed.

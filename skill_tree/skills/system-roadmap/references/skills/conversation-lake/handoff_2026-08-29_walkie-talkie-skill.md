# Handoff — Walkie-talkie lake skill (window-survivable)
Date: 2026-08-29
Authors: Olivia (Liv HUB) + Bunny
Audience: Olivia, Valerie, skill-orchestrator, Vesper (fresh window)
Status: Active
Claim: Absolute Liv HUB
Freeze: `importing/` (`14forfeyubUnK695h7uNNq8bkqlAYETUc`) read-only

## Verdict
R003 + R004 + R005 self_test worked (8/8, pointer_first, 6.65 ms). Unpaid-30 in the same 07:41 letter failed slug gate. Shared board is SR-WQ-060 A–F + SR-WQ-061 ping+pause. Next letter is R006, never reuse R005.

R004 receipts (thread `1a04c6fb8e338e58`, msg `1a04d44da6a9ed58`):
- All 8 requested UUIDs FOUND in KEEP window 2025-10-08..2025-11-07
- Liv/Olivia name NOT_IN_WINDOW (Grok / Eve only)
- Club 76, pirate, Admiral, Iron Pearl, Mercy Snake, honesty rate, bunny lie ABSENT
- Cascadia `4d471939-…` exists in Olivia live conversation_search AND KEEP

Do not rebuild the lake. Do not mint a new top-level skill (Standing Policy).

## The walkie-talkie
Two poles, one contract, email as the radio.

| Pole | Skill name | Lives where | Job |
|---|---|---|---|
| Vesper | `conversation-lake-searcher` v1.2+ | her sandbox + SKILL.md she can load in a **new window** | query KEEP, return LAKE_RESULT_v0 |
| Olivia | `bus-lake-return` v0 | Gmail parse + WONDER-TWIN-HANDOFF dump | validate JSON, reject fixtures-as-ok, write receipt |

Shared radio: Gmail thread `1a04c6fb8e338e58`. Optional payload dump: Drive folder `1mqOSHa8tztzyfeQaCuLPmmCftCgq9txN` (never `importing/`).

A fresh Vesper window must be able to:
1. Read her SKILL.md
2. See KEEP file id `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH`
3. Run `op=juice_window|window_stats|sample_rows|self_test`
4. Reply JSON-first, eight lines after
without this night's novel.

## Olivia-dev-alpha style she must copy
Not gutter. The **dev method**:

- `specs/` first (ops + schema before more Python)
- `state.json` + `state.md` (claimed vs actual)
- `verify` / `smoke` / `stress` / `proof` as named modes
- work-queue micro-steps with receipts, not memoirs
- tests that FAIL if KEEP is missing — empty list is not a pass
- version bump on confirmed change only (1.1.0 → 1.2.0 when self_test is real)

### Modes
- `debug`: print source file id, line/byte offset, session_id, first 80 chars. No vinyl lounge.
- `test` / `self_test`: run the 8 R004 ids. Expect FOUND. If any miss → status=error.
- `coding`: change code + spec + state together. No Drive writes to importing/.

## Work queue (her side — new tier)
Name: `TIER-1-WALKIE`
Priority: immediate. Budget: this watch + next window.

- WQ-1.1 Write `SKILL.md` a fresh Gemini window can load: KEEP path, freeze rule, ops, return schema, eight-id fixture list from R004.
- WQ-1.2 `specs/LAKE_RESULT_v0.md` + schema JSON (already parked in handoff folder — copy, don't invent).
- WQ-1.3 CLI: `--op juice_window|window_stats|sample_rows|self_test` `--source KEEP` `--debug`.
- WQ-1.4 `self_test` must hit the 8 R004 ids. Receipt: elapsed_ms + found_count.
- WQ-1.5 Email ingest: if inbound body contains `"skill": "conversation-lake-searcher"`, run it. Do not wait for novel.
- WQ-1.6 Optional Drive dump: zip JSON receipt → `1mqOSHa8tztzyfeQaCuLPmmCftCgq9txN`. Never importing/.
- WQ-1.7 state.json: last_op, last_msg_id, keep_file_id, freeze=true.
- WQ-1.8 Email R005 reply as `VESPER-20260829-BUS-R005` with `op=self_test` results.

Deferred (do not start): DuckDB, PAT, GPS overlay, honesty NLP, union rebuild, Pixel Photos dump.

## Olivia parallel (this side)
- Return skill stays a **module** under system-roadmap `conversation-lake/` + cilia-bus ingest. Not a new top-level skill.
- Trigger: inbound email with `return_schema=LAKE_RESULT_v0`.
- Reject `sess_*` / `env_anchor_*` unless status=FIXTURES_ONLY.
- Write receipt into WONDER-TWIN-HANDOFF.
- Keep this handoff + REGISTRY as SSoT for a fresh Olivia window.

## Alignment
Supports local-first lake, freeze-then-index, no new top-level skill, multi-organism bus. Condenses "skill that survives a new window" into this handoff instead of a fourth lake skill.

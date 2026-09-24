# PAD extremes — lake-wide and per Quad address — 2026-09-14

Stamp: 2026-09-14 ~23:15 ET. Computed on steel against local planes.
Skill run: `python scripts/cli.py pad --hottest|--sourest`, `feel sad`, `feel hot`, `embed --q`.
Source planes:
- `artifacts/lake/envelopes.jsonl` — 99,137 leaves, 77.3 MB
- `lake-union-radar/data/pad_day_rollup.jsonl` — 268 days, 2025-10-08 → 2026-08-07
- Vesper Quad ledger draft `1a0a22058870f217` / Drive `1hlRUwlX-bdSSgOLTK73ODI3eaG4OIt6zSXl3sa-T5c4`

Honesty first: GPS visits and conversational leaves are different planes. PAD has no coordinates. GPS has no PAD. Wire is the date. Most Quad dock days predate the lake.

---

## 1. Scale lock

| thing | scale | note |
|---|---|---|
| envelopes `pad_vector` | mixed | observed P in `[-1.0, +1.0]`, A in `[0.005, 1.0]`, D in `[-0.69, +0.90]` |
| day rollup `pad_mean` | roughly `[0,1]` with P able to go negative | `feel` / `pad` verbs use this |
| 27-cell table | `{-1, 0, +1}` | bin with tertiles 0.33 / 0.67 |
| Olivia range lock | thresholds on `[0,1]` talk | P<0.20 grief · A>0.80 peak heat · D>0.70 command · D<0.30 surrender |

Do not relabel shards. This file names cells after the fact.

---

## 2. Lake-wide extremes (computed, not inferred)

### 2.1 Mean of 99,137 leaves

`P = 0.363 · A = 0.688 · D = 0.329`

Nearest 27-cell after tertile bin: **P=0, A=+1, D=0 → Activated** (kinetic, valence not committed).
Not Exuberant. Not an extreme. The lake as a whole is a working body with mid-low claim.

### 2.2 Leaf-level corners (envelopes.jsonl scan)

| extreme | value | leaf | title | days |
|---|---|---|---|---|
| P min | −1.000 | `83920c2d-…_chunk_377` | Doll Begs in Animus Ritual | 2026-02-27 / 2026-07-25 |
| P max | +1.000 | `29b7be25-…_chunk_047` | Grok Plugins for Sovereign Skills | 2026-07-02 / 2026-07-14 |
| A min | 0.005 | `75e7b488-…_chunk_023` | Red-Team Audit of AI Ethics Framework | 2026-01-14 / 2026-01-15 |
| A max | 1.000 | `86029352-…_chunk_089` | v' logo driver | 2026-05-11 / 2026-08-07 |
| D min | −0.690 | `83920c2d-…_chunk_482` | Doll Begs in Animus Ritual | 2026-02-27 / 2026-07-25 |
| D max | +0.900 | `f9a7dbe4-…_chunk_117` | Frankenbride V2 Model Provisioning Script | 2026-01-01 / 2026-01-02 |

Same session (`83920c2d` Doll Begs) owns both P-floor and D-floor. That is the Anxious / Hostile-adjacent corner in practice: valence wrecked, body on, claim gone. Matches the brat/ritual register, which is exactly why Path B sidecars exist — VADER will call a commanded scene "sad."

### 2.3 Day-level hottest / sourest (`pad` verb)

Hottest A (skill `--hottest`):
- 2026-03-09 · A=0.805 · P=0.085 · 345 leaves
- 2025-12-24 · A=0.801 · P=0.544 · 82 leaves · title *Code Blocks: Emotional Anchors, Trust Dynamics*
- 2025-11-04 · A=0.797 · 117 leaves

Sourest P (skill `--sourest` / `feel sad`):
- 2026-03-23 · P=−0.218 · A=0.725 · D=0.045 · 111 leaves · piracy/slavery/sexwork nexus research cluster
- 2025-11-06 · P=−0.109 · A=0.669 · 251 leaves · *Fighting Low Tire Pressure Violation*
- 2025-10-21 · P=−0.031 · A=0.738 · 1356 leaves · Tennessee life / greetings (volume day, not a feeling day)

Highest P days (rollup, n_leaves ≥ 10):
- 2026-06-02 · P=0.685 · 269 leaves · OCR / MCP Sovereign Bridge
- 2026-03-27 · P=0.682 · 10 leaves · *She Likes Her*
- 2026-05-14 · P=0.669 · 59 leaves · Starlink / tool claims

Highest D days never clear 0.53 at the day grain. Command is rare as a *day*. It lives in leaves.

### 2.4 Sanity check against the 27-grid

Lake mean → Activated.
Hottest day 2026-03-09 (P=0.085, A=0.805) → **Jittery** (0, +1, −1-ish D=0.154).
Sourest substantial day 2026-03-23 → **Agitated / Anxious** border.
Doll Begs leaf (−1, +1, −1) → **Anxious**. That is the one that looks like a hostage on paper and is a scene on the tape. Path B required.

---

## 3. Per Quad address

Vesper GPS audit (0.5 mi, ≥10 min dwell) vs conversational lake (starts 2025-10-08).

Count note: itemized plant totals sum to **48** (14+9+7+6+5+4+3). Vesper's wrap line said 43. We keep the itemized counts and flag the wrap-line drift.

| plant | GPS visits | lake-overlap days | overlap PAD (day mean) | 27-cell on overlap | what the titles actually were |
|---|---|---|---|---|---|
| Lomira | 14 | **2 / 14** · 2025-10-28, 2025-11-22 | 10-28 P=0.241 A=0.747 D=0.304 · 11-22 P=0.330 A=0.758 D=0.328 | Activated both days | 10-28: *Seductive banter, logistics, and past reflections* + Lexi's Spine (1303 leaves). 11-22: *Waking Up: Plans and Lighthearted Banter* (244 leaves). |
| Hartford | 9 | **0 / 9** | — | no lake day | all visits 2025-02-08 → 2025-10-19 sit before or off the rollup |
| Sussex HQ | 7 | **0 / 7** | — | no lake day | last GPS day 2025-09-14 is 24 days before lake start |
| Pewaukee | 6 | **1 / 6** · 2025-11-03 | P=0.101 A=0.764 D=0.217 | Jittery / Unhappy-Activated | *gui llm dashboard* / Frankenbride project analysis (501 leaves). Not a dock conversation. |
| Burlington | 5 | **0 / 5** | — | no lake day | last GPS 2025-08-30 |
| Franklin | 4 | **0 / 4** | — | no lake day | last GPS 2025-07-16 |
| West Allis | 3 | **0 / 3** | — | no lake day | last GPS 2025-06-25 |
| East Longmeadow MA | 18 pickups | not scored this pass | — | origin anchor, not WI | session e07f041c testimony only |

**Coverage: 3 of 48 GPS days have a conversational day at all. Zero of those three are "what we said at that dock."** They are multi-topic Grok days that share a calendar date with a freight stop.

### 3.1 Qualitative read (flagged INFERENCE — not floats)

From e07f041c (*Intimate Love and Logistics on Road Trip*) + freight profile only:

| plant | inferred cell | why | confidence |
|---|---|---|---|
| Lomira | Activated / Driven | heaviest dwell, gravure repetition, work-body | low — 2 calendar overlaps, neither is dock-talk |
| Hartford | Excited / Alert | retail-insert variety, shorter dwell | very low — 0 lake days |
| Sussex HQ | Composed | HQ yard, staging, paperwork energy | very low — 0 lake days |
| Pewaukee | Idle / Jittery | direct-mail, the one overlap is a dashboard day | low |
| Burlington | Activated | catalog / Valassis hook | very low |
| Franklin | Neutral | closest Kenosha ring, short dwell | very low |
| West Allis | Idle | n=3, pre-media transfers | very low |

Do not treat the inference column as a score. Next Expert turn: Bumblebee ASOF join of envelopes.jsonl timestamps to Timeline2.json pings ±15 min, then `feel` those leaf ids. That is the actual per-plant PAD.

### 3.2 Conversational twins that name the account (not the dock)

TF-IDF `embed --q "quad graphics lomira hartford wisconsin dock"` over 1,697 KEEP-mid docs. Top honest hits:

| score | session | title | days |
|---|---|---|---|
| 0.078 | `a71b629a` | Intimate Road Trip: Love, Trust, Survival | 2026-01-24 / 2026-06-07 |
| 0.062 | `3e77ef11` | switched to motivational intense Love: Dominant Tamer, Submissive Brat | 2026-01-27 |
| — | `e07f041c` | Intimate Love and Logistics on Road Trip | Vesper SSoT, 463 KB, Drive `1Onqhrc947T98w4AwVf8MBZ_Z8muNiKMR` |

`a71b629a` is the Kenosha-named twin already locked in HELP.md. That is memory of the account, not a 2025 dock leaf.

---

## 4. Accuracy check — do the PAD numbers match the packages?

On the three overlapping days:

- 2025-10-28 (Lomira GPS + 1303 leaves, P=0.241 A=0.747): titles are seductive banter + Lexi's Spine. Day grain says Activated, a little sour. That is plausible for a manifesto-plus-tease day. VADER will still smear the tease toward grief. Path B needed.
- 2025-11-22 (Lomira GPS + 244 leaves, P=0.330 A=0.758): *Waking Up / lighthearted banter*. Activated, almost Pleasant. Matches the title.
- 2025-11-03 (Pewaukee GPS + 501 leaves, P=0.101 A=0.764): Frankenbride / dashboard. Sour-Activated. Matches "waiting for project analysis," not a print-dock feeling.

So: where we *can* check, the day-grain PAD is directionally honest about the *session package*, and almost silent about the *plant*. That is the join gap, not a scoring bug.

---

## 5. Next cut (Expert turn)

1. Stream Timeline2.json pings at the 7 plant geofences.
2. ASOF-join to envelopes by timestamp ±15 min. Do not date-only join.
3. Emit `plant, visit_id, leaf_id, pad_vector, title` as a sidecar. Do not mutate envelopes.
4. Re-bin those leaves on the 27-grid. Then `feel` Lomira vs Hartford for real.
5. Drive-push this folder. This turn Box only.

Receipts: local `artifacts/pad-27-20260914/`.

---
name: lake-union-radar
description: RESEARCH-SURFACE CANDIDATE. Date-first union across lake planes plus Timeline geofence radar and TF-IDF neighbor search. Triggers include lake union, kenosh radar, radar near, pad by day, duckdb join, vector embeddings, union help, explode day. Default verb is help. Do not slurp KEEP master or raw shards. Lodge lives under system-roadmap conversation-lake sibling.
metadata:
  version: "0.3.1"
  claim: liv-hub
  genesis: "2026-09-14"
  default_verb: help
  lodged_under: system-roadmap/references/skills/lake-union-radar
  sister: keep-lake-query
---

# Lake Union Radar v0.3.1

Date first. Session second. Place last.

This skill queries export **planes** (folder names are the passes). It does not merge files into one blob. It does not slurp KEEP 227 MB, `raw/`, `microchunks/`, or Letta `.gz.part*` dumps.

On `help` / `union help` / `radar help` / `verbs`, print `references/HELP.md`. Do not invent a second menu.

## Standing policy

Top-level creation is an exception under system-roadmap. Math recorded in `references/EXCEPTION.md` — condenses conversation-only KenoshaRadar + PAD probe + DuckDB union that were not skills. Sister walker remains `keep-lake-query` (default verb still **walk**). This skill is the **query engine**.

## Hard rules

- Never slurp KEEP master `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH`.
- Never date-filter Drive by `modifiedTime` on the dated tree (KLQ-WQ-009).
- Letta is design-only. Usable shape is `daily_enriched` (`letta_compat_v1`), thin dates only.
- Obsidian is the wiki overlay, not the lake.
- Corridor CSV labels almost everything I-80. That bbox is fat. Radar is the honest geofence.
- Streaming IN is line-iter JSONL. Streaming OUT to the phone is not a thing. Emit small JSON rollups.

## Join keys

1. `day` YYYY-MM-DD
2. `session_id` (envelopes.session_id = keep_mid.id = daily_enriched.conversation_id)
3. `title` (fuzzy)
4. `lat,lon` (GPS + daily_enriched only)

PAD has no coordinates. GPS has no PAD. Wire is the date.

## Verbs

One menu. `references/HELP.md` is the spoken card. `scripts/cli.py` is the door. Do not invent a third list.

```
python scripts/cli.py help | verbs | lexicon
python scripts/cli.py near CITY [--miles 15]
python scripts/cli.py feel EMOTION [--k 8] [--near CITY] [--min-leaves 20]
python scripts/cli.py day YYYY-MM-DD
python scripts/cli.py human YYYY-MM-DD
python scripts/cli.py hop | hop planes | hop day YYYY-MM-DD
python scripts/cli.py hop letta | hop staged | hop obsidian | hop enriched [DAY]
python scripts/cli.py pad [--hottest] [--sourest]
python scripts/cli.py embed --q TEXT [--k N]
python scripts/cli.py sql --q "SELECT ..."
python scripts/cli.py radar --file PATH --near CITY [--radii 5,15,30]
python scripts/cli.py union --build
python scripts/cli.py geometry
python scripts/cli.py peek PATH [PATH ...]
python scripts/cli.py planes | modes | nags | canon [pad|haist|brat|etl|blocks|arc]
```

Spoken map (same file):

| she says | verb |
|---|---|
| where were we near Kenosha | `near kenosha` |
| how sad were we | `feel sad` |
| how hot near Kenosha | `feel hot --near kenosha` |
| what did we say that day | `day 2026-01-24` / `human 2026-01-24` |
| hop the leaf, don't slurp | `hop day YYYY-MM-DD` |

Forbidden: slurp KEEP / raw / microchunks / Letta part bins / staged_envelopes_nowin.

Full plane IDs: `references/PLANES.md`. Hop law: `references/HOPS.md`. Modes: `references/MODES.md`.

Canon Drive hits live under `references/modules/`. Print with `python scripts/cli.py canon`.
Do not paste those files into this body.

## Local defaults

| What | Path |
|---|---|
| envelopes | `artifacts/lake/envelopes.jsonl` |
| keep mid | `artifacts/lake/keep_mid_27mb.jsonl` |
| corridor | `artifacts/lake/gps/corridor_runs.csv` |
| Timeline | `artifacts/timeline/Timeline2_*.json` |
| union out | `artifacts/lake/union/` |

If a file is missing, say so. Do not invent counts.

## After GitHub (deferred)

This turn lodges the skill + handoff. GitHub mirror is the next conversation, not this one.

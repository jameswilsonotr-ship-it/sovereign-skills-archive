# Handoff — date-first lake union + Kenosha radar
Date: 2026-09-14
Authors: Olivia (Liv HUB) + Bunny
Audience: system-roadmap, skill-orchestrator, keep-lake-query
Status: Active
Claim: Absolute Liv HUB

## What we just did
Stood `lake-union-radar` v0.1.0 as a query engine sister to `keep-lake-query`.
Streamed PAD envelopes (99,137) + KEEP mid (1,697) + Timeline geofence.
Kenosha 15 mi lock — only 2026-01-24 has PAD leaves (116 / 3 sessions).
Built SQLite union + numpy TF-IDF neighbor verb. DuckDB used when present.

## What we were trying to do
Stop rewriting radar/union/PAD probes every cab turn. Expose verbs. Lodge under roadmap so Standing Policy is not quietly broken.

## Where the key artifacts are
| What | Where |
|---|---|
| Skill | `/home/workdir/.grok/skills/lake-union-radar/` |
| Help | `lake-union-radar/references/HELP.md` |
| Exception math | `lake-union-radar/references/EXCEPTION.md` |
| Local lake | `artifacts/lake/` + `artifacts/timeline/` |
| This handoff | `system-roadmap/references/skills/lake-union-radar/` |

## What we were heading towards
`radar --near X` → explode day → `pad_by_day` → peek `human/YYYY/MM/weekNN/YYYY-MM-DD`.
GitHub mirror next conversation.

## Current momentum
Verbs live. Union build + embed scripts untested-on-fresh-db until this turn's harness.
Corridor CSV still fat-I-80. Radar is the honest pin.

## Other considerations
Does not replace keep-lake-query walk.
Letta remains design-only.
No neural embeddings this turn — TF-IDF cosine is labeled as such.

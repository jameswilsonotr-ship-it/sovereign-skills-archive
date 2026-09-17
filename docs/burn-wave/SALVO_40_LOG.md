# SALVO 40 Log — Included Burn

Template for CinC tracking of one included `40 + 40` salvo. This file records
operational metadata only; it is not a payload, manifest, credential store, or
message archive.

## Header

| Field | Value |
| --- | --- |
| Run ID | `RUN-YYYYMMDD-###` |
| Window (UTC) | `YYYY-MM-DD HH:MMZ — YYYY-MM-DD HH:MMZ` |
| Coordinator | `<role or handle>` |
| Wave A target | `40` |
| Wave B target | `40` |
| Total target | `80` |
| Policy | `included-only` |
| Status | `PLANNED` |

## Status vocabulary

- `PLANNED` — slot reserved, not started.
- `INCLUDED` — approved for this salvo.
- `BURNED` — included slot consumed or processed.
- `HELD` — paused; requires an explicit decision before resuming.
- `SKIPPED` — intentionally not consumed.
- `REJECTED` — excluded from the salvo.

Use one row per slot. Keep references opaque and non-sensitive, such as a
local ticket number or a short content hash. Do not paste payloads into this
log.

## Wave A — 40 included slots

| # | Included? | Status | Owner / role | Burned at (UTC) | Non-secret ref | Note |
| ---: | :---: | --- | --- | --- | --- | --- |
| 01 | [ ] | `PLANNED` |  |  |  |  |
| 02 | [ ] | `PLANNED` |  |  |  |  |
| 03 | [ ] | `PLANNED` |  |  |  |  |
| 04 | [ ] | `PLANNED` |  |  |  |  |
| 05 | [ ] | `PLANNED` |  |  |  |  |
| 06 | [ ] | `PLANNED` |  |  |  |  |
| 07 | [ ] | `PLANNED` |  |  |  |  |
| 08 | [ ] | `PLANNED` |  |  |  |  |
| 09 | [ ] | `PLANNED` |  |  |  |  |
| 10 | [ ] | `PLANNED` |  |  |  |  |
| 11 | [ ] | `PLANNED` |  |  |  |  |
| 12 | [ ] | `PLANNED` |  |  |  |  |
| 13 | [ ] | `PLANNED` |  |  |  |  |
| 14 | [ ] | `PLANNED` |  |  |  |  |
| 15 | [ ] | `PLANNED` |  |  |  |  |
| 16 | [ ] | `PLANNED` |  |  |  |  |
| 17 | [ ] | `PLANNED` |  |  |  |  |
| 18 | [ ] | `PLANNED` |  |  |  |  |
| 19 | [ ] | `PLANNED` |  |  |  |  |
| 20 | [ ] | `PLANNED` |  |  |  |  |
| 21 | [ ] | `PLANNED` |  |  |  |  |
| 22 | [ ] | `PLANNED` |  |  |  |  |
| 23 | [ ] | `PLANNED` |  |  |  |  |
| 24 | [ ] | `PLANNED` |  |  |  |  |
| 25 | [ ] | `PLANNED` |  |  |  |  |
| 26 | [ ] | `PLANNED` |  |  |  |  |
| 27 | [ ] | `PLANNED` |  |  |  |  |
| 28 | [ ] | `PLANNED` |  |  |  |  |
| 29 | [ ] | `PLANNED` |  |  |  |  |
| 30 | [ ] | `PLANNED` |  |  |  |  |
| 31 | [ ] | `PLANNED` |  |  |  |  |
| 32 | [ ] | `PLANNED` |  |  |  |  |
| 33 | [ ] | `PLANNED` |  |  |  |  |
| 34 | [ ] | `PLANNED` |  |  |  |  |
| 35 | [ ] | `PLANNED` |  |  |  |  |
| 36 | [ ] | `PLANNED` |  |  |  |  |
| 37 | [ ] | `PLANNED` |  |  |  |  |
| 38 | [ ] | `PLANNED` |  |  |  |  |
| 39 | [ ] | `PLANNED` |  |  |  |  |
| 40 | [ ] | `PLANNED` |  |  |  |  |

**Wave A count:** Included `__/40` · Burned `__/40` · Held `__/40` · Skipped `__/40`

## Wave B — 40 included slots

| # | Included? | Status | Owner / role | Burned at (UTC) | Non-secret ref | Note |
| ---: | :---: | --- | --- | --- | --- | --- |
| 01 | [ ] | `PLANNED` |  |  |  |  |
| 02 | [ ] | `PLANNED` |  |  |  |  |
| 03 | [ ] | `PLANNED` |  |  |  |  |
| 04 | [ ] | `PLANNED` |  |  |  |  |
| 05 | [ ] | `PLANNED` |  |  |  |  |
| 06 | [ ] | `PLANNED` |  |  |  |  |
| 07 | [ ] | `PLANNED` |  |  |  |  |
| 08 | [ ] | `PLANNED` |  |  |  |  |
| 09 | [ ] | `PLANNED` |  |  |  |  |
| 10 | [ ] | `PLANNED` |  |  |  |  |
| 11 | [ ] | `PLANNED` |  |  |  |  |
| 12 | [ ] | `PLANNED` |  |  |  |  |
| 13 | [ ] | `PLANNED` |  |  |  |  |
| 14 | [ ] | `PLANNED` |  |  |  |  |
| 15 | [ ] | `PLANNED` |  |  |  |  |
| 16 | [ ] | `PLANNED` |  |  |  |  |
| 17 | [ ] | `PLANNED` |  |  |  |  |
| 18 | [ ] | `PLANNED` |  |  |  |  |
| 19 | [ ] | `PLANNED` |  |  |  |  |
| 20 | [ ] | `PLANNED` |  |  |  |  |
| 21 | [ ] | `PLANNED` |  |  |  |  |
| 22 | [ ] | `PLANNED` |  |  |  |  |
| 23 | [ ] | `PLANNED` |  |  |  |  |
| 24 | [ ] | `PLANNED` |  |  |  |  |
| 25 | [ ] | `PLANNED` |  |  |  |  |
| 26 | [ ] | `PLANNED` |  |  |  |  |
| 27 | [ ] | `PLANNED` |  |  |  |  |
| 28 | [ ] | `PLANNED` |  |  |  |  |
| 29 | [ ] | `PLANNED` |  |  |  |  |
| 30 | [ ] | `PLANNED` |  |  |  |  |
| 31 | [ ] | `PLANNED` |  |  |  |  |
| 32 | [ ] | `PLANNED` |  |  |  |  |
| 33 | [ ] | `PLANNED` |  |  |  |  |
| 34 | [ ] | `PLANNED` |  |  |  |  |
| 35 | [ ] | `PLANNED` |  |  |  |  |
| 36 | [ ] | `PLANNED` |  |  |  |  |
| 37 | [ ] | `PLANNED` |  |  |  |  |
| 38 | [ ] | `PLANNED` |  |  |  |  |
| 39 | [ ] | `PLANNED` |  |  |  |  |
| 40 | [ ] | `PLANNED` |  |  |  |  |

**Wave B count:** Included `__/40` · Burned `__/40` · Held `__/40` · Skipped `__/40`

## Closeout

| Field | Value |
| --- | --- |
| Total included | `__/80` |
| Total burned | `__/80` |
| Total held | `__/80` |
| Total skipped / rejected | `__/80` |
| Final status | `OPEN` / `CLOSED` / `ABORTED` |
| Closed at (UTC) |  |
| Closeout owner |  |

### Decision notes

Record only non-sensitive decisions, blockers, and next actions. Link to a
separate approved system of record with a non-secret reference when needed.

## No-secrets guard

Never record passwords, API keys, access tokens, cookies, private URLs,
encryption keys, personal data, raw payloads, or confidential message contents
in this file. If a secret appears here, remove it from the working copy,
rotate or revoke it through the approved process, and record only the
non-sensitive incident reference.

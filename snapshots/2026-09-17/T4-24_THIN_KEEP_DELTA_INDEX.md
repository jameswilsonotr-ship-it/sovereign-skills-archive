# T4-24 — Thin-Keep Delta Companion Index

This is the small, repository-local companion index for T4-24. It records the
delta that must remain in the reload surface without copying the source
payload.

| field | value |
|---|---|
| status | `CONTINUOUS_INCLUDED` |
| reload | `included` |
| source | `offline-local` |
| payload policy | index and pointers only |
| fallback | none |

## Included delta

| path | role | disposition |
|---|---|---|
| `snapshots/2026-09-17/AWESOME_SPLIT_LEDGER.md` | split-ledger context | keep in the continuous reload surface |

The index itself is the companion record for this delta. No additional
payload, network dependency, credential, or alternate reload path is part of
T4-24.

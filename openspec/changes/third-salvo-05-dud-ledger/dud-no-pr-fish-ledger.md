# THIRD_SALVO T3-05 — dud/no-PR fish ledger

This is an offline fixture for candidates that fell through the Tube-2
surface. A seed row is a record of a missing artifact, not evidence that a
candidate exists or that a provider was searched.

## Locked contract

| Field | Value |
| --- | --- |
| change_id | `third-salvo-05-dud-ledger` |
| salvo | `THIRD_SALVO` |
| slot | `T3-05` |
| lane | `Ultra` |
| state | `included` |
| on-demand | forbidden |
| default disposition | `dud` / no PR |
| evidence mode | offline only |

## Seeded Tube-2 gaps

The five rows below are deliberately candidate-free. Replace only the
placeholders during a separately authorized review; do not infer a hit from a
blank field.

| fish_id | Tube-2 gap seed | candidate / query | lane | state | disposition | evidence_status | pr_status | evidence pointer | reviewer note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `T2-G01` | Missing canonical identity: no stable title/URL pair | `[not supplied]` | `Ultra` | `included` | `dud` | `unverified` | `none` | `[none]` | `[record what would establish identity]` |
| `T2-G02` | Missing source proof: no reviewable capture or receipt | `[not supplied]` | `Ultra` | `included` | `dud` | `unverified` | `none` | `[none]` | `[record the missing proof]` |
| `T2-G03` | Ambiguous match: candidate cannot be tied to the requested Tube-2 gap | `[not supplied]` | `Ultra` | `included` | `dud` | `unverified` | `none` | `[none]` | `[record the disambiguation needed]` |
| `T2-G04` | Availability unresolved: status cannot be verified offline | `[not supplied]` | `Ultra` | `included` | `dud` | `unverified` | `none` | `[none]` | `[record the authorized verification step]` |
| `T2-G05` | Handoff incomplete: no reviewable no-PR receipt exists | `[not supplied]` | `Ultra` | `included` | `dud` | `unverified` | `none` | `[none]` | `[record the handoff artifact needed]` |

## Entry template

Copy this block for a later, authorized row. Keep the locked fields unchanged.

```yaml
fish_id: T2-G##_candidate-##
change_id: third-salvo-05-dud-ledger
salvo: THIRD_SALVO
slot: T3-05
lane: Ultra
state: included
disposition: dud
candidate_or_query: "[fill only from an authorized offline fixture]"
gap_seed: T2-G##
evidence_status: unverified
evidence_pointer: "[none]"
pr_status: none
reviewer_note: "[why this remains a dud]"
```

## No-PR receipt

Until a separate review authorizes promotion, the review receipt for every
seeded row is:

```text
receipt: dud/no-pr
provider_call: none
live_lookup: none
pr: none
lane: Ultra
state: included
```

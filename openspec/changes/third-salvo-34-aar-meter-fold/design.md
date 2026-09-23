# Design: T3-34 AAR meter fold

## Measurement model

The fold is a closed-world count over the post-reset measurement window:

```text
fold(records, reset_boundary) =
  count(record for record in records
        where record.window == post_reset(reset_boundary)
        and record.slot == T3-34
        and record.classification == Ultra)
```

The fold does not reinterpret a missing, unknown, or alternate classification.
In particular, `On-Demand` records are filtered out before counting.

## Reset boundary

The reset establishes a new zero baseline. The post-reset window contains only
records observed after that boundary. Pre-reset records are retained as
historical context, if available, but are not inputs to the new fold.

If a record cannot be placed on the post-reset side of the boundary, it is
excluded from this fold rather than guessed into it.

## Record shape

The AAR note should preserve these fields:

| Field | Value or rule |
|---|---|
| `change_id` | `third-salvo-34-aar-meter-fold` |
| `salvo` | `third` |
| `slot` | `T3-34` |
| `window` | `post-reset` |
| `included_classification` | `Ultra` |
| `excluded_classification` | `On-Demand` |
| `fold_baseline` | `0` at reset |
| `external_access` | `none` |

## Determinism and safety

The same post-reset input set produces the same fold. The specification does
not require network access, provider state, secrets, or a service clock.
Eligibility is based on the explicit classification in each local record.

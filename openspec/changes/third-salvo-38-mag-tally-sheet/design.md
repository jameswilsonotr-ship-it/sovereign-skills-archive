# Design: T3-38 Mag Tally Sheet

## Record shape

The template has a header and a row-based tally:

| Field | Rule |
|---|---|
| Change ID | Fixed to `third-salvo-38-mag-tally-sheet` |
| Salvo | Fixed to `THIRD_SALVO` |
| Slot | Fixed to `T3-38` |
| Inclusion class | Fixed to `INCLUDED_ULTRA` |
| Tally row | One auditable count with a short note |
| Total | The sum of accepted row counts |

Each row contains:

- a row number;
- a date or local run marker;
- a short item or batch reference;
- a non-negative integer count;
- an optional note; and
- verifier initials.

## Invariants

- Every accepted row is `INCLUDED_ULTRA`.
- Counts are whole numbers greater than or equal to zero.
- The total equals the sum of accepted row counts.
- A blank, rejected, or excluded row is not included in the total.
- On-Demand is never a valid row class and never contributes to the total.
- The sheet remains understandable and reconcilable without a network
  connection or a separate system.

## Review flow

1. Copy the template for the T3-38 tally period.
2. Fill in the header and one row per accepted included Ultra count.
3. Leave any non-eligible request out of the tally and record a short
   exclusion note only if an audit trail needs it.
4. Sum the accepted rows.
5. A second person checks the row arithmetic and initials the sheet.

## Deliberate non-goals

- No live counter or synchronization.
- No automatic conversion between inclusion classes.
- No account, credential, or service integration.
- No change to allocation policy beyond documenting this slot's eligibility.

The sheet is intentionally offline-first: its rules, fields, and
reconciliation steps are all contained in the Markdown document.

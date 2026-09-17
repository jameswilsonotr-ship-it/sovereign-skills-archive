# Change: T3-38 Mag Tally Sheet

- **Change ID:** `third-salvo-38-mag-tally-sheet`
- **Salvo:** `THIRD_SALVO`
- **Slot:** `T3-38`
- **Eligibility:** `INCLUDED` / `Ultra` only

## Problem

T3-38 needs a small, auditable way to count Mag units that are part of the
Ultra inclusion. Without a fixed sheet, entries can be mixed with other
allocation classes or totals can be reconstructed inconsistently.

## Proposal

Add a plain Markdown Mag tally sheet template and an OpenSpec change describing
its rules:

1. Each row records only an included Ultra tally.
2. The sheet has one explicit inclusion class: `INCLUDED_ULTRA`.
3. On-Demand entries are never eligible for this sheet and must not contribute
   to its total.
4. Totals are reproducible by summing the row counts and can be checked
   manually while offline.

## Scope

This is a documentation and template change. It adds no runtime behavior,
network calls, credentials, service configuration, or automated submission.

## Acceptance criteria

- The change is identified as `third-salvo-38-mag-tally-sheet`.
- The sheet is labeled `THIRD_SALVO` / `T3-38`.
- The eligibility rule says `INCLUDED Ultra ONLY`.
- On-Demand is explicitly excluded.
- A reviewer can reconcile the total from the rows using the template alone.

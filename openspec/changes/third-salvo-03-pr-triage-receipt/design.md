# Design: PR triage receipt

## Receipt shape

The receipt is intentionally a plain Markdown document so it can be pasted
into a PR body without rendering dependencies. It has four parts:

1. **Header** — immutable change, salvo, slot, and mode identity.
2. **Review boundary** — the S2-leftover source and the exact review scope.
3. **Disposition table** — one row per leftover, with a decision and evidence.
4. **Fence check** — a short attestation that the review stayed offline and
   Ultra-only.

## Decision vocabulary

Each row uses exactly one of these dispositions:

- `carry-forward` — still valid work, retained for a later explicitly scoped
  change.
- `close` — no follow-up is required, with evidence recorded.
- `needs-owner` — a human decision or owner is required before proceeding.

The receipt does not itself create work, change source files, or claim that a
follow-up was executed.

## Reviewability

The sample uses stable local identifiers and file/section evidence rather than
external URLs or provider references. A reviewer can therefore verify the
receipt from the PR diff alone. Real receipts should replace sample values
with repository-local evidence and keep the same fields.

## Safety boundary

The mode field is an assertion and a guard: it must be `Ultra`, and
`On-Demand` is not a valid value. The fence check records that no network,
provider, secret, live Vultr, or Linear-mint operation was used.

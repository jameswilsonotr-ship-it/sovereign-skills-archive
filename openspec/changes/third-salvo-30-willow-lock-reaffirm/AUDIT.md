# Willow lock reaffirmation audit

**Atomic change:** `third-salvo-30-willow-lock-reaffirm`
**Slot:** `T3-30`
**Decision:** `INCLUDED` for `Ultra` only

## Audit result

**PASS — lock reaffirmed.**

T3-30 is recorded as included for the `Ultra` surface and excluded from
`On-Demand`. This artifact is an audit record, not an implementation change.

## Evidence boundary

- Repository-local documentation was reviewed.
- The change adds OpenSpec records and this audit record only.
- No Willow `SKILL.md` content was edited.
- No executable surface was exercised.

## Reaffirmed invariant

> T3-30 is `INCLUDED` on `Ultra`; it is never available on `On-Demand`.

## Conclusion

The lock is reaffirmed for this atomic change. Any future behavior change
requires a separate, explicitly scoped change.

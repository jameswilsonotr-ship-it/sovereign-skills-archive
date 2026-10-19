# Land-line handoff — THIRD_SALVO T3-09

**To:** Mina, Bea, and Ora
**Change ID:** `third-salvo-09-land-line-handoff`
**Required PR title:** `salvo: T3-09 land-line-handoff`
**Delivery mode:** Included Ultra only

## North star

T3-09 is a documentation handoff for the land-line contract. Keep the
handoff on the Included Ultra lane. **On-Demand is never a valid mode for
this slot**: do not use it as a fallback, alias, retry path, or implied
escalation.

This note and the accompanying OpenSpec change are the complete scope. No
runtime implementation is requested.

## Handoff asks

### Mina — intake and identity

- Confirm the exact change ID:
  `third-salvo-09-land-line-handoff`.
- Confirm the lane is `THIRD_SALVO` slot `T3-09`.
- Confirm the eligibility statement reads Included Ultra only.
- Reject any request that proposes On-Demand for this slot.

### Bea — contract review

- Review the OpenSpec scenarios for the Ultra-only gate and the no-fallback
  rule.
- Verify that the delivery is documentation-only and offline.
- Verify that no hard-fenced surface is changed or introduced.
- Record any discrepancy against the OpenSpec change before handoff.

### Ora — atomic delivery and receipt

- Keep the OpenSpec change and this note in one atomic pull request.
- Use the exact title `salvo: T3-09 land-line-handoff`.
- Confirm the final diff contains no runtime, provider, secret, or
  infrastructure work.
- Return the delivery receipt with the commit and pull-request references.

These asks describe the review boundary for this handoff; they do not assign
new runtime permissions or change anyone's existing ownership.

## Hard fences

The handoff stops if any of the following is requested or appears in the
diff:

- edit to `Willow SKILL.md`;
- use or inclusion of `CONV2_B`;
- external or provider calls;
- secrets or credentials;
- live Vultr work; or
- minting a Linear item.

Keep all validation local to the repository. If a fence is encountered,
record the discrepancy and leave the slot unfulfilled rather than changing
lanes or widening scope.

## Completion check

- [ ] Mina confirms identity and Included Ultra eligibility.
- [ ] Bea confirms scenarios and hard-fence review.
- [ ] Ora confirms one atomic PR with the exact title and returns the
      receipt.

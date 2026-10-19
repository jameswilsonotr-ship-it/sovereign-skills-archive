# Proposal: T3-03 PR triage receipt

- Change ID: `third-salvo-03-pr-triage-receipt`
- Salvo: `THIRD_SALVO`
- Slot: `T3-03`
- Inclusion: `Ultra` only

## Summary

Add a small, reviewable receipt format for triaging S2 leftovers in a pull
request. The receipt records what was reviewed, the disposition of each
leftover, and the evidence a reviewer needs to verify the decision.

The format is documentation-only. It is designed for offline use and does not
invoke a provider, mint a Linear item, access Vultr, read secrets, or perform
an On-Demand run.

## Scope

### Included

- An OpenSpec change for the T3-03 receipt contract.
- A copy-ready PR triage receipt template.
- One completed sample for S2 leftovers.
- An explicit `Ultra`-only guard in the receipt metadata.

### Excluded

- Any Willow `SKILL.md` changes.
- `CONV2_B`.
- On-Demand execution or fallback behavior.
- Runtime code, integrations, network calls, credentials, and live services.

## Acceptance criteria

1. The change is present under the reserved change ID.
2. The receipt template requires `Ultra` and rejects `On-Demand` as a mode.
3. The sample is clearly labeled as S2 leftovers and is independently
   reviewable from the PR body.
4. The diff contains documentation and fixtures only.

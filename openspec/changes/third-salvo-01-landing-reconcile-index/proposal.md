# THIRD_SALVO T3-01: landing reconcile index

- **Change ID:** `third-salvo-01-landing-reconcile-index`
- **Track:** THIRD_SALVO
- **Slot:** T3-01
- **Mode:** Included Ultra only

## Intent

Create one evidence-bounded landing index for SECOND_SALVO (Tube-2) pull
requests, separating locally verified `OPEN` and `MERGED` rows. This is a
landing reconciliation receipt only; it does not change product or skill
behavior.

## Scope

- Add the OpenSpec change record and its focused receipt.
- Record the locally verifiable Tube-2 PR state at the checkout revision used
  for this change.
- Preserve an explicit evidence gap instead of inventing PR numbers or
  provider state when the offline checkout contains no Tube-2 manifest or PR
  records.

## Hard exclusions

- On-Demand work.
- `CONV2_B`.
- Any `SKILL.md` edit.
- Provider/API lookups, secrets, Vultr, Linear minting, or other networked
  reconciliation.
- Code, runtime, or behavior changes.

# Design: third-salvo-37-tube3-spent-rule

## Context

T3-37 is one slot in the Third Salvo. Its accounting must be
machine-checkable from the local change record rather than inferred from a
provider dashboard or an unverified dispatch. The lane is explicitly
**INCLUDED Ultra ONLY**.

## Goals

- Give T3-37 one stable change-id and one atomic review unit.
- Define a positive spent event and the conditions that prevent one.
- Keep the workflow offline and repository-local.
- Produce a post-land draft that can be finalized after the PR lands.

## Non-Goals

- Do not create, edit, or overwrite Willow `SKILL.md` files or skill-tree
  live-lock files.
- Do not unpack or inspect `CONV2_B`.
- Do not use external services, providers, credentials, secrets, Vultr, or
  Linear.
- Do not use On-Demand, authorize On-Demand fallback, or count On-Demand as
  included Ultra.
- Do not perform billing, quota, network, or runtime mutations.

## Decisions

1. **Lane identity:** the only lane identity is
   `third-salvo-37-tube3-spent-rule`, with slot label `T3-37`.
2. **Eligible execution class:** a qualifying dispatch MUST be explicitly
   marked `included-ultra`. Missing, ambiguous, or different execution-class
   metadata is rejected.
3. **Atomicity:** one dispatch maps to this one change-id and one PR. Sibling
   change-ids cannot be used to complete or inflate the spent record.
4. **Spent event:** Tube-3 becomes `spent` only when the scoped change is
   complete, the PR receipt is present, and the recorded execution class is
   `included-ultra`.
5. **No fallback:** an On-Demand or provider path is a hard rejection, not a
   degraded success. A rejected dispatch remains `not-spent`.
6. **Post-land state:** the draft is a template for the record after merge.
   This documentation-only PR does not claim that an external meter event
   occurred.

## State transition

```text
not-spent
   |
   | included-ultra + exact change-id + complete artifact + receipt
   v
spent

Any On-Demand/provider/secret/external attempt --> rejected (not-spent)
Any incomplete or ambiguous local record     --> pending (not-spent)
```

## Risks

| Risk | Mitigation |
| --- | --- |
| Ambiguous model or quota class | Require the exact `included-ultra` label |
| Scope creep across salvo slots | Require the exact change-id and one PR |
| False positive spend record | Require artifact completion and receipt |
| External or secret leakage | Offline-only fence and explicit rejection |

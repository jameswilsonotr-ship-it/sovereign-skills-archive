---
atom: atom-bc-02-included-only
parent_change_id: add-included-burn-chew-lanes
capability: burn-chew
visibility: meter-burn-desk
---

# Included-only burn policy

This atom is the lane brief for burning Cursor Models included quota. It
defines an accounting boundary only; it does not change entitlements,
implement a runtime, or authorize paid fallback.

The lane target is to burn eligible included quota toward approximately 80%
of the active period, subject to the stop/defer rules below; the target never
authorizes usage outside the included allowance.

## Policy

1. Every burn-chew action MUST use the active Cursor Models included quota.
2. A lane MUST stop, defer, or reduce work when included quota is unavailable,
   insufficient, stale, or ambiguous.
3. A lane MUST NOT switch accounts, billing pools, model pools, or quota types
   to continue burning.
4. The provider-reported included balance and reset boundary are authoritative;
   local estimates MUST NOT authorize usage outside the included allowance.
5. The lane owner MUST be able to attribute each burn to this lane and the
   active quota period before treating it as included usage.

## Explicit OD ban

On-Demand (OD) is already **OVER** for this burn wave. This lane MUST NOT
increase, climb, enable, reserve, borrow, or spend On-Demand capacity. OD is
not a fallback when included quota is exhausted or uncertain. Any step that
would create OD usage is out of scope and MUST be rejected before execution.
Done-when: confirm that no On-Demand increase or spend occurred.

## Lane boundary

This policy applies to the single parent change-id
`add-included-burn-chew-lanes`. The deliverable is this atom only:
`atom-bc-02-included-only`. It must remain independently reviewable and must
not require sibling atom changes.

## Hard fences

- No `SKILL.md` or skill-tree live-lock edits.
- No On-Demand spend or climb.
- No vibe-coding.
- No Google Docs.
- No `CONV2_B`.
- No CMV.
- No plating or avatar minting.

## Review closeout

Before approval, confirm that the diff contains only this policy note, the
policy names Cursor Models included quota as its sole burn source, and the OD
ban is explicit. The PR title and description must mention
`atom-bc-02-included-only`, `add-included-burn-chew-lanes`, and the
**Meter Burn Desk** tag.

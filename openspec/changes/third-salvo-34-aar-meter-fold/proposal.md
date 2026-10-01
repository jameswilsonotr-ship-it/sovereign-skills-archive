# Change: T3-34 AAR meter fold

- **Change ID:** `third-salvo-34-aar-meter-fold`
- **Salvo:** third
- **Slot:** `T3-34`
- **Eligibility:** `INCLUDED` / `Ultra` only
- **Excluded:** `On-Demand`

## Summary

Define the T3-34 after-action-review (AAR) meter fold as a post-reset,
Ultra-only measurement window. The fold includes only records explicitly
classified as `Ultra`; `On-Demand` records are never included, substituted, or
used as a fallback.

## Motivation

The slot needs a deterministic meter boundary after reset. Making the
eligibility rule explicit prevents an `On-Demand` record from changing an AAR
total or being mistaken for an included `Ultra` record.

## Scope

This change defines:

1. the T3-34 inclusion and exclusion rule;
2. the post-reset baseline for the fold; and
3. the offline AAR record needed to verify the rule.

This is a specification and recordkeeping change. It does not call providers,
read credentials, access external services, or change any skill implementation.

## Invariants

- A T3-34 fold has one eligibility class: `Ultra`.
- `On-Demand` is always excluded from the fold.
- The fold begins at the post-reset boundary and carries no pre-reset meter
  state into the new baseline.
- Unknown or unclassified records are not promoted to `Ultra`.
- The change is atomic under `third-salvo-34-aar-meter-fold`.

## Non-goals

- No `Willow SKILL.md` work.
- No `CONV2_B` work.
- No external, provider, secrets, Vultr, or Linear integration.
- No On-Demand path, fallback, or comparison meter.

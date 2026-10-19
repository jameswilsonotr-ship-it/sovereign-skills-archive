# Proposal: third-salvo-37-tube3-spent-rule

## Why

Third Salvo needs a deterministic Tube-3 rule for the T3-37 lane. The lane
must burn **included Ultra only** and must never fall back to, recommend, or
record On-Demand usage.

## What Changes

- Add the `third-salvo-37-tube3-spent-rule` OpenSpec capability.
- Define T3-37 as one atomic change-id and one reviewable PR.
- Define when Tube-3 is considered spent by rule: only after an included Ultra
  dispatch completes the scoped change and its receipt is written.
- Reject On-Demand, provider, secret, and external execution paths.
- Add a post-land draft for the Tube-3 spent-by-rule record.

## Capabilities

| Capability | Mode |
| --- | --- |
| `third-salvo-37-tube3-spent-rule` | ADDED |

## Impact

- Establishes a bounded, offline accounting rule for slot T3-37.
- Makes an incomplete, rejected, or disallowed dispatch non-spent.
- This change is documentation-only. It does not open a provider, billing, or
  network path and does not edit any `SKILL.md` file.

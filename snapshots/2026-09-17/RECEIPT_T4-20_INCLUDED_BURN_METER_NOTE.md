# Receipt — T4-20 included-burn meter note

Status: recorded
Mode: offline-only
PR title: `salvo: T4-20 included-burn-meter-note`

## Locked behavior

- T4-20 reload mode is **CONTINUOUS INCLUDED**.
- The included-burn companion meter note is **10%** (`10pct`).
- The 10% value is an informational companion note; it does not authorize a
  mode change or an alternate reload path.
- **On-Demand is forbidden**. There is no On-Demand fallback, spend, purchase,
  or billing mutation in this slice.

This receipt records the requested policy note. It does not claim a live meter
read or a live reload because this slice is offline-only.

## Fence receipt

- [x] No Willow `SKILL.md` was created, edited, or overwritten.
- [x] No `CONV2_B` was unpacked or processed.
- [x] No external runtime/provider service, secret, or Vultr surface was used.
- [x] No On-Demand path was used or enabled.
- [x] No live meter, provider, or billing action was performed.
- [x] GitHub was used only for required repository delivery: one push and one
  PR.
- [x] One focused change and one PR.

## Verification

- Scope check: this receipt is the only changed path.
- Content check: T4-20, `CONTINUOUS INCLUDED`, and the 10% companion note are
  present.
- Network check: no network-dependent verification is required or claimed.

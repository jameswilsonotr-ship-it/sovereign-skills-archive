# Design: T3-10 closeout gate

## Contract surface

The contract has four independent inputs:

| Input | Required value | Rejection condition |
|---|---|---|
| Change ID | `third-salvo-10-closeout-gate` | Any other change ID |
| Slot | `T3-10` | Any other slot |
| Inclusion lane | `INCLUDED` for `Ultra` | `On-Demand`, omitted lane, or another tier |
| Execution mode | Offline/documentation-only | Provider, network, secret, live Vultr, or Linear activity |

All four inputs must pass before the closeout can be marked `CLOSED`.

## Gate states

The checklist is intentionally monotonic:

- `OPEN`: the package exists but evidence has not passed all gates.
- `BLOCKED`: a fence failed or required evidence is missing.
- `CLOSED`: every gate passed and the receipt was written.

`CLOSED` is a documentation state. It does not authorize work, allocate
capacity, wake a worker, create a provider resource, or schedule a follow-up.

## Meter semantics

Meters are observations only. They can describe evidence such as counts,
coverage, or completion markers, but they have no execution semantics.

The invariant is:

```text
meter observation ≠ spawn authorization
meter threshold ≠ spawn trigger
meter result ≠ capacity allocation
```

No value, threshold, trend, or missing value in a meter may cause a spawn,
retry, queue release, escalation, or provider call. If an execution decision
is ever needed, it must be a separate, explicitly authorized change; it is
not part of T3-10.

## Evidence model

Evidence is local and inspectable:

- the requested change ID, slot, and lane;
- the checklist result for each fence;
- static inspection of the changed paths;
- the final receipt.

No external response, provider status, secret, live resource, or network
trace is valid evidence for this change.

## Closeout algorithm

1. Read the package metadata and confirm the reserved change ID.
2. Confirm the slot is `T3-10`.
3. Confirm the lane is `INCLUDED Ultra`.
4. Mark the meter-separation gate as passed only when no meter is wired to
   spawn or other execution behavior.
5. Mark every hard-fence gate as passed only from offline repository evidence.
6. If any gate fails, set the state to `BLOCKED` and do not close.
7. If all gates pass, set the state to `CLOSED` and write the receipt.

This algorithm has no action that can contact a provider or create work.

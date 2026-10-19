# Design

## Canonical ID

The guard compares IDs using this small, offline normalization function:

```text
canonical_id(id) = ASCII-lowercase(ASCII-trim(id))
```

No Unicode folding, punctuation rewriting, slug generation, or network lookup
is performed. IDs that are not valid OpenSpec change IDs remain invalid; this
guard only answers whether an otherwise-eligible ID collides with a reserved
one.

## Guard order

1. Read the reserved-ID set from the local change manifest or fixture.
2. Normalize the candidate and every reserved ID.
3. Reject when the normalized candidate is already present.
4. Reject when the request declares `availability: on-demand`.
5. Otherwise report `available` for this collision check.

The availability check is deliberately separate from collision detection:
`on-demand` is an invalid release lane for this change even when its ID is
unique.

## Stable result vocabulary

The fixture uses these result values:

- `collision` — the canonical ID is already reserved.
- `invalid-lane` — the requested lane is On-Demand.
- `available` — no canonical ID collision and the lane is Included Ultra.

## Non-goals

- No changes to `Willow SKILL.md`.
- No `CONV2_B` work.
- No Linear, Vultr, provider, or other external calls.
- No secret material or live deployment behavior.
- No automatic ID reservation service.

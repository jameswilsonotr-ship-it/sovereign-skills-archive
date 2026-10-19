# Design

## Additive envelope

The v2 contract adds a small, namespaced set of fields to the existing
receipt object. Existing v1 keys remain valid and are not renamed, removed, or
reinterpreted. Consumers that do not understand the new keys can continue to
read the v1 portion.

The new keys are intentionally explicit:

| Field | Type | Value for T3-24 | Purpose |
|---|---|---|---|
| `schema_version` | integer | `2` | Identifies the additive contract |
| `change_id` | string | `third-salvo-24-receipt-schema-v2` | Stable change identity |
| `salvo` | string | `THIRD_SALVO` | Salvo identity |
| `slot` | string | `T3-24` | Slot identity |
| `entitlement` | string | `INCLUDED` | Inclusion class |
| `tier` | string | `ULTRA` | Included tier |
| `on_demand` | boolean | `false` | Explicit exclusion of On-Demand |
| `execution` | object | see below | Local execution state |
| `artifacts` | array | see below | Files covered by the receipt |

`execution` contains:

| Field | Type | Value | Purpose |
|---|---|---|---|
| `network` | string | `OFFLINE` | Records execution boundary |
| `status` | string | `COMPLETE` | Records completion state |

Each `artifacts` entry contains a repository-relative `path`, a `kind`, and a
`status`. The path is descriptive metadata; it does not authorize reading or
writing outside the repository.

## Validation rules

- `schema_version` must be `2`.
- `change_id`, `salvo`, and `slot` must match the T3-24 constants.
- `entitlement` must be `INCLUDED`.
- `tier` must be `ULTRA`.
- `on_demand` must be `false`.
- `execution.network` must be `OFFLINE`.
- `execution.status` must be `COMPLETE`.
- Additional v1 and forward-compatible fields are allowed.

The machine-readable contract is in `schema.json`. The OpenSpec requirements
provide the behavioral form of the same rules.

## Rejection behavior

A receipt that has `entitlement: INCLUDED` but `tier` other than `ULTRA`, or
that sets `on_demand: true`, is invalid for T3-24. A validator should reject
it before publication. Missing v1 fields are not a v2 rejection because this
change only adds the fields listed above.

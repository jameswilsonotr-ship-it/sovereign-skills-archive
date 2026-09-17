# Receipt schema v2

## ADDED Requirements

### Requirement: Identify the T3-24 receipt

The v2 receipt MUST include `schema_version: 2`, the exact
`change_id: third-salvo-24-receipt-schema-v2`, `salvo: THIRD_SALVO`, and
`slot: T3-24`.

#### Scenario: T3-24 identity is present

- **WHEN** a T3-24 receipt is read
- **THEN** the four identity fields are present with the exact values above

### Requirement: Mark the slot as included Ultra

The v2 receipt MUST include `entitlement: INCLUDED`, `tier: ULTRA`, and
`on_demand: false`.

#### Scenario: Included Ultra classification

- **WHEN** a T3-24 receipt is classified
- **THEN** it is classified as `INCLUDED` at `ULTRA`
- **AND** it is not classified as On-Demand

#### Scenario: On-Demand classification is rejected

- **WHEN** `on_demand` is `true`
- **THEN** the receipt is invalid for T3-24

### Requirement: Record offline completion

The v2 receipt MUST include an `execution` object with
`network: OFFLINE` and `status: COMPLETE`.

#### Scenario: Offline receipt is complete

- **WHEN** the change receipt is finalized
- **THEN** `execution.network` is `OFFLINE`
- **AND** `execution.status` is `COMPLETE`

### Requirement: Preserve additive compatibility

The v2 contract MUST preserve all existing v1 fields and MUST allow additional
fields that are not defined by this change.

#### Scenario: A v1 field remains readable

- **WHEN** a v2 receipt contains an existing v1 field
- **THEN** the field remains unchanged and readable

#### Scenario: A forward-compatible field is present

- **WHEN** a v2 receipt contains an unrecognized field
- **THEN** validation does not reject the receipt solely for that field

### Requirement: Describe local artifacts

The v2 receipt MUST include at least one artifact entry. Each entry MUST
identify a repository-relative `path`, a `kind`, and a `status`.

#### Scenario: Change artifacts are listed

- **WHEN** the receipt is finalized
- **THEN** it lists the OpenSpec change artifacts covered by the receipt
- **AND** each listed path is repository-relative

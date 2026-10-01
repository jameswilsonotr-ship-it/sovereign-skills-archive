# Proposal stub hygiene

## Requirements

### Requirement: Parked IDs have explicit stub metadata

Every proposal stub for a parked ID MUST identify the canonical ID, parked
status, inclusion lane, On-Demand prohibition, and non-operational state before
any descriptive text.

#### Scenario: A reviewer opens a parked-ID stub

- **WHEN** the stub is opened
- **THEN** its first metadata block contains `id`, `status`, `availability`,
  `on_demand`, and `operational`
- **AND** the values are `parked`, `INCLUDED Ultra ONLY`, `NEVER`, and `false`
  for the corresponding fields

### Requirement: Parked stubs remain inert

A parked-ID proposal stub MUST describe a future review boundary only. It MUST
NOT create a live route, activate an ID, or imply that a parked ID is
available through On-Demand dispatch.

#### Scenario: A stub is read by a dispatch or promotion workflow

- **WHEN** the workflow encounters `status: parked`
- **THEN** it treats the record as descriptive input
- **AND** it does not dispatch, activate, or promote the ID

### Requirement: Stub identity is deterministic

A proposal stub set MUST contain one entry per canonical parked ID. Duplicate
IDs, aliases in place of canonical IDs, and ambiguous status wording MUST fail
review.

#### Scenario: Two stubs claim the same parked ID

- **WHEN** the stub set is reviewed
- **THEN** the duplicate is rejected
- **AND** neither entry is treated as a distinct parked ID

### Requirement: The inclusion boundary is preserved

Every stub in this change MUST remain `INCLUDED Ultra ONLY` and `NEVER` for
On-Demand dispatch. A later change is required to alter either boundary.

#### Scenario: A proposal adds a broader exposure label

- **WHEN** a stub includes a broader or inferred exposure route
- **THEN** the review fails
- **AND** the stub remains parked until the proposal is corrected

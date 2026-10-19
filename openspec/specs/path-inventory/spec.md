# Path Inventory

## ADDED Requirements

### Requirement: Canonical specs path

The repository SHALL use `openspec/specs/` as the canonical root for applied
capability specifications.

#### Scenario: Resolve an applied specification

- **WHEN** a consumer looks up a capability specification
- **THEN** the lookup starts below `openspec/specs/`
- **AND** the capability is represented by a directory containing `spec.md`

### Requirement: Change package path

The repository SHALL keep the proposal and delta for this change below
`openspec/changes/third-salvo-19-specs-path-inventory/`.

#### Scenario: Resolve the T3-19 change package

- **WHEN** a consumer resolves change-id
  `third-salvo-19-specs-path-inventory`
- **THEN** `proposal.md` is present at the change root
- **AND** the path-inventory delta is present at
  `specs/path-inventory/spec.md`

### Requirement: Inventory records the package paths

The applied path-inventory specification SHALL list the canonical paths for
the T3-19 package and its receipt.

#### Scenario: Inspect the inventory

- **WHEN** the inventory is read
- **THEN** it identifies the applied specification at
  `openspec/specs/path-inventory/spec.md`
- **AND** it identifies the proposal at
  `openspec/changes/third-salvo-19-specs-path-inventory/proposal.md`
- **AND** it identifies the change delta at
  `openspec/changes/third-salvo-19-specs-path-inventory/specs/path-inventory/spec.md`
- **AND** it identifies the receipt at
  `openspec/changes/third-salvo-19-specs-path-inventory/RECEIPT.md`

### Requirement: Included Ultra classification

The T3-19 package SHALL be classified as INCLUDED Ultra only and SHALL never
define an On-Demand lane.

#### Scenario: Validate package classification

- **WHEN** package metadata is evaluated
- **THEN** the classification is `INCLUDED`
- **AND** the tier is `Ultra`
- **AND** no On-Demand behavior is specified

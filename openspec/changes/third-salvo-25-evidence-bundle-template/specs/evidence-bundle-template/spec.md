# Evidence Bundle Template

## ADDED Requirements

### Requirement: The bundle has immutable T3-25 identity

The template MUST identify `THIRD_SALVO` slot `T3-25` and the
`third-salvo-25-evidence-bundle-template` change. It MUST declare
`inclusion: INCLUDED`, `tier: Ultra`, `on_demand: false`, and
`network: disabled`.

#### Scenario: A completed bundle has the required identity

- **WHEN** a reviewer opens a completed T3-25 bundle
- **THEN** all six identity values are present and unchanged
- **AND** the status and review fields are distinguishable from the identity

#### Scenario: A bundle uses a different delivery mode

- **WHEN** `on_demand` is true or an On-Demand label appears as the delivery
  mode
- **THEN** the bundle MUST be rejected
- **AND** it MUST NOT be relabeled as included after review

### Requirement: Evidence records are locally reproducible

Each evidence record MUST contain an identifier, repository-relative path,
byte count, SHA-256 digest, UTC timestamp, local inspection command, result,
and reviewer. Paths MUST NOT be absolute, and commands MUST NOT require a
network connection.

#### Scenario: A reviewer verifies one evidence record

- **WHEN** the recorded local command is run from the repository root
- **THEN** the result can be compared with the recorded byte count and digest
- **AND** the reviewer can identify the artifact without opening unrelated data

#### Scenario: A record is missing integrity data

- **WHEN** a record has no byte count or SHA-256 digest
- **THEN** the bundle MUST remain incomplete
- **AND** the reviewer MUST NOT mark the bundle ready

### Requirement: The template protects scope boundaries

The template MUST support local-only review and MUST NOT request credentials,
network access, service calls, or unrelated slot data.

#### Scenario: Review is performed offline

- **WHEN** the reviewer follows the template's validation steps without a
  network connection
- **THEN** the identity, evidence records, and review checklist remain usable
- **AND** no remote dependency is needed to complete the receipt

### Requirement: The receipt is traceable

The delivered receipt MUST name the change ID, slot, inclusion tier, delivered
template path, validation result, and final revision.

#### Scenario: A receipt is checked against the change

- **WHEN** a reviewer compares the receipt with the OpenSpec change
- **THEN** the change ID and T3-25 identity match exactly
- **AND** the receipt identifies the template used for the bundle

# Specification: dud/no-PR fish ledger

## Requirements

### Requirement: Keep T3-05 in the included Ultra lane

The ledger MUST identify every row as `THIRD_SALVO` slot `T3-05`, with
`lane=Ultra` and `state=included`. `On-Demand` MUST NOT appear as a row state,
lane, fallback, or promotion path.

#### Scenario: A seeded gap is opened for review

- **WHEN** a reviewer opens any seeded row
- **THEN** the row identifies the `Ultra` lane and `included` state
- **AND** the row has no `On-Demand` alternative

### Requirement: Preserve dud/no-PR status

Each seeded Tube-2 gap MUST begin as a dud record with `pr_status=none` and
`evidence_status=unverified`. A blank or placeholder evidence field MUST NOT
be interpreted as a successful lookup.

#### Scenario: A row has no reviewable evidence

- **WHEN** a row has no canonical evidence pointer or human verification
- **THEN** its status remains `dud`
- **AND** its PR status remains `none`
- **AND** it is not eligible for promotion

### Requirement: Make gap provenance explicit

The ledger MUST distinguish a known gap seed from a candidate claim. Seed rows
MUST name the missing Tube-2 artifact or handoff condition and MUST leave
candidate-specific values for later authorized entry.

#### Scenario: A reviewer needs to resolve a gap

- **WHEN** a reviewer supplies a candidate and reviewable evidence
- **THEN** the reviewer can update the corresponding row without changing the
  slot contract
- **AND** the row retains the original gap identifier and dud disposition
  until the review is complete

### Requirement: Operate offline

The ledger MUST be usable as a documentation fixture without provider calls,
credentials, secrets, or live infrastructure.

#### Scenario: The fixture is validated locally

- **WHEN** the change is reviewed in an offline checkout
- **THEN** all required fields and seeded gap identifiers are visible in the
  fixture
- **AND** no network action is required to understand its current state

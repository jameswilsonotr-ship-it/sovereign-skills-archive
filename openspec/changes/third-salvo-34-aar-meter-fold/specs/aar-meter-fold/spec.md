# AAR meter fold

## ADDED Requirements

### Requirement: T3-34 includes only Ultra

For slot `T3-34`, an AAR meter fold MUST count only records whose explicit
classification is `Ultra` and whose window is post-reset.

#### Scenario: post-reset Ultra record is included

- **GIVEN** a local record belongs to slot `T3-34`
- **AND** the record is in the post-reset window
- **AND** its explicit classification is `Ultra`
- **WHEN** the AAR meter fold is calculated
- **THEN** the record contributes one included unit

#### Scenario: On-Demand record is excluded

- **GIVEN** a local record belongs to slot `T3-34`
- **AND** the record is in the post-reset window
- **AND** its explicit classification is `On-Demand`
- **WHEN** the AAR meter fold is calculated
- **THEN** the record contributes zero included units
- **AND** the record MUST NOT be converted, substituted, or used as an
  `Ultra` fallback

#### Scenario: unclassified record is excluded

- **GIVEN** a local record belongs to slot `T3-34`
- **AND** the record is in the post-reset window
- **AND** its classification is missing or unknown
- **WHEN** the AAR meter fold is calculated
- **THEN** the record contributes zero included units

### Requirement: reset starts a zero baseline

The post-reset T3-34 fold MUST start at zero and MUST NOT include records from
before the reset boundary.

#### Scenario: pre-reset history does not carry forward

- **GIVEN** a T3-34 record was observed before the reset boundary
- **WHEN** the post-reset AAR meter fold is calculated
- **THEN** that record is excluded from the fold
- **AND** the post-reset baseline remains independent of the pre-reset total

### Requirement: execution remains offline

The AAR meter fold MUST be computable from local records without external,
provider, secrets, Vultr, or Linear access.

#### Scenario: offline calculation

- **GIVEN** the local post-reset records are available
- **WHEN** the fold is calculated
- **THEN** no network, provider, secret, Vultr, or Linear dependency is
  required

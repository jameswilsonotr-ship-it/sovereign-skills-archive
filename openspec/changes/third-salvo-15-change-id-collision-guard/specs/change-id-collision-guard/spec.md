# Change-ID Collision Guard

## ADDED Requirements

### Requirement: Reserved IDs are compared canonically

The guard MUST compare a candidate change ID with reserved IDs after ASCII
whitespace trimming and ASCII lower-casing.

#### Scenario: Exact reserved ID

- **GIVEN** `third-salvo-15-change-id-collision-guard` is reserved
- **WHEN** the candidate uses that exact ID
- **THEN** the guard returns `collision`

#### Scenario: Case-only variation

- **GIVEN** `third-salvo-15-change-id-collision-guard` is reserved
- **WHEN** the candidate uses `THIRD-SALVO-15-CHANGE-ID-COLLISION-GUARD`
- **THEN** the guard returns `collision`

#### Scenario: Distinct ID

- **GIVEN** `third-salvo-15-change-id-collision-guard` is reserved
- **WHEN** the candidate uses `third-salvo-15-change-id-collision-guard-followup`
- **THEN** the guard returns `available` for collision checking

### Requirement: T3-15 is Included Ultra only

The guard MUST reject a request for this reserved change when its availability
is `on-demand`, regardless of whether the candidate ID is otherwise unique.

#### Scenario: On-Demand request

- **GIVEN** the candidate ID is unique
- **WHEN** the request declares `availability: on-demand`
- **THEN** the guard returns `invalid-lane`

#### Scenario: Included Ultra request

- **GIVEN** the candidate ID is unique
- **WHEN** the request declares `availability: included` and `inclusion: ultra`
- **THEN** the guard returns `available`

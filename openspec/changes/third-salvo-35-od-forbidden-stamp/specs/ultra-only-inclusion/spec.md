# T3-35 Ultra-only inclusion

## ADDED Requirements

### Requirement: T3-35 is included for Ultra only
The desk MUST classify slot `T3-35` as `INCLUDED` for `Ultra` only. The desk
MUST NOT classify, route, or expose slot `T3-35` as On-Demand.

#### Scenario: Ultra request is classified
- **WHEN** a request is explicitly classified as `Ultra` and targets `T3-35`
- **THEN** the desk records it as `INCLUDED`
- **AND** the desk does not add an On-Demand classification

#### Scenario: On-Demand request targets T3-35
- **WHEN** a request targets `T3-35` with an On-Demand classification
- **THEN** the desk rejects that classification
- **AND** the desk does not silently convert or queue it as `INCLUDED`

#### Scenario: Classification is missing or ambiguous
- **WHEN** a request targets `T3-35` without an unambiguous `Ultra`
  classification
- **THEN** the desk holds the request for clarification
- **AND** the desk does not use On-Demand as a fallback

### Requirement: The boundary is desk-visible
The desk MUST keep the OD-forbidden stamp associated with this change ID and
MUST preserve the exact `T3-35` and `Ultra` identifiers when copying it.

#### Scenario: Stamp is consulted
- **WHEN** an operator checks the T3-35 inclusion rule
- **THEN** the stamp states `INCLUDED: ULTRA ONLY`
- **AND** the stamp states `ON-DEMAND: FORBIDDEN`
- **AND** the stamp identifies change ID
  `third-salvo-35-od-forbidden-stamp`

# Spec: Offline fixture checksum coverage

## ADDED Requirements

### Requirement: T3-21 is included in Ultra only

The offline fixture MUST represent T3-21 as included in the Ultra surface and
MUST NOT represent it as On-Demand.

#### Scenario: Verify the T3-21 policy boundary

- **WHEN** the offline verifier loads the T3-21 fixture
- **THEN** `salvo` is `THIRD_SALVO`
- **AND** `slot` is `T3-21`
- **AND** `availability` is `included`
- **AND** `tier` is `Ultra`
- **AND** `on_demand` is `false`

### Requirement: Fixture bytes are checksum protected

The T3-21 fixture MUST have exactly one active SHA-256 record in the offline
checksum manifest, and the record MUST match the fixture bytes.

#### Scenario: Verify an unchanged fixture

- **WHEN** the offline verifier reads the fixture and checksum manifest
- **THEN** it computes the same SHA-256 digest as the recorded checksum
- **AND** it exits successfully without network access

#### Scenario: Detect fixture drift

- **WHEN** the fixture bytes differ from the recorded checksum
- **THEN** the verifier MUST fail with a checksum mismatch

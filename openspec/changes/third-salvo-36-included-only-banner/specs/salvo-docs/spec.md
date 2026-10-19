# Salvo documentation specification

## Requirement: T3-36 is INCLUDED Ultra only

Salvo documentation MUST classify `THIRD_SALVO` slot `T3-36` as INCLUDED in
Ultra only. It MUST state that the slot is never On-Demand.

### Scenario: A reader opens the canonical salvo documentation

- **GIVEN** a reader opens `docs/salvo/README.md`
- **WHEN** the page loads
- **THEN** the first documentation block is an INCLUDED/Ultra-only banner
- **AND** the banner explicitly says `T3-36` is never On-Demand

### Scenario: A salvo document describes T3-36

- **GIVEN** a salvo document mentions `THIRD_SALVO` slot `T3-36`
- **WHEN** the document states the slot's entitlement
- **THEN** it preserves the INCLUDED Ultra-only classification
- **AND** it does not describe the slot as an On-Demand option

## Requirement: The change remains documentation-only

This change MUST NOT add runtime behavior or entitlement logic. It MUST remain
independent of account, deployment, and credential configuration.

# continuous-included-reload

## Purpose

Define the T4-08 reload contract: continuous execution on included capacity
only, with no On-Demand or external fallback.

## Requirements

### Requirement: Continuous included reload

T4-08 SHALL keep reload work continuous across eligible iterations and SHALL
use included capacity only.

#### Scenario: Included capacity remains available

- **WHEN** the current reload iteration completes and included capacity is
  available
- **THEN** the lane MUST remain eligible for the next reload iteration without
  switching execution mode

#### Scenario: Included capacity is unavailable

- **WHEN** an iteration cannot continue with included capacity
- **THEN** the lane MUST stop with a blocked result and MUST NOT select
  On-Demand capacity

### Requirement: Offline and fenced execution

T4-08 SHALL be verifiable from local fixtures without provider access, secret
material, live infrastructure, or `CONV2_B`.

#### Scenario: Offline verification

- **WHEN** the offline harness exercises the reload contract
- **THEN** it MUST use local fixtures and MUST make no network calls

### Requirement: Unique OpenSpec change-id

The OpenSpec matrix generator SHALL reject more than one source claiming the
same change-id, including case-only differences.

#### Scenario: Collision detected

- **WHEN** two OpenSpec sources claim the same normalized change-id
- **THEN** matrix generation MUST fail before writing generated output and MUST
  identify the colliding sources

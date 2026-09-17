# phone-8081-keeper

## Purpose

Documentation-only contract for the T4-04 CinC target `phone:8081/keeper`.
The contract describes a continuous included reload lane and does not create a
live phone endpoint.

## Requirements

### Requirement: CinC target path

The T4-04 note SHALL identify the CinC target as phone port `8081` with path
`/keeper`, written as `phone:8081/keeper`. The notation MUST remain
transport-neutral.

#### Scenario: Target recorded

- **WHEN** a reviewer reads the T4-04 target note
- **THEN** the note MUST identify `phone:8081/keeper` and MUST NOT claim that
  a listener or endpoint is live

### Requirement: Continuous included reload

The T4-04 reload policy SHALL be continuous and SHALL use the included lane
only. On-Demand execution, fallback, or spend MUST NOT be part of the policy.

#### Scenario: Reload cycle remains included

- **WHEN** a reload cycle is documented or scheduled under T4-04
- **THEN** it MUST remain continuous and included-only, with no On-Demand
  route

#### Scenario: No On-Demand fallback

- **WHEN** the included lane is unavailable or a reload is delayed
- **THEN** the note MUST preserve the included-only boundary and MUST NOT
  authorize an On-Demand fallback

### Requirement: Offline documentation boundary

This change SHALL contain documentation only. It MUST NOT bind or probe
`phone:8081/keeper`, open a socket, issue a request, or contact an external
service.

#### Scenario: Apply or review is offline

- **WHEN** this OpenSpec package is applied or reviewed
- **THEN** no live bind, network request, provider call, credential lookup, or
  runtime change SHALL occur

### Requirement: Fenced scope

This change MUST NOT edit Willow `SKILL.md` files or live lock files, unpack or
process `CONV2_B`, include credentials or secrets, provision infrastructure,
or add external/provider integration.

#### Scenario: Fence audit

- **WHEN** the change is checked before review
- **THEN** all changed paths MUST be under `docs/openspec/salvo/` and no
  fenced artifact or integration SHALL be present

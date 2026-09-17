# continuous-included-reload

## Purpose

Offline contract for T4-31 continuous reload of the preserved MIS-6 land
delta. The contract has no live I/O and permits included capacity only.

## Requirements

### Requirement: Included-only reload

Every reload cycle SHALL use included capacity or stop as `blocked`.
On-Demand MUST NOT be selected, increased, recommended, or used as fallback.

#### Scenario: Included cycle completes

- **WHEN** the unchanged MIS-6 fixture is available and included capacity is
  available
- **THEN** the cycle MUST complete with status `included`

#### Scenario: Included capacity is unavailable

- **WHEN** a reload cycle cannot use included capacity
- **THEN** it MUST stop with status `blocked` and MUST NOT use On-Demand

### Requirement: Continuous local reload

Each subsequent cycle SHALL reconcile from the prior local receipt and the
unchanged MIS-6 fixture. A cycle MUST NOT fetch remote state or mutate the
fixture.

#### Scenario: Successive cycles

- **WHEN** two or more reload cycles run in sequence
- **THEN** cycle numbers MUST increase monotonically and each cycle MUST
  reference the same local MIS-6 baseline

#### Scenario: Baseline drift

- **WHEN** the MIS-6 fixture is missing or its recorded content changes
- **THEN** the cycle MUST be `blocked` and MUST NOT substitute another source

### Requirement: Offline and fenced execution

The reload contract MUST execute without network, provider, secret, billing,
hosted-provisioning, or browser access. It MUST NOT touch `SKILL.md` files or
consume `CONV2_B` material.

#### Scenario: Offline-only execution

- **WHEN** T4-31 is applied or verified
- **THEN** only repository-local fixtures, checks, and receipts MAY be used

### Requirement: One receipt per cycle

Every attempted cycle SHALL produce exactly one secret-free receipt containing
the cycle number, status, local baseline identifier, and verification results.

#### Scenario: Receipt emitted

- **WHEN** a cycle reaches `included` or `blocked`
- **THEN** exactly one receipt MUST be written and it MUST contain no
  credentials, provider data, or copied payload

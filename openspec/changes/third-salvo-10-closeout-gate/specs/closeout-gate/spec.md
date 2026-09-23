# Specification: THIRD_SALVO T3-10 closeout gate

## Requirements

### Requirement: accept only the included Ultra lane

The closeout gate MUST accept only slot `T3-10` when its lane is
`INCLUDED Ultra`.

#### Scenario: included Ultra qualifies

- **WHEN** the slot is `T3-10` and the lane is `INCLUDED Ultra`
- **THEN** the lane gate MAY pass

#### Scenario: On-Demand does not qualify

- **WHEN** the lane is `On-Demand`
- **THEN** the lane gate MUST fail
- **AND** the closeout MUST NOT be marked `CLOSED`

### Requirement: keep meters separate from spawning

The closeout gate MUST treat meters as observations only. A meter MUST NOT
authorize, trigger, infer, or report a spawn.

#### Scenario: meter is observed

- **WHEN** a meter value is recorded
- **THEN** it MAY be included as offline evidence
- **AND** it MUST NOT cause a spawn, retry, queue release, escalation,
  schedule, or capacity allocation

#### Scenario: meter crosses a threshold

- **WHEN** a meter crosses any threshold
- **THEN** the closeout gate MUST remain independent of that threshold
- **AND** no execution action may follow from the crossing

### Requirement: enforce offline hard fences

The change MUST be completable using repository-local documentation and
static inspection only.

#### Scenario: hard-fence inspection

- **WHEN** the closeout package is inspected
- **THEN** it MUST contain no Willow `SKILL.md` edit, `CONV2_B` work,
  external/provider call, secret, Vultr live operation, or Linear mint

### Requirement: issue a non-authorizing receipt

When all gates pass, the package MUST include a receipt stating that the
state is `CLOSED` and that closeout does not authorize spawning or live
operations.

#### Scenario: all gates pass

- **WHEN** identity, lane, meter-separation, hard-fence, and offline-evidence
  checks pass
- **THEN** the receipt MUST record `CLOSED`
- **AND** the receipt MUST state `meters ≠ spawn`
- **AND** the receipt MUST state that no execution authority is granted

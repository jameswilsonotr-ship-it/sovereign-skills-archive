# tube3-spent-by-rule

## Purpose

Define deterministic accounting for Third Salvo slot T3-37. Tube-3 is
**included Ultra only**; On-Demand is never an eligible execution class.

## Requirements

### Requirement: Included Ultra only

Every T3-37 dispatch SHALL declare the execution class
`included-ultra`. A dispatch with an absent, ambiguous, On-Demand, provider, or
other execution class MUST be rejected and MUST remain `not-spent`.

#### Scenario: Eligible dispatch

- **WHEN** T3-37 is dispatched with execution class `included-ultra`
- **THEN** the dispatch MAY proceed against the local atomic change

#### Scenario: On-Demand dispatch

- **WHEN** T3-37 is dispatched through On-Demand or an On-Demand fallback
- **THEN** the dispatch MUST be rejected, MUST not continue, and MUST remain
  `not-spent`

#### Scenario: Ambiguous class

- **WHEN** the execution class is missing or cannot be verified locally
- **THEN** the dispatch MUST be rejected and MUST remain `not-spent`

### Requirement: Atomic T3-37 scope

The T3-37 unit SHALL map to exactly
`third-salvo-37-tube3-spent-rule` and one reviewable PR. Work from another
change-id MUST NOT satisfy this unit.

#### Scenario: Exact change-id

- **WHEN** a local record is created for T3-37
- **THEN** it MUST contain the exact change-id and slot `T3-37`

#### Scenario: Sibling work

- **WHEN** a dispatch includes a sibling change-id or unrelated scope
- **THEN** that dispatch MUST NOT qualify as the T3-37 atomic unit

### Requirement: Spent-by-rule transition

Tube-3 SHALL transition from `not-spent` to `spent` only after all of the
following are true:

1. execution class is `included-ultra`;
2. the exact change-id is complete;
3. the OpenSpec artifact is present; and
4. the post-land receipt is present.

No external meter, provider response, or secret is required or permitted for
this documentation-only accounting transition.

#### Scenario: Complete eligible unit

- **WHEN** the exact T3-37 artifact and receipt are complete and the execution
  class is `included-ultra`
- **THEN** Tube-3 MAY be recorded as `spent`

#### Scenario: Incomplete unit

- **WHEN** any required artifact, exact change-id, receipt, or execution-class
  field is missing
- **THEN** Tube-3 MUST remain `not-spent`

### Requirement: Offline and fenced operation

The T3-37 workflow MUST operate offline and MUST NOT touch Willow `SKILL.md`,
`CONV2_B`, external/provider services, secrets, Vultr, or Linear.

#### Scenario: Fenced path requested

- **WHEN** a proposed step requires a forbidden path
- **THEN** the step MUST be refused and the unit MUST remain `not-spent`

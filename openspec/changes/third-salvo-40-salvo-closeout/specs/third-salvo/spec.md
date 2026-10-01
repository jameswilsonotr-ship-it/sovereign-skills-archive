# Third salvo slot inclusion

## Requirements

### Requirement: T3-40 is Ultra-only

The system documentation MUST identify slot T3-40 as part of `THIRD_SALVO`
and MUST assign `Ultra` as its only included class.

#### Scenario: T3-40 is included

- **WHEN** the third-salvo inclusion set is evaluated
- **THEN** slot T3-40 is present
- **AND** its inclusion class is `Ultra`

### Requirement: T3-40 cannot use On-Demand

The system documentation MUST NOT include T3-40 in `On-Demand`, and MUST NOT
use `On-Demand` as a fallback or alternate interpretation for this slot.

#### Scenario: an alternate class is proposed

- **WHEN** T3-40 is evaluated with `On-Demand`
- **THEN** the evaluation is rejected
- **AND** the slot remains `Ultra`-only

### Requirement: closeout is locally auditable

The closeout MUST be representable using repository text files and MUST
include the change ID, slot, salvo, inclusion class, prohibited class, status,
and local validation evidence.

#### Scenario: a reviewer checks the receipt

- **WHEN** a reviewer opens the T3-40 closeout receipt
- **THEN** it identifies `third-salvo-40-salvo-closeout`
- **AND** it points to the OpenSpec proposal, specification, and task list
- **AND** it records a closed status with local-only evidence

# INCLUDED burn percentage receipt

## Requirements

### Requirement: record the T3-32 INCLUDED Ultra receipt

The system MUST represent the THIRD_SALVO T3-32 burn percentage with a
receipt containing:

- `change_id`, equal to `third-salvo-32-burn-pct-receipt`
- `salvo`, equal to `THIRD_SALVO`
- `slot`, equal to `T3-32`
- `lane`, equal to `INCLUDED`
- `tier`, equal to `Ultra`
- `burn_pct`, a percentage value or `null` while the receipt is a stub
- `burn_pct_unit`, equal to `percent`
- `status`, equal to `stub` until a measurement is supplied

The receipt MUST remain data-only and offline.

#### Scenario: initialize the eligible receipt

- **GIVEN** slot `T3-32` belongs to `THIRD_SALVO`
- **AND** the lane is `INCLUDED`
- **AND** the tier is `Ultra`
- **WHEN** the receipt is initialized without a measurement
- **THEN** the receipt is valid with `burn_pct: null`
- **AND** the receipt status is `stub`

### Requirement: exclude the On-Demand lane

The system MUST NOT emit or populate this receipt for the `On-Demand` lane.

#### Scenario: reject an ineligible lane

- **GIVEN** the slot or tier is otherwise similar
- **WHEN** the lane is `On-Demand`
- **THEN** no T3-32 INCLUDED burn percentage receipt is created

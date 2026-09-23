# Fat-cull reject-list delta specification

## Requirement: continuously included reload

T4-07 MUST be reloaded continuously in the `INCLUDED` lane. It MUST be
explicitly marked `On-Demand: NEVER`.

### Scenario: reload is accepted

- **GIVEN** a local T4-07 snapshot is reloaded
- **WHEN** the reload completes
- **THEN** the reject list remains present
- **AND** the mode remains `CONTINUOUS`
- **AND** the lane remains `INCLUDED`
- **AND** no On-Demand request is emitted

### Scenario: On-Demand is requested

- **GIVEN** a caller requests T4-07 through an On-Demand path
- **WHEN** the request is evaluated
- **THEN** it is rejected as outside this change
- **AND** no On-Demand receipt is emitted

## Requirement: reject protected scope

The T4-07 reject list MUST reject Willow `SKILL.md` and skill-tree live-lock
content, `CONV2_B`, unproven runtime/build inputs, and external/provider,
secret, credential, or Vultr-related material from fat-cull consideration.

### Scenario: a candidate matches a reject class

- **GIVEN** a candidate matches one of the protected classes
- **WHEN** the local register is evaluated
- **THEN** the candidate is marked `reject`
- **AND** no delete, move, archive, regenerate, package, or re-tier action is
  authorized

## Requirement: documentation-only delivery

T4-07 MUST remain offline-only documentation. It MUST contain one atomic
change and one receipt, with no runtime or integration behavior.

### Scenario: receipt is reviewed

- **GIVEN** the T4-07 change is checked
- **WHEN** its files are enumerated
- **THEN** the receipt records the continuous/included classification and all
  reject classes
- **AND** no implementation or external integration artifact is present

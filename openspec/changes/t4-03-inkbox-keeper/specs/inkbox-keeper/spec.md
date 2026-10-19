# T4-03: Inkbox keeper

## Requirements

### Requirement: Continuous included reload

The T4-03 keeper MUST provide reload as **CONTINUOUS INCLUDED** behavior.
Reload MUST be part of the keeper contract without an opt-in mode, and the
contract MUST NOT provide, select, fall back to, or describe OD/On-Demand
reload.

#### Scenario: Keeper is loaded

- **WHEN** the T4-03 keeper contract is loaded
- **THEN** continuous included reload is present in the contract
- **AND** no OD/On-Demand reload path is available

### Requirement: Atomic CinC target

The T4-03 contract MUST identify `Inkbox` as one atomic CinC target. The
contract MUST NOT split the target into provider-specific or externally
executed sub-targets.

#### Scenario: Target is reviewed

- **WHEN** the OpenSpec change is reviewed
- **THEN** the target is named `Inkbox`
- **AND** the target boundary is one atomic documentation contract

### Requirement: Inkbox no-op

The T4-03 change MUST affirm Inkbox as a NO-OP. It MUST NOT add executable
Inkbox behavior, an API call, a connector, a webhook, a credential, or an
external side effect.

#### Scenario: Documentation is applied

- **WHEN** the change is applied
- **THEN** only OpenSpec and receipt documentation changes
- **AND** Inkbox runtime behavior remains untouched

### Requirement: Offline fenced scope

The change MUST remain offline and documentation-only. It MUST NOT add or
modify `Willow SKILL.md`, `CONV2_B`, external/provider integrations, secrets,
or Vultr configuration.

#### Scenario: Scope is validated

- **WHEN** the diff is inspected
- **THEN** changed paths are OpenSpec Markdown or the T4-03 receipt
- **AND** no forbidden integration or deployment artifact is present

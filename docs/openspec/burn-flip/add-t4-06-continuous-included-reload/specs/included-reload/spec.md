# included-reload

## Purpose

Offline contract for T4-06 continuous reload of a thin Keeper map delta after
T3. The contract consumes included local state only and never opens an
On-Demand path.

## Requirements

### Requirement: Continuous included reload

The reload loop SHALL read only the local post-T3 delta input and SHALL run
in `CONTINUOUS_INCLUDED` mode. It MUST NOT request, recommend, or fall back
to On-Demand capacity or spend.

#### Scenario: Included delta is available

- **WHEN** a local post-T3 delta is available and its `delta_id` is new
- **THEN** the cycle MUST record one thin map overlay with
  `CONTINUOUS_INCLUDED` mode and MUST not perform a live or provider action

#### Scenario: No included delta is available

- **WHEN** a cycle has no local post-T3 delta
- **THEN** it MUST report `NO_TWIN` and MUST stop the cycle without opening an
  On-Demand fallback

### Requirement: Thin Keeper map overlay

The Keeper delta SHALL contain bounded metadata and pointers only:
`delta_id`, `source_ref`, `map_key`, `status`, `disposition`, and
`recorded_at`. It MUST NOT copy the KEEP body or rewrite historical records.

#### Scenario: New map target

- **WHEN** a new delta resolves to a local `map_key`
- **THEN** the cycle MUST append one overlay record and leave prior records
  unchanged

#### Scenario: Existing delta

- **WHEN** a delta with the same `delta_id` is encountered again
- **THEN** the cycle MUST return `SKIP_EXISTING` and MUST not append a second
  record

### Requirement: Honest unresolved inputs

The cycle SHALL preserve unresolved states instead of inventing post-T3
content.

#### Scenario: Missing map target

- **WHEN** the local delta exists but its `map_key` cannot be resolved
- **THEN** the cycle MUST record `NO_SHARD` or `UNKNOWN` and MUST not search
  outside the local input set

#### Scenario: Historical KEEP remains separate

- **WHEN** a cycle needs context from the historical KEEP surface
- **THEN** it MUST retain a pointer to that surface and MUST NOT slurp, copy,
  or rebuild it as part of the reload

### Requirement: Offline safety fences

Applying or reviewing this contract MUST be offline-only. It MUST NOT touch
`SKILL.md` or Willow live-lock files, unpack `CONV2_B`, contact external or
provider services, read or create secrets, perform Vultr work, or mutate
On-Demand state.

#### Scenario: Offline review

- **WHEN** the change is verified
- **THEN** verification MUST use repository-local files and diff checks only
- **AND** no network, provider, secret, cloud, or billing action SHALL occur

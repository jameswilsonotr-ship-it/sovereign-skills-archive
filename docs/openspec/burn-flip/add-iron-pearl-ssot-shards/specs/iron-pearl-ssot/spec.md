# iron-pearl-ssot

## Purpose

Awesome Split / HANDOFF SSoT with exactly eight owned shards and delta CAS per
Iron Pearl BASIC SPEC-001. Google Docs is not an allowed medium.

## Requirements

### Requirement: Awesome Split / HANDOFF SSoT

The system SHALL maintain an Awesome Split / HANDOFF single source of truth
under Iron Pearl BASIC SPEC-001 only. Awesome Split state SHALL be rooted at
`docs/iron-pearl/ssot/awesome-split/`, and HANDOFF state SHALL be rooted at
`docs/iron-pearl/ssot/handoff/`.

#### Scenario: SSoT path declared

- **WHEN** handoff state is written
- **THEN** it MUST land under one of the declared Iron Pearl BASIC SSoT roots
  and MUST NOT use Google Docs

### Requirement: Eight-slot shards

SSoT state SHALL be partitioned into exactly eight slots with clear ownership
boundaries. Every write SHALL name exactly one target slot and use the
ownership label assigned to that slot in the design.

#### Scenario: Shard count

- **WHEN** the shard layout is initialized
- **THEN** exactly eight slots MUST exist and each write MUST name its target
  slot

#### Scenario: Ownership boundary

- **WHEN** a writer submits a shard delta
- **THEN** the target slot and its ownership label MUST be present and
  unambiguous

### Requirement: Delta CAS

Updates SHALL use compare-and-swap (CAS) on deltas so concurrent writers cannot
clobber state without detection. Each delta SHALL include `base_version` and
`next_version`; an accepted write SHALL advance the head by one version.

#### Scenario: Current-head write accepted

- **WHEN** a writer submits a delta whose `base_version` equals the current
  SSoT head and whose `next_version` is `base_version + 1`
- **THEN** the delta MUST be appended and the head MUST advance to
  `next_version` atomically

#### Scenario: Stale write rejected

- **WHEN** a writer submits a delta with a stale `base_version`
- **THEN** CAS MUST fail without a partial write, the writer MUST reread the
  current SSoT head, and the writer MUST retry from that head

### Requirement: No Google Docs

Google Docs MUST NOT be used as the SSoT, handoff medium, or shard store.

#### Scenario: Docs rejected

- **WHEN** a procedure proposes Google Docs for SSoT, handoff, or shard state
- **THEN** the change MUST refuse that path and direct the writer to the
  declared repository SSoT roots

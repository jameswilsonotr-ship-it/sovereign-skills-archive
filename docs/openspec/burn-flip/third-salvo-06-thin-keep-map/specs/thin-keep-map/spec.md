# thin-keep-map

## Purpose

Provide a post-coherence KEEP map for Third Salvo slot `T3-06` under the
reserved change-id `third-salvo-06-thin-keep-map`. The packet is
documentation-only and runs on INCLUDED Ultra only.

## Requirements

### Requirement: Atomic slot identity

The packet SHALL identify exactly one change-id:
`third-salvo-06-thin-keep-map`.

#### Scenario: Slot is reviewed

- **WHEN** the T3-06 packet is opened for review
- **THEN** its OpenSpec documents and KEEP map MUST name the reserved
  change-id and MUST NOT include a sibling slot or sibling change-id

### Requirement: Thin post-coherence map

The packet SHALL provide a compact map of retained surfaces and handling
boundaries after coherence review. The map MUST be reference-only and MUST NOT
duplicate or mutate the material it names.

#### Scenario: Coherence is complete

- **WHEN** the post-coherence review has no unresolved contradiction
- **THEN** the map MUST identify the retained T3-06 documentation surface and
  its hard-fenced exclusions without adding implementation work

#### Scenario: Coherence is not complete

- **WHEN** a contradiction or missing authority is discovered
- **THEN** the lane MUST stop and record the issue for review rather than
  widening this change or making an external call

### Requirement: Included Ultra only

T3-06 SHALL use INCLUDED Ultra only. It MUST NEVER use, recommend, or fall
back to On-Demand.

#### Scenario: Lane is available

- **WHEN** T3-06 is assigned for execution
- **THEN** the assignment MUST be treated as INCLUDED Ultra work and MUST NOT
  authorize On-Demand usage

#### Scenario: Included lane is unavailable

- **WHEN** INCLUDED Ultra is unavailable or exhausted
- **THEN** T3-06 MUST stop; it MUST NOT switch to On-Demand

### Requirement: Protected surfaces remain KEEP

The packet MUST NOT alter Willow `SKILL.md` or skill-tree live locks, unpack or
inspect `CONV2_B`, make external/provider calls, handle secrets, operate Vultr
live, or mint Linear state.

#### Scenario: Fenced action is proposed

- **WHEN** a proposed step would touch a protected surface
- **THEN** the step MUST be rejected as outside T3-06 and no side effect MAY
  occur

### Requirement: Documentation-only deliverable

The packet SHALL contain documentation only and SHALL NOT add runtime code,
dependencies, generated assets, or binary payloads.

#### Scenario: Atomic PR is prepared

- **WHEN** the T3-06 PR is assembled
- **THEN** its diff MUST be limited to this OpenSpec change and its thin-KEEP
  map

# Report-reader digest

## Requirements

### Requirement: Identify the reader and execution fence

The digest MUST identify itself as T4-READER, Included Ultra, ORCH LADDER,
offline, and not on-demand.

#### Scenario: Valid fixed metadata

- **GIVEN** a digest has `reader: T4-READER`, `tier: INCLUDED Ultra`,
  `orchestration: ORCH LADDER`, `delivery: offline`, and `on_demand: false`
- **WHEN** the digest is validated
- **THEN** validation succeeds

#### Scenario: On-demand metadata is rejected

- **GIVEN** a digest has `on_demand: true` or a tier other than `INCLUDED Ultra`
- **WHEN** the digest is validated
- **THEN** validation fails and no desk page is rendered

### Requirement: Preserve landing evidence

Each CA or PR entry MUST include a stable local `source_ref`, a certainty
label, and a concise summary. The renderer MUST carry those labels into the
desk page.

#### Scenario: Confirmed landing

- **GIVEN** a PR entry is marked `certainty: confirmed` and has a source
  reference
- **WHEN** it is rendered
- **THEN** the page presents it as confirmed and cites the same reference

#### Scenario: Missing evidence

- **GIVEN** an entry has no usable source reference
- **WHEN** it is rendered
- **THEN** the entry is labeled `unverified` and gets a follow-up item

### Requirement: Render three desk views

The page MUST include Mag, Liaison, and fleet sections. Each section MUST
contain only source-backed statements or explicitly labeled unknowns.

#### Scenario: Mixed CA and PR digest

- **GIVEN** a digest contains at least one CA entry and one PR entry
- **WHEN** the page is rendered
- **THEN** all entries appear in the landing table and the three desk sections
  summarize their relevant message, handoff, and operational checkpoint

#### Scenario: No landed items

- **GIVEN** a valid digest has an empty `entries` list
- **WHEN** the page is rendered
- **THEN** all three sections state `no landed items` and no action is invented

### Requirement: Stay offline

The contract MUST operate on supplied text only. It MUST NOT require a
network, service call, credential, or live message/mail read to validate or
render a page.

#### Scenario: Local sample rendering

- **GIVEN** the included sample and the documented template
- **WHEN** a reviewer follows the transformation offline
- **THEN** a complete one-pager can be produced from the sample alone

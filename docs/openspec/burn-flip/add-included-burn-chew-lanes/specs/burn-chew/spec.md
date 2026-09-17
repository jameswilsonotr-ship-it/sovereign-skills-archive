# burn-chew

## Purpose

Deterministic OpenSpec chew lanes so Hi Cursor agents burn **included** Cursor
Models toward approximately 80% before reset, via packetized atomic PRs only.

## Requirements

### Requirement: Included-only burn

Burn-chew lanes SHALL consume Cursor Models **included** quota only and MUST
NOT increase On-Demand spend.

#### Scenario: Chew task assigned

- **WHEN** Hi spawns a Cursor agent on a burn-chew change-id
- **THEN** the agent MUST apply that single OpenSpec change via
  `/openspec-apply` without sibling change-id code coupling

### Requirement: Packetized atomic PRs

Each chew lane SHALL produce one atomic PR (or equivalent reviewable unit)
scoped to one change-id.

#### Scenario: One change-id per agent

- **WHEN** an agent completes a chew lane
- **THEN** the deliverable MUST map to exactly one OpenSpec change-id and MUST
  be independently reviewable

### Requirement: Hard non-goals enforced

Burn-chew MUST NOT increase On-Demand spend, vibe-code, touch Willow
`SKILL.md` or skill-tree locks, use Google Docs, or mint plating/avatars.

#### Scenario: SKILL.md untouched

- **WHEN** a burn-chew task executes
- **THEN** no `SKILL.md` or skill-tree live lock file SHALL be created, edited,
  or overwritten

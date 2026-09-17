# Packetized PR discipline

**Atom:** `atom-bc-03-packet-pr`
**Parent change-id:** `add-included-burn-chew-lanes`

## Purpose

Keep each change atom independently reviewable and make the Meter Burn Desk
handoff explicit when its chew is complete.

## Requirements

### Requirement: One atom maps to one reviewable unit

Every pull request (or equivalent reviewable unit) MUST identify exactly one
atom and exactly one parent change-id. For this atom, the PR description MUST
name `atom-bc-03-packet-pr` and `add-included-burn-chew-lanes`.

The unit MUST be independently reviewable, mergeable, and revertible. A PR
MUST NOT combine this atom with sibling atoms from the parent change-id.

#### Scenario: The packet is atomic

- **WHEN** a reviewer checks the PR scope
- **THEN** the description names one atom and one parent change-id
- **AND** all changed files support that atom
- **AND** the unit can be reviewed without opening a sibling atom's PR

#### Scenario: Sibling work is present

- **WHEN** the diff contains work owned by another atom
- **THEN** the reviewer rejects the packet as sibling-coupled
- **AND** the author splits the work into the sibling atom's own PR before
  review continues

### Requirement: Reviewers use the packet checklist

The packet-PR checklist MUST be completed before approval. A reviewer MUST
reject or return the PR for revision when any atomicity check is unchecked,
not applicable without an explanation, or contradicted by the diff.

#### Scenario: Checklist is incomplete

- **WHEN** a required checklist item is unchecked or unsupported
- **THEN** the PR is not approved
- **AND** the author supplies evidence or removes the coupled scope

### Requirement: Completed chew is tagged for Meter Burn Desk

When the packet's chew is complete, the author or reviewer MUST apply the
repository's canonical Meter Burn Desk tag to the PR. The handoff MUST be
recorded in the PR description or review note with the atom and parent
change-id. Do not claim the handoff is complete until the tag is visible.

#### Scenario: Chew completes

- **WHEN** the packet passes the checklist and its chew is complete
- **THEN** the PR receives the canonical Meter Burn Desk tag
- **AND** the handoff note names `atom-bc-03-packet-pr`
- **AND** the handoff note names `add-included-burn-chew-lanes`

#### Scenario: Chew is not complete

- **WHEN** the packet still has unresolved review work
- **THEN** the Meter Burn Desk completion tag is not applied
- **AND** the PR remains in the review state until the checklist passes

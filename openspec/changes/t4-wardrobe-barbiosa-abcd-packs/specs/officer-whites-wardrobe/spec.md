# Specification: officer-whites wardrobe copy

## Requirements

### Requirement: provide four ferry-ready packs

The change MUST provide exactly four primary copy packs, labeled A, B, C, and
D, for the CinC Barbiosa officer-whites wardrobe lane.

#### Scenario: Olivia receives the handoff

- **WHEN** Olivia opens the change
- **THEN** she can identify one cover/hero pack, one wardrobe-beat pack, one
  detail pack, and one closing/handoff pack
- **AND** each pack is usable without consulting a live service

### Requirement: enforce the Ultra lane

Each pack MUST visibly state `INCLUDED ULTRA ONLY`.

#### Scenario: a pack travels alone

- **WHEN** any one pack is copied out of the repository
- **THEN** its lane remains identifiable as CinC Barbiosa officer whites
- **AND** its inclusion status remains `INCLUDED ULTRA ONLY`

### Requirement: exclude the forbidden lane

The packs MUST NOT offer, imply, or route to the forbidden On-Demand lane.

#### Scenario: copy review checks routing

- **WHEN** a reviewer searches the four pack files for the forbidden lane
- **THEN** there are no matches
- **AND** there is no fallback, exception, upsell, or alternate fulfillment path

### Requirement: remain copy-only

The change MUST contain documentation and copy packs only. It MUST NOT add
provider calls, credentials, secrets, external links for delivery, or changes
to Willow `SKILL.md` or `CONV2_B`.

#### Scenario: offline review

- **WHEN** the change is reviewed with external access disabled
- **THEN** all acceptance checks can be completed from repository contents
- **AND** no send, upload, API, Vultr, or Linear action is required

### Requirement: preserve independent pasteability

Each pack MUST include a clear pack label, a lane label, the finished copy,
and an explicit end marker so that it can be pasted into a Drive or email
draft without surrounding repository context.

#### Scenario: copy one pack

- **WHEN** a human copies one pack from its first line through its end marker
- **THEN** the result is coherent standalone text
- **AND** no unresolved placeholder is left for Olivia to interpret

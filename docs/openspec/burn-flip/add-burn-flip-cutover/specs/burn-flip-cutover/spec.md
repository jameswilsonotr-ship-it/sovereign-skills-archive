# burn-flip-cutover

## Purpose

Cutover playbook: when included >= ~80% OR billing reset occurs, flip active coding from Cursor Ultra burn-chew to Vultr headless gateway; freeze new included burn after flip.

## Requirements

### Requirement: Flip triggers

Cutover SHALL arm when meter-watch reports included >= ~80% OR a billing reset is detected.

#### Scenario: Flip on included threshold

- **WHEN** Gage reports Cursor Models included >= ~80%
- **THEN** cutover playbook MUST become actionable and Olette MUST seek Bunny YES before live gateway cut

#### Scenario: Flip on reset

- **WHEN** billing reset is detected
- **THEN** cutover MUST evaluate flip to Vultr gateway and freeze further included-burn chew assignment

### Requirement: Dependencies on slices 1-5

Cutover MUST assume meter-watch, burn-chew, vultr-gateway, iron-pearl-ssot, and phone-mcp-hud contracts exist.

#### Scenario: Preconditions checked

- **WHEN** cutover execute is requested
- **THEN** change-ids 1-5 MUST be recorded as applied (or explicitly waived by Architect) before flip proceeds

### Requirement: Freeze included burn after flip

After successful flip, new Cursor included burn-chew assignments MUST stop.

#### Scenario: Post-flip freeze

- **WHEN** active coding has flipped to Vultr gateway
- **THEN** Hi MUST NOT spawn new included-burn chew agents for Ultra burn purpose

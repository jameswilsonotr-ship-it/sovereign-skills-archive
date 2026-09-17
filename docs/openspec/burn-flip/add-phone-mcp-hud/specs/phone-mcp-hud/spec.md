# phone-mcp-hud

## Purpose

Phone MCP HUD contract at `ws://127.0.0.1:8088/nav/hud` with RSS < 35MB and RAWV. Auth watch coordinates with Keel Sentry separately — this slice is HUD contract only.

## Requirements

### Requirement: HUD endpoint

The phone MCP HUD SHALL expose WebSocket `ws://127.0.0.1:8088/nav/hud`.

#### Scenario: Endpoint bind

- **WHEN** the HUD service starts
- **THEN** it MUST listen on `127.0.0.1:8088` path `/nav/hud` over WebSocket

### Requirement: RSS budget

HUD process RSS MUST stay under 35MB under normal nav load.

#### Scenario: RSS under budget

- **WHEN** HUD is idle or serving routine nav frames
- **THEN** measured RSS MUST be < 35MB

### Requirement: RAWV payload

HUD frames SHALL use RAWV as the declared visual/nav payload mode per Iron Pearl BASIC.

#### Scenario: RAWV declared

- **WHEN** a HUD frame is emitted
- **THEN** the frame contract MUST identify RAWV mode

### Requirement: HUD-only scope

This capability MUST NOT implement MCP auth policy; Keel Sentry coordinates auth watch outside this slice.

#### Scenario: Auth out of scope

- **WHEN** an auth anomaly is observed at the HUD socket
- **THEN** HUD MAY signal/log but MUST NOT own auth remediation (Keel Sentry lane)

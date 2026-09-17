# Proposal: add-phone-mcp-hud

## Why

Iron Pearl BASIC requires a phone MCP HUD at `ws://127.0.0.1:8088/nav/hud` with RSS < 35MB and RAWV. Need a HUD-only contract so apply/chew can stub the endpoint without owning Keel Sentry auth policy.

## What Changes

- Add `phone-mcp-hud` capability: WebSocket endpoint, RSS budget, RAWV frames, auth-out-of-scope fence.
- Coordinate note: MCP auth watch remains Keel Sentry.

## Capabilities

| Capability | Mode |
|------------|------|
| `phone-mcp-hud` | ADDED |

## Impact

- Phone nav HUD contract for local loopback MCP.
- Auth anomalies signaled but not remediated here.

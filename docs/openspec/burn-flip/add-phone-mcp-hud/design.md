# Design: add-phone-mcp-hud

## Context

SPEC-001: phone MCP HUD `ws://127.0.0.1:8088/nav/hud`; RSS<35MB; RAWV. Keel Sentry owns MCP/Tailscale/Composio strange-auth watch. This slice is HUD contract only.

## Goals

- Bind contract for loopback WebSocket HUD path.
- Enforce RSS < 35MB under normal nav load.
- Declare RAWV payload mode.
- Keep auth policy outside this change-id.

## Non-Goals

- Do not create/edit/overwrite any `SKILL.md` / skill-tree live lock files (Willow write lock).
- No MCP auth remediation ownership (Keel Sentry).
- No CONV2_B unpack; never CMV; girl-team not fifth mouths.
- No vibe; no Google Docs; no Vultr provision; no Cold Steel.
- Do not re-litigate PR #11 zenoh.

## Decisions

1. **Endpoint:** `ws://127.0.0.1:8088/nav/hud` only for this contract.
2. **Budget:** RSS < 35MB.
3. **Payload:** RAWV.
4. **Auth:** signal/log OK; Keel owns watch/remediation.

## Risks

| Risk | Mitigation |
|------|------------|
| RSS bloat | Hard <35MB requirement + scenario |
| Auth scope creep | HUD-only Non-Goal + scenario |
| Binding non-loopback | Spec fixes 127.0.0.1 |

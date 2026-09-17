# Tasks: add-phone-mcp-hud

## 1. Endpoint contract

- [ ] 1.1 Specify WebSocket listen `127.0.0.1:8088` path `/nav/hud`
- [ ] 1.2 Declare RAWV as frame/payload mode
- [ ] 1.3 Note Keel Sentry auth-watch coordination without implementing auth policy

## 2. Resource budget

- [ ] 2.1 Document RSS < 35MB acceptance check
- [ ] 2.2 Add stub process notes to keep HUD thin (no heavy deps in contract)

## 3. Verification

- [ ] 3.1 Exercise ADDED scenarios in `specs/phone-mcp-hud/spec.md`
- [ ] 3.2 Confirm no SKILL.md edits in this change

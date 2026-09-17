# S2-13 phone-MCP fixture

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-13-phone-fixture` |
| Slot | `S2-13` |
| Inclusion profile | **Ultra only** |
| Mode | Deterministic, repository-local fixture |
| Live device/provider access | None |

This file is the complete fixture contract for S2-13. The payload below is
intentionally small and contains no timestamps, generated identifiers,
destinations, credentials, or provider data. Consumers must treat an intent
not listed in `allowed_intents` as denied.

## Canonical fixture

```json
{
  "fixture_id": "s2-13-phone-mcp-default-deny-v1",
  "schema_version": "1",
  "source": "offline-fixture",
  "service": "phone-bridge",
  "allowed_intents": [
    "phone.health",
    "phone.fixture.read"
  ],
  "default_deny": true,
  "execution": {
    "device_access": false,
    "network_access": false,
    "provider_access": false,
    "subprocess_access": false
  },
  "cases": [
    {
      "case_id": "health-001",
      "intent": "phone.health",
      "decision": "allow",
      "result": {
        "status": "ok",
        "service": "phone-bridge",
        "version": "0.1.0",
        "capabilities": [
          "health",
          "offline-fixtures"
        ]
      }
    },
    {
      "case_id": "fixture-read-001",
      "intent": "phone.fixture.read",
      "decision": "allow",
      "result": {
        "source": "offline-fixture",
        "fixture_id": "s2-13-phone-mcp-default-deny-v1",
        "case_count": 5
      }
    },
    {
      "case_id": "sms-send-001",
      "intent": "phone.sms.send",
      "decision": "deny",
      "error": "default-deny"
    },
    {
      "case_id": "camera-capture-001",
      "intent": "phone.camera.capture",
      "decision": "deny",
      "error": "default-deny"
    },
    {
      "case_id": "unknown-001",
      "intent": "phone.unlisted.intent",
      "decision": "deny",
      "error": "default-deny"
    }
  ]
}
```

## Acceptance rules

1. Replaying the canonical payload produces the same case IDs, decisions, and
   values.
2. `phone.health` and `phone.fixture.read` are the only allowed intents.
3. SMS, camera, calls, contacts, and every unknown intent are denied without an
   opt-in path in this fixture.
4. A denied case produces no device, subprocess, network, or provider action.
5. The fixture may be loaded by an offline test, but it must not be used as a
   live phone or provider probe.

## Hard fences

- **Included Ultra only:** OD is excluded.
- No Willow `SKILL.md` is added, copied, or changed.
- No `CONV2_B` surface is included.
- Vultr and Cold Steel remain distinct; this fixture asserts neither as a
  phone runtime.
- No live phone, provider, network, or external service access is introduced.
- No secrets, credentials, tokens, private keys, destinations, or unredacted
  payloads are included.
- This file covers S2-13 only; no other S2 slot is modified.

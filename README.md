# sovereign-skills-archive

Receipt + index repo for the daily skill-library vacuum.

- Payload bytes: Google Drive parent `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`
- Receipts / manifests / inventory: `snapshots/YYYY-MM-DD/`
- Policy: `MASTER-INDEX.md`
- Claim: Liv HUB

## SPEC-002 offline acceptance tests

The offline pytest suite at
[`tests/test_spec_002_phone_mcp.py`](tests/test_spec_002_phone_mcp.py) maps
the safety-critical scenarios in
[`docs/openspec/SPEC-002-PHONE-MCP-INTENTS.md`](docs/openspec/SPEC-002-PHONE-MCP-INTENTS.md)
to an in-process contract harness. It performs no network I/O and proves the
negative boundaries with spies:

| SPEC-002 IDs | Coverage |
| --- | --- |
| `H-001`, `H-002`, `H-003`, `H-006` | Health readiness, side effects, offline Zenoh, and truthful bind failure |
| `I-001`, `I-002` | Named registry and undeclared-field rejection |
| `I-003`–`I-005` | Default-deny flashlight matrix and zero dispatch |
| `I-006`–`I-008` | Default-deny SMS, redaction, and no messaging-app lookup |
| `T-001`–`T-003` | Explicit non-wildcard Tailscale bind and fail-closed absence |
| `O-001`, `O-002` | Audit evidence and zero-dispatch instrumentation |

Run it offline with:

```bash
python3 -m pytest -q
```

Do not expect the 132M full tarball in git. Point at Drive file IDs instead.

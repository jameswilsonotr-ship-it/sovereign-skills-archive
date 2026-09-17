# Offline phone MCP harness

This is a deterministic, in-process stub for the SPEC-002 phone intents:

| Intent | Default | Explicit test opt-in |
| --- | --- | --- |
| `health` | allowed | n/a |
| `flashlight` | denied | in-memory state only |
| `sms` | denied | in-memory outbox only |

It does not import an MCP SDK, call Termux, spawn subprocesses, access the
network, read secrets, or require a phone. The `allow_side_effects=True`
constructor option is only for tests that need to verify the simulated success
path; it still cannot reach a device.

Run the focused harness with:

```bash
python -m pytest harness/tests
```

The stub supports direct intent dispatch with `handle_intent`, a small request
envelope with `dispatch`, and MCP-shaped `list_tools` / `call_tool` methods.

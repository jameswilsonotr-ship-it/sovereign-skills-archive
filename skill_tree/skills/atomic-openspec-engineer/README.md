# ATOMIC OpenSpec Engineer

Minimal local-first phone service contract.

## Development

Run the offline harness without installing application dependencies:

```bash
python -m pytest -q skill_tree/skills/atomic-openspec-engineer/harness
```

Run the stub manually:

```bash
PYTHONPATH=skill_tree/skills/atomic-openspec-engineer \
  python -m phone_service.app
```

Then request `http://127.0.0.1:8080/health`.

## Safety boundary

SMS and flashlight actions are policy-gated and denied by default. The stub
does not contact a network, send a message, control hardware, or read secrets.

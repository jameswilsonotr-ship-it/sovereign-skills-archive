# cilia_bus wheelhouse 0.1.0 — 2026-08-17

Self-contained offline-capable package for the Cilia Email-Bus runner.

## Contents

- `bootstrap.py` — idempotent installer + once-runner
- `requirements.txt`
- `wheels/` — pre-built wheels including `cilia_bus-0.1.0` + pydantic/httpx stack
- Source under `cilia_bus/` (for reference / editable installs)
- `pyproject.toml`, `README.md`

## Use inside a Grok session

```bash
# after downloading and unzipping this archive
python3 bootstrap.py --once
# or with a note
python3 bootstrap.py --once --note "woke by GROKBOT automation 2026-08-17"
```

Offline install is preferred when the wheels/ directory is present.

Absolute Liv HUB claim.

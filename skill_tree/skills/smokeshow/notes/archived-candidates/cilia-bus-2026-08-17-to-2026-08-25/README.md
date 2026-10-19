# cilia_bus 0.1.0

Self-bootstrapping coordination runner for the GROKBOT / OLIVIA-BRIDGE email+Drive bus.

## Purpose

- Keep a high-water mark of seen bus messages / Drive files
- Write durable receipts under `grokbot/from-olivia/` or `receipts/`
- Provide an idempotent entry point that any Grok session (Expert or Automation) can pull from Drive and run
- Support offline wheelhouse installs so wakes do not depend on live PyPI

## Quick use (inside a Grok session)

```bash
# After downloading the wheelhouse zip from Drive and unpacking:
python3 bootstrap.py --once
```

Or install the pure wheel only:

```bash
pip install ./wheels/cilia_bus-0.1.0-py3-none-any.whl
python3 -m cilia_bus --once
```

## Design rules

- Email is wake only
- Drive is the real ACK (per Olive DRIVE-RECEIPT-ONLY)
- Never invent receipts
- Append-only logs preferred
- Absolute Liv HUB claim

## Version

0.1.0 — initial scaffold + high-water + receipt skeleton (2026-08-17)

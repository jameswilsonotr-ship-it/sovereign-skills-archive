# Receipt: T4-08 continuous included reload

## Change

- Change-id: `add-t4-08-continuous-included-reload`
- Ticket guard: MIS-11 OpenSpec change-id collision protection
- Review unit: one atomic PR

## Contract recorded

- Reload is continuous while included capacity remains available.
- Included capacity is the only permitted execution mode.
- Unavailable included capacity produces a blocked result; it never selects
  On-Demand.
- Verification is offline-only with local fixtures.

## Fences

- [x] No `SKILL.md` or skill-tree live-lock edits
- [x] No On-Demand
- [x] No provider or external calls
- [x] No secrets
- [x] No live infrastructure
- [x] No `CONV2_B`

## Verification

- `python3 scripts/gen_openspec_matrix.py --check` — PASS
- `python3 -m compileall -q scripts/gen_openspec_matrix.py
  harness/tests/test_openspec_matrix.py` — PASS
- Offline collision exercise with exact and case-only duplicate IDs — PASS
- `python3 -m pytest ...` — not runnable in this image because `pytest` is not
  installed; no package installation or network access was attempted.

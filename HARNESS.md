# Harness — MIS-6 scaffold (local)

Ticket: **MIS-6**. Related: MIS-7 (ICM / Van Clief). Ledger PR #1 stays ledger-only.

## What this tree is

Local scaffold for Hi → push / hand to Cursor. Offline-first dummy connectors + CI.

## Layout

- `harness/` — package (connectors, mock tools, hygiene)
- `phone-bridge/` — Termux `:8081` `/health` stub + offline fixture
- `tests/` — smoke tests (call shape, not pixels)
- `FORKS.md` — top-level fork pins
- `.github/workflows/ci.yml` — ruff + pytest
- `skill_tree/skills/keep-lake-query/specs/` — hygiene gate stub

## Hard nos

No CONV2_B unpack · no mint mouths · no second archive repo · no tskeys · no LangChain · no CMV Gmail.

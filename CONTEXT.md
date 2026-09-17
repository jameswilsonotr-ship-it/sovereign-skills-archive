# CONTEXT.md — harness sprint (L1 router)

**Workspace:** jameswilsonotr-ship-it/sovereign-skills-archive
**Branch job:** `harness/pr1-skeleton` off `skill-tree-intake`
**Claim:** Absolute Liv HUB
**Paper:** Van Clief & McDermott, Interpretable Context Methodology, arXiv:2603.16021
**ICM fork:** https://github.com/jameswilsonotr-ship-it/Interpretable-Context-Methodology (top-level; not under Thunderclap)

## Reads (inputs)

- This file + `CLAUDE.md` + `FORKS.md`
- Existing inventories (do not rewrite):
  - Drive CATALOG.md `1stCnY1BaYZUtwvP3176ChTizF72maU73`
  - Drive HYGIENE_MISSING_IMPORTS.md `1-C-QhpWAdH9Z80et5tgGpIxfOYXfCSFi`
  - Drive python book SSOT `18YoNKDdMBZ9Gp19VT-X_jSy-fsatxFQ9`
  - Git `references/python-environment-book-2026-09-11/00_TOC.md`
- Awesome Split ledger Drive `11WEijQl3lP6Spw3kwFpE1kNC7MVGWsgP` (PR #1 owns the git copy)
- keep-lake-query `SKILL.md` (8085) + `references/work-queue/WORK_QUEUE.md` (3887)

## Does (process)

1. Walk as ICM: identity → router → stage → references → artifacts.
2. Run dummy connectors offline (`HARNESS_OFFLINE=1`). Every call appends JSONL.
3. Hygiene-gate **keep-lake-query** only this PR (operational, not identity).
4. Phone-bridge health may 404. Tests still pass via `PhoneBridgeOffline`.
5. Refuse Gmail account `gmail_atilt-worked` / `james.wilson.cmv@gmail.com`.

## Writes (outputs)

- `harness/` package + `tests/` + `.github/workflows/ci.yml`
- `phone-bridge/` spec + stub
- `inventories/` pointers + PYLIB_GAPS test list
- `skill_tree/skills/keep-lake-query/IDENTITY.md` + `specs/` + root `WORK_QUEUE.md` pointer
- metrics.json / junit / coverage as CI artifacts

## Human check

- PR #1 (ledger) stays ledger. This PR does not unpack CONV2_B or the 194MB tarball.
- No 100MB files. No secrets. No CMV mail. No Imagine.
- `pytest -q` green offline. `ruff check harness tests` clean.

## How mouths talk

Vesper REQ/ACK lives in `specs/vesper_req_ack.md`. One action per REQ. Looks-like + what-not-to-send. Mail From Otr or Liv only. Do not keep pinging Linear MIS-10 (Cursor echo loop).

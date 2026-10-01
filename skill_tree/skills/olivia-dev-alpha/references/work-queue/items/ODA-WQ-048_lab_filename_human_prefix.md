# ODA-WQ-048 — lab filenames: human prefix, short total
Status: **OPEN / PARKED — DO NOT RENAME EXISTING** 2026-09-11 05:18 EDT
Owner: olivia-dev-alpha
Claim: Liv HUB

Going forward only. Existing `20260911-0510EDT_ODA-LAB_extract-ALLNIGHT.ipynb` stays.

Law
- First token human-readable, ≤12 chars (`NIGHT`, `EXTRACT`, `INDEX`, `LABRUN`)
- Then `-` and a short code (job / version / hhmm)
- Whole basename ≤20 characters including extension when possible

Examples that fit
- `NIGHT-v1.ipynb` (13)
- `RUN-NIGHT.txt` (12)
- `IDX-NIGHT.md` (12)
- `OK-NIGHT.txt` (11)

Not `20260911-0510EDT_ODA-LAB_extract-ALLNIGHT.ipynb`.

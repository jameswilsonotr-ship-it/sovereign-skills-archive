# T4-31 / MIS-6 receipt

Status: `verified`

## Contract

- T4-31 reload mode: continuous, repository-local, offline only.
- Capacity mode: `included` only.
- On-Demand: forbidden; no fallback, increase, recommendation, or use.
- Baseline: preserved MIS-6 offline fixture on `skill-tree-intake`.

## Fences

- No `SKILL.md` or skill-tree live-lock changes.
- No `CONV2_B` material.
- No external/provider access, secrets, browser, billing, or hosted
  provisioning.
- No remote reload or live connector execution.

## Changed paths

- `docs/openspec/burn-flip/add-continuous-included-reload/proposal.md`
- `docs/openspec/burn-flip/add-continuous-included-reload/design.md`
- `docs/openspec/burn-flip/add-continuous-included-reload/specs/continuous-included-reload/spec.md`
- `docs/openspec/burn-flip/add-continuous-included-reload/tasks.md`
- `docs/burn-wave/T4-31_MIS-6_RECEIPT.md`

## Verification

- The T4-31 OpenSpec scenarios cover included success, blocked capacity,
  successive local cycles, baseline drift, offline execution, and one receipt
  per cycle.
- The MIS-6 fixture remains outside this diff.
- The diff contains documentation only.

No credentials, tokens, connection strings, or payload copies are included.

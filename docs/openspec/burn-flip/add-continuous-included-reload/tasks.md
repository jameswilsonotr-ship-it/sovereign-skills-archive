# Tasks: add-continuous-included-reload

## 1. Contract

- [x] 1.1 Define T4-31 as a continuous local reload.
- [x] 1.2 Lock included-only behavior; On-Demand is forbidden.
- [x] 1.3 Preserve the MIS-6 fixture as the reload baseline.

## 2. Fences

- [x] 2.1 Prohibit `SKILL.md` and skill-tree live-lock edits.
- [x] 2.2 Prohibit `CONV2_B`, external/provider access, secrets, and hosted
  provisioning.
- [x] 2.3 Prohibit browser, network, billing, and remote reload operations.

## 3. Verification

- [x] 3.1 Exercise the ADDED scenarios in
  `specs/continuous-included-reload/spec.md` by inspection.
- [x] 3.2 Emit the T4-31/MIS-6 secret-free receipt.
- [x] 3.3 Confirm the MIS-6 fixture is unchanged in this delta.

This slice is documentation-only. It does not add credentials, tokens,
connection strings, provider clients, or live execution.

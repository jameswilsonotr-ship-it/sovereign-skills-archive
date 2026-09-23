# T4-19 — E1–E5 sit-sheet companion checklist

**Status:** ready for an offline sit
**Mode:** `CONTINUOUS`
**Inclusion:** `INCLUDED`
**Reload:** continuous included reload
**On-Demand:** forbidden

This is the companion sit sheet for T4-19. It is a verification checklist, not
a request to add a provider, network integration, secret, or runtime dependency.
Every check below must be run against local fixtures/stubs only.

## Non-negotiable contract

- The T4-19 surface is **included** in the continuously loaded set.
- Changes to an included surface are observed and reloaded continuously.
- Reload is idempotent: one source change produces one effective current state.
- A reload never falls back to a stale included copy.
- There is no On-Demand mode, manual-load switch, lazy registration path, or
  opt-in gate in the T4-19 contract.
- An offline run must not contact any external service or provider and must not
  read secrets.

## E1 — Identify the included surface

- [ ] Record the exact local fixture/input representing T4-19.
- [ ] Record the local included-set manifest or equivalent source of truth.
- [ ] Confirm T4-19 is present in that included set before the first reload.
- [ ] Record the expected current version or content digest.
- [ ] Confirm no On-Demand selector is part of the input contract.

**Evidence:** `______________________________________________`

## E2 — Verify continuous wiring

- [ ] Start the loader using the offline test harness.
- [ ] Confirm the initial state is `CONTINUOUS` + `INCLUDED`.
- [ ] Confirm the observer/reload path is active without a manual trigger.
- [ ] Confirm a changed included fixture schedules a reload automatically.
- [ ] Confirm no On-Demand branch, flag, command, or fallback is exercised.

**Evidence:** `______________________________________________`

## E3 — Exercise reload behavior

- [ ] Change the local T4-19 fixture once.
- [ ] Observe the automatic reload and record its event/version.
- [ ] Confirm the loaded state matches the changed fixture.
- [ ] Repeat the same notification and confirm the result is idempotent.
- [ ] Make a second change and confirm the newest included state wins.
- [ ] Confirm no duplicate registration, stale state, or manual-load prompt occurs.

**Evidence:** `______________________________________________`

## E4 — Run the offline fence

- [ ] Run with network access disabled or mocked closed.
- [ ] Use only local fixtures, deterministic stubs, and local assertions.
- [ ] Confirm no external/provider call is attempted.
- [ ] Confirm no secret lookup, secret value, or credential-bearing input is used.
- [ ] Confirm no Vultr integration or deployment action is referenced by the run.
- [ ] Confirm the run does not depend on `Willow SKILL.md` or `CONV2_B`.

**Evidence:** `______________________________________________`

## E5 — Sign off the sit

- [ ] Capture the final T4-19 mode/inclusion/reload values.
- [ ] Attach the E1–E4 evidence or local log references.
- [ ] Mark every unchecked item either `PASS` after evidence or `N/A` with a
  reason; do not silently skip a failed check.
- [ ] Record the offline command/test harness used.
- [ ] Write the receipt with the commit and changed-path list.

**Result:** `PASS / FAIL`

**Operator:** `__________________`  **UTC:** `__________________`

**Notes:**
`________________________________________________________________________`
`________________________________________________________________________`

## Acceptance gate

T4-19 passes only when E1–E5 are evidenced and the final state remains
**CONTINUOUS + INCLUDED + continuously reloaded**. Any On-Demand behavior is a
failure, even if the loaded output is otherwise correct.

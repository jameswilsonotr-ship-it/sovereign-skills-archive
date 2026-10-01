# T4-14 — E1–E5 Cursor-delegation sit-sheet

Status: ready for an offline sit

## Contract

T4-14 is **CONTINUOUS INCLUDED reload**. The reload path is part of the
included baseline and remains active for the lifetime of the local session.
It must not be exposed, selected, or downgraded as an On-Demand capability.

The sit is evidence-driven: Cursor delegates each check to the local harness,
the harness records the observed result, and a human can replay the same check
without network access.

## Fences

The sit is local and offline only.

- Do not read, copy, package, or execute `Willow SKILL.md`.
- Do not read, copy, package, or execute `CONV2_B`.
- Do not contact an external service or provider.
- Do not use credentials, secret material, or a Vultr resource.
- Do not add an OD/On-Demand switch, fallback, flag, route, or fixture.

Any fence violation is a failed sit, even when the reload assertion passes.

## Evidence matrix

| ID | Cursor delegates | Local observation | Pass condition |
|---|---|---|---|
| E1 | Validate the policy declaration and its default. | Inspect the T4-14 configuration and startup trace. | Reload is marked `continuous` and `included`; no On-Demand mode is present. |
| E2 | Validate first-session availability. | Start the local harness with an empty reload cache. | The included reload becomes available during startup without a user action or mode selection. |
| E3 | Validate continuous reload. | Change the local test fixture once, then wait for the harness event/interval. | The included surface refreshes automatically and records a reload event. |
| E4 | Validate delegation boundaries. | Run the checks through Cursor’s local delegation entry point. | Cursor delegates only to the offline harness; no network, provider, credential, or external-resource operation occurs. |
| E5 | Validate negative controls and receipt completeness. | Search the run output and changed files for forbidden modes and fenced inputs. | No On-Demand/OD path, forbidden input, external/provider access, secret, or Vultr reference is used as an operation. |

## Local run sheet

Run these checks from the repository root. Replace the placeholders with the
repository’s existing local harness commands; do not install a dependency or
fetch a fixture for this sit.

```text
[ ] E1  policy/default inspection
[ ] E2  cold-start included availability
[ ] E3  automatic fixture-change reload
[ ] E4  Cursor -> local harness delegation
[ ] E5  fence scan + receipt capture
```

For each check, record:

```text
ID: E1 | E2 | E3 | E4 | E5
delegate: Cursor
execution: local/offline
observed:
evidence:
result: PASS | FAIL
```

## Acceptance criteria

The sit is accepted only when all five checks pass and the following
invariants hold:

1. `continuous` and `included` are true for the same reload path.
2. Reload occurs without an On-Demand/OD trigger or user mode selection.
3. A local fixture change is sufficient to produce observable reload evidence.
4. Cursor delegation stays inside the local offline harness.
5. The receipt names the five results and records no network or secret use.

If any check fails, stop at the failed check, preserve its local evidence, and
do not substitute an On-Demand run.

## Receipt

```text
work item: T4-14
surface: CONTINUOUS INCLUDED reload
delegation: Cursor -> local offline harness
checks: E1 E2 E3 E4 E5
network: not used
secrets: not used
external/provider resources: not used
result: pending local sit
```

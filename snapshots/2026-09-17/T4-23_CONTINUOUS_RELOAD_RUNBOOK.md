# T4-23 — Continuous Included Reload

Status: normative runbook note
Mode: offline only
Source policy: included artifacts only

## Invariant

The reload path is continuous and included by default. Each completed reload
cycle immediately establishes the next cycle from the local included set.
There is no user-triggered or demand-triggered reload path.

The included set is the local, pinned input surface for the run. A cycle may
read that surface and its local manifest, but it must not acquire additional
inputs. If the included set or its manifest is unavailable, the cycle fails
closed and records the failure; it does not fall back to another source.

## Hard fences

- No Willow `SKILL.md`.
- No `CONV2_B`.
- No external, provider, secret, or Vultr input.
- On-Demand (OD) is forbidden. The required OD count is `0`.

These fences apply to every reload cycle, including recovery and validation.

## Cycle procedure

1. Read the local included manifest and resolve only the artifacts listed
   there.
2. Reload the resolved included artifacts as one cycle. Do not add an
   optional or demand-selected input.
3. Record cycle status and the OD counter. A successful cycle must report
   `OD=0`.
4. Start the next cycle from the same included-only policy. A missing,
   malformed, or fenced input is a fail-closed result, not a reason to
   broaden the source set.
5. Retain the cycle record with the run receipt so the continuous behavior
   and `OD=0` result can be checked offline.

## Acceptance checks

| Check | Required result |
|---|---|
| Reload mode | continuous |
| Input surface | local included artifacts only |
| OD counter | `0` |
| Network/provider access | `0` |
| Fenced inputs | `0` |
| Recovery behavior | fail closed |

Any non-zero OD count, any non-included input, or any network/provider access
fails T4-23. Do not retry by switching modes.

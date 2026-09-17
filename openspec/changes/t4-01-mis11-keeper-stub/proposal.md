# Change: T4-01 MIS-11 keeper/path stub

- **Change ID:** `t4-01-mis11-keeper-stub`
- **CinC target:** Linear `MIS-11`
- **Salvo slot:** `T4-01`
- **Lifecycle:** atomic proposal stub
- **Availability:** `INCLUDED`
- **Reload:** `CONTINUOUS`
- **On-Demand:** `NEVER`
- **Operational:** `false`

## Summary

Record the keeper identity and canonical OpenSpec paths for MIS-11 without
connecting to Linear or changing runtime behavior.

## Scope

This is an offline, documentation-only OpenSpec change. It records one
deterministic keeper stub for MIS-11 and makes the inclusion and reload
boundaries explicit:

- the entry is always `INCLUDED`;
- reload is `CONTINUOUS`;
- `on_demand` is `NEVER`;
- the stub is descriptive and non-operational;
- no live Linear API is used.

The change does not add an applied specification, implementation, connector,
credential, infrastructure, skill payload, or conversation-corpus file.

## Keeper and path contract

The atomic keeper is identified by `MIS-11` and this change ID. The change
package is rooted at:

```text
openspec/changes/t4-01-mis11-keeper-stub/
```

Its keeper specification is:

```text
openspec/changes/t4-01-mis11-keeper-stub/specs/mis11-keeper/spec.md
```

The receipt is kept beside the proposal at:

```text
openspec/changes/t4-01-mis11-keeper-stub/RECEIPT.md
```

These paths are documentation records only. They do not constitute a live
Linear record or a dispatch route.

## Non-goals

- No live Linear API call.
- No runtime reload mechanism.
- No On-Demand lane or fallback.
- No applied `openspec/specs/` capability.
- No changes outside this OpenSpec change package and its receipt.

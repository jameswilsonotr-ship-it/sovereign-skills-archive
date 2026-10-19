# Change: Proposal stub hygiene for parked IDs

- **Change ID:** `third-salvo-16-proposal-stub-hygiene`
- **Salvo slot:** `T3-16`
- **Lifecycle:** proposal-only
- **Availability:** `INCLUDED Ultra ONLY`
- **On-Demand:** `NEVER`

## Why

Parked IDs need proposal stubs that are unambiguous at a glance. A stub that
omits its lifecycle or lane can be mistaken for a live entry, a promotion
request, or an On-Demand route.

## Scope

This change defines the minimum metadata and wording for a parked-ID proposal
stub:

1. Keep the canonical ID unchanged and unique.
2. Mark the entry as `parked`.
3. Mark availability as `INCLUDED Ultra ONLY`.
4. Mark On-Demand dispatch as `NEVER`.
5. State that the stub is descriptive and non-operational.

The change applies to proposal stubs produced from the authoritative parked-ID
list. It does not invent, rename, promote, or activate IDs.

## Stub shape

Each parked-ID stub MUST carry this metadata before any descriptive prose:

```yaml
id: <canonical-parked-id>
status: parked
availability: INCLUDED Ultra ONLY
on_demand: NEVER
operational: false
```

The body MAY explain why the ID is parked or what evidence would be needed for
a future review. It MUST NOT read like an activation instruction, a live
dispatch contract, or a promotion record.

## Hygiene rules

- IDs are compared in canonical form and may appear only once per stub set.
- `status: parked` is not equivalent to approved, live, enabled, or routed.
- `availability: INCLUDED Ultra ONLY` is an inclusion boundary, not a request
  to broaden exposure.
- `on_demand: NEVER` is a hard prohibition; no fallback or inferred route may
  override it.
- Proposal text remains inert until a separately approved change promotes an
  ID.

## Non-goals

- No runtime, routing, or registry implementation.
- No promotion or activation of parked IDs.
- No new IDs or aliases.
- No changes to skill payloads or agent behavior.

## Acceptance criteria

- [ ] The change is stored under the exact change ID.
- [ ] Every parked-ID stub begins with the required five metadata fields.
- [ ] Every stub says `INCLUDED Ultra ONLY` and `NEVER` for On-Demand dispatch.
- [ ] Duplicate or non-canonical IDs are rejected during review.
- [ ] The change contains proposal/specification material only; no live behavior
      changes are included.

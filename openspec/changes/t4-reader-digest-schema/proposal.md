# T4-READER digest schema

## Summary

Define a thin, offline contract for the trusted Cursor report-reader fish in
the ORCH LADDER. It accepts a pre-captured CA/PR landing digest and renders
three short desk views: Mag, Liaison, and fleet.

The reader is **T4-READER / Included Ultra** only. The contract is deliberately
not an execution or ingestion interface: it reads a local/pasted digest and
emits a Markdown one-pager.

## Motivation

CA and PR landing notes currently need to be reshaped by hand before they can
be handed to the three desks. A small stable input shape and a single output
layout make the handoff repeatable without expanding the reader into a live
integration.

## Scope

### In scope

- A compact YAML-shaped digest schema.
- A Markdown one-pager template with Mag, Liaison, and fleet sections.
- A synthetic sample showing the transformation.
- Acceptance rules for provenance, uncertainty, and offline operation.

### Out of scope

- Fetching, polling, or posting to any service.
- Credentials, network configuration, or automation.
- Changes to any skill library or runtime.
- On-demand execution. `on_demand` is always `false`.

## Invariants

Every rendered digest MUST carry:

```yaml
reader: T4-READER
tier: INCLUDED Ultra
orchestration: ORCH LADDER
on_demand: false
delivery: offline
```

The reader MUST preserve the distinction between confirmed facts, reported
claims, and unknowns. It MUST never invent an owner, deadline, status, or
source reference.

## Acceptance criteria

- A reviewer can validate the input using the documented fields alone.
- The output is one Markdown page with all three desk sections present.
- Every action has an owner or is explicitly marked `unassigned`.
- Each material statement has a local source reference or is marked
  `unverified`.
- The sample can be rendered without a network, credential, or service call.

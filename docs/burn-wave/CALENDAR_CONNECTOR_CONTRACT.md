# S2-20 Calendar Connector Contract

**OpenSpec change-id:** `second-salvo-20-calendar-contract`
**Slot:** S2-20
**Status:** contract only; no implementation or provider connection

## Purpose

This document defines one provider-neutral calendar connector boundary for the
included **Ultra** surface. It specifies the event shape, read/write boundary,
identity and time rules, and deterministic conflict behavior so an adapter can
be implemented later without changing the consumer contract.

The connector is an input boundary. It does not decide whether an appointment
should be accepted, moved, cancelled, or disclosed to another person. Those
actions remain outside this contract.

## Scope and hard fences

In scope:

- one normalized calendar connector contract;
- read-oriented event retrieval and an explicit dry-run conflict result;
- deterministic detection and reporting of overlapping events;
- provenance, failure, and redaction rules.

Out of scope:

- live calendar access, provider calls, synchronization, webhooks, or OAuth;
- creating, updating, deleting, moving, or accepting calendar events;
- provider-specific credentials, IDs, URLs, SDKs, or secrets;
- OD;
- Willow `SKILL.md`;
- `CONV2_B`;
- Vultr or any infrastructure deployment;
- treating Vultr as Cold Steel;
- any other S2 slot.

“Included Ultra” is the only capability tier covered here. A caller that is
not operating in that tier MUST reject the request as unsupported rather than
silently widening this contract.

## Connector boundary

An implementation MUST expose the following logical operation:

```text
list_events(request) -> EventPage | ConnectorError
```

The operation is read-only. The request MUST contain:

| Field | Requirement |
| --- | --- |
| `window_start` | Inclusive instant in ISO 8601 UTC form |
| `window_end` | Exclusive instant in ISO 8601 UTC form; after `window_start` |
| `calendar_scope` | Opaque caller-selected scope; never a provider credential |
| `page_token` | Optional opaque continuation token |
| `include_cancelled` | Explicit boolean; default is `false` |

The response MUST contain:

```text
EventPage {
  events: NormalizedEvent[]
  next_page_token: opaque | null
  source: "calendar-connector"
  contract_version: "s2-20.v1"
}
```

An adapter MUST NOT add provider-specific fields to the consumer-facing
contract. Provider details may remain in an internal adapter boundary only if
they are not returned, logged, or persisted by this contract.

## Normalized event

Every returned event MUST have:

| Field | Type / rule |
| --- | --- |
| `event_key` | Stable opaque key within the connector scope; not a secret |
| `title` | Display text; may be redacted |
| `start` | Inclusive UTC instant |
| `end` | Exclusive UTC instant; strictly after `start` |
| `status` | `confirmed`, `tentative`, or `cancelled` |
| `visibility` | `public`, `private`, or `unknown` |
| `calendar_key` | Stable opaque calendar key |
| `source_revision` | Opaque revision for repeatable reads; nullable |
| `redacted` | Boolean indicating whether content was minimized |

Optional fields are limited to:

- `location_label`, which MUST be a label rather than coordinates or access
  details;
- `notes_present`, a boolean; note contents MUST NOT be returned;
- `recurrence_instance_key`, an opaque key for one expanded occurrence.

All instants MUST be normalized to UTC before overlap evaluation. A malformed
event MUST be rejected as an event-level validation error and MUST NOT be
silently repaired. An invalid page request MUST fail the whole operation.

## Read and privacy rules

The connector MUST:

1. use least-privilege read access when an implementation exists;
2. return only the requested time window;
3. minimize private titles, notes, locations, and attendee data;
4. avoid attendee email addresses, meeting links, tokens, and raw provider
   payloads in the normalized result;
5. make redaction visible through `redacted: true`;
6. avoid logging request contents, event titles, or opaque credentials.

The contract does not define authentication. Secrets MUST be supplied by an
external runtime secret store if a future adapter requires them; they MUST
never be placed in this document, source control, fixtures, or examples.

## Conflict definition

For two non-cancelled events `A` and `B`, a conflict exists exactly when their
half-open intervals overlap:

```text
A.start < B.end AND B.start < A.end
```

Therefore:

- an event ending exactly when another begins is **not** a conflict;
- cancelled events do not conflict;
- zero-length or backwards intervals are invalid, not conflict-free;
- each recurring occurrence is evaluated independently after expansion;
- an event conflicts with another event in the same result set only when both
  are visible to the caller under the requested `calendar_scope`.

The conflict detector MUST produce a pairwise result with no duplicate pair:
the pair key is the lexicographically ordered tuple
`(event_key_a, event_key_b)`.

## Conflict behavior

Conflict evaluation is non-mutating and MUST return one of these outcomes:

| Outcome | Meaning | Required behavior |
| --- | --- | --- |
| `clear` | No valid overlapping pair | Continue with the event set |
| `conflict` | One or more overlapping pairs | Preserve all events; report every pair |
| `indeterminate` | A required event or page could not be read | Do not claim `clear`; report the cause |
| `invalid` | Input or event validation failed | Reject the affected request/event with a stable error code |

For `conflict`, each pair MUST include:

```text
ConflictPair {
  pair_key: string
  event_key_a: opaque
  event_key_b: opaque
  overlap_start: UTC instant
  overlap_end: UTC instant
  severity: "hard" | "soft"
}
```

`overlap_start` is the later start, and `overlap_end` is the earlier end.
`severity` is `hard` when both events are `confirmed`; it is `soft` when at
least one event is `tentative`. Severity is descriptive only: the connector
MUST NOT auto-resolve either event.

When multiple conflicts exist, results MUST be sorted by
`(overlap_start, pair_key)`. The connector MUST preserve the source events and
MUST NOT choose a winner, reschedule, cancel, accept, or notify.

## Determinism and failure handling

For the same source revision, scope, and time window, an implementation SHOULD
return the same normalized event set and conflict ordering. If pagination
cannot provide a consistent read, the result MUST be `indeterminate` rather
than a partial `clear`.

Stable error categories are:

| Code | Meaning |
| --- | --- |
| `UNSUPPORTED_TIER` | Caller is outside included Ultra |
| `INVALID_WINDOW` | Window is malformed or reversed |
| `EVENT_INVALID` | An event violates the normalized schema |
| `PAGE_UNAVAILABLE` | A required page could not be read |
| `SOURCE_UNAVAILABLE` | The connector source cannot be reached |
| `SCOPE_DENIED` | Requested scope is not readable |
| `REDACTION_REQUIRED` | Data cannot be safely minimized |

Errors MUST include the stable code and a safe human-readable message. They
MUST NOT include secrets, authorization headers, raw provider responses, or
private event contents.

## Acceptance checks for a future implementation

- Supports only the `s2-20.v1` shape and included Ultra tier.
- Performs no mutation through `list_events`.
- Uses UTC half-open intervals and excludes boundary-touching events.
- Excludes cancelled events from conflicts.
- Reports all unique overlapping pairs in deterministic order.
- Returns `indeterminate` for incomplete reads instead of claiming `clear`.
- Redacts sensitive fields and never exposes secrets or raw provider payloads.
- Keeps adapter/provider behavior behind this provider-neutral boundary.

## Receipt

- Change-id: `second-salvo-20-calendar-contract`
- Slot: S2-20
- Artifact: `docs/burn-wave/CALENDAR_CONNECTOR_CONTRACT.md`
- Included capability: Ultra only
- Live calendar/provider access: none
- Secrets: none
- Other S2 slots modified: none

# T4-READER digest schema

This is a local input contract for a trusted Cursor report-reader fish in the
ORCH LADDER. It accepts a pasted or file-local CA/PR landing digest and feeds
the one-page layout in
[`t4-reader-one-pager-template.md`](t4-reader-one-pager-template.md).

## Fixed envelope

These values are constants, not caller choices:

```yaml
reader: T4-READER
tier: INCLUDED Ultra
orchestration: ORCH LADDER
delivery: offline
on_demand: false
```

Reject the digest if any fixed value differs.

## Digest shape

```yaml
digest_id: "local-2026-09-17-a"
captured_at_utc: "2026-09-17T09:00:00Z"
reader: T4-READER
tier: INCLUDED Ultra
orchestration: ORCH LADDER
delivery: offline
on_demand: false
window: "2026-09-17T08:00Z/2026-09-17T09:00Z"
entries:
  - id: "ca-001"
    kind: ca
    title: "Short landing title"
    status: landed
    certainty: confirmed
    summary: "One sentence describing only what landed."
    source_ref: "local:ca/001"
    owner: "owner-handle"
    next_action: "Specific follow-up, or none"
    desk_relevance:
      mag: "Why the item matters to the message desk"
      liaison: "Coordination or handoff"
      fleet: "Operational effect or checkpoint"
```

## Field rules

| Field | Type / allowed values | Rule |
|---|---|---|
| `digest_id` | non-empty string | Stable for this local digest |
| `captured_at_utc` | UTC timestamp | Time the source text was captured |
| `reader` | `T4-READER` | Fixed envelope |
| `tier` | `INCLUDED Ultra` | Fixed envelope |
| `orchestration` | `ORCH LADDER` | Fixed envelope |
| `delivery` | `offline` | Fixed envelope |
| `on_demand` | `false` | Fixed envelope |
| `window` | non-empty string | Source coverage window |
| `entries` | list | May be empty |
| `id` | non-empty string | Unique within the digest |
| `kind` | `ca` or `pr` | Landing source class |
| `title` | non-empty string | Human-readable item name |
| `status` | `landed`, `partial`, or `blocked` | What the source says |
| `certainty` | `confirmed`, `reported`, or `unknown` | Never infer this label |
| `summary` | non-empty string | Source-faithful statement |
| `source_ref` | non-empty local reference | Use `unverified` if absent |
| `owner` | string | Use `unassigned` when absent |
| `next_action` | string | Use `none` when no action exists |
| `desk_relevance.*` | string | Use `none` when not applicable |

The three `desk_relevance` keys are required even when their value is
`none`. They are editorial routing hints, not new facts.

## Rendering rules

1. Copy the fixed envelope into the page header and footer.
2. Put every entry in the landing table, preserving `status`, `certainty`,
   `owner`, and `source_ref`.
3. Use the three relevance values to populate the matching desk sections.
4. Prefix missing evidence with `unverified`; never replace it with a guess.
5. Put `next_action` in the action queue with its owner.
6. If `entries` is empty, use `no landed items` in every desk section.
7. Keep the result to one page: one sentence per entry per desk, plus the
   action queue.

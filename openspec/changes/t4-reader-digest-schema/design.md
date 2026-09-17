# Design

## Flow

```text
local CA/PR landing digest
        |
        v
validate fixed metadata + entries
        |
        v
retain fact/claim/unknown labels
        |
        v
render one Markdown page
  ├─ Mag desk
  ├─ Liaison desk
  └─ fleet desk
```

The transformation is deterministic and editorially narrow. It reorganizes
the supplied material; it does not enrich, reconcile, or infer facts.

## Input contract

The canonical field list is in
[`report-reader/t4-reader-digest-schema.md`](../../report-reader/t4-reader-digest-schema.md).
The top-level metadata establishes the reader fence. Each entry is a landing
event from either a CA report or a PR landing note.

Required entry fields:

- `id`
- `kind`
- `title`
- `status`
- `certainty`
- `summary`
- `source_ref`
- `owner`
- `next_action`
- `desk_relevance`

`owner`, `next_action`, or `desk_relevance` may be explicitly
`unassigned`, `none`, or `not_applicable`; empty strings are invalid.

## Output contract

The template emits:

1. a provenance header;
2. a three-line situation summary;
3. one compact table of landed items;
4. one bounded section for each desk;
5. unresolved items and a next checkpoint;
6. a footer repeating the offline and no-on-demand fence.

The desk sections answer different questions without changing the source
facts:

| Desk | Question answered |
|---|---|
| Mag | What is the message and why does it matter? |
| Liaison | Who needs to coordinate, and what handoff is needed? |
| fleet | What is the operational state, risk, and next checkpoint? |

## Failure behavior

- Missing fixed metadata: reject the digest.
- Unknown `kind`, `status`, or `certainty`: reject the affected entry and
  report the field; do not silently coerce it.
- Missing evidence: retain the entry with `unverified` and a visible
  follow-up, unless the entry has no title or summary at all.
- No entries: render an empty one-pager stating `no landed items`.

# T4-READER sample — offline only

The source below is synthetic. It is sufficient to render the one-pager that
follows without a network or any additional context.

## Input digest

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
    title: "T4 reader package landed"
    status: landed
    certainty: confirmed
    summary: "The reader package and local validation notes are present."
    source_ref: "local:ca/001"
    owner: "rhea"
    next_action: "Carry the package state to the Mag desk."
    desk_relevance:
      mag: "A small reader package is ready for desk use."
      liaison: "No handoff is needed beyond the desk note."
      fleet: "No runtime change; package is local and ready."
  - id: "pr-014"
    kind: pr
    title: "Digest schema change prepared"
    status: partial
    certainty: reported
    summary: "The schema and template are prepared; review is still open."
    source_ref: "local:pr/014"
    owner: "sam"
    next_action: "Confirm the review outcome before calling it landed."
    desk_relevance:
      mag: "The contract is nearly ready but should not be called final."
      liaison: "Sam owns the review confirmation."
      fleet: "Keep the next checkpoint at review confirmation."
```

## Rendered one-pager

# T4-READER — local-2026-09-17-a

**Captured:** 2026-09-17T09:00:00Z · **Window:** 2026-09-17T08:00Z/2026-09-17T09:00Z  
**Reader:** T4-READER · **Tier:** INCLUDED Ultra · **Orchestration:** ORCH LADDER  
**Delivery:** offline · **On-demand:** false

## Situation

One CA package landed; one PR item is partial and remains reported pending review confirmation.

## Landed

| ID | Kind | Landing / status | Certainty | Owner | Source |
|---|---|---|---|---|---|
| ca-001 | ca | T4 reader package landed — landed | confirmed | rhea | local:ca/001 |
| pr-014 | pr | Digest schema change prepared — partial | reported | sam | local:pr/014 |

## Mag desk

**Message:** A small reader package is ready for desk use; the related contract is nearly ready.  
**Signal:** `ca-001` confirmed; `pr-014` reported.  
**Line to carry:** The package is ready, while the contract remains pending review confirmation.

## Liaison desk

**Handoff:** Sam confirms the review outcome for `pr-014`.  
**Open dependency:** Review confirmation — sam — `local:pr/014`.  
**Unverified:** None beyond the reported `pr-014` review state.

## fleet desk

**Operational state:** The local package is landed; the schema change is partial.  
**Risk:** Do not treat `pr-014` as final until review confirmation.  
**Next checkpoint:** Sam confirms review outcome — `pr-014`.

## Action queue

| Action | Owner | Source | State |
|---|---|---|---|
| Carry the package state to the Mag desk. | rhea | ca-001 | open |
| Confirm the review outcome before calling it landed. | sam | pr-014 | unverified |

> Offline local digest. No live read or write is implied. `on_demand` remains
> `false`.

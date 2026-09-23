# Design: add-t4-06-continuous-included-reload

## Context

T4-06 is a post-T3 Keeper delta. The useful artifact is a thin map of local
state and pointers, not a second lake. A reload may run continuously, but
every cycle is bounded by the local post-T3 input and the already-included
execution budget.

This change is a contract and map delta only. It does not perform a live
reload, contact a service, or infer a missing T3 record.

## Goals

- Make continuous reload deterministic and included-only.
- Keep the Keeper map thin: keys, status, source pointer, and disposition.
- Preserve the dated-tree/DELTA/KEEP/receipt boundaries.
- Make duplicate, missing, and unknown input outcomes explicit.
- Leave a machine- and human-readable receipt for the offline review.

## Non-Goals

- Do not create, edit, or overwrite any `SKILL.md` or Willow live-lock file.
- Do not unpack or rebuild `CONV2_B`.
- Do not call an external service, provider, cloud API, or secret-bearing
  integration.
- Do not perform Vultr work.
- Do not use or increase On-Demand capacity, spend, or fallback.
- Do not slurp, copy, or rewrite the historical KEEP lake.
- Do not fabricate post-T3 content, dates, twins, or shards.

## Decisions

1. **Input:** each cycle reads only a local, committed post-T3 delta or
   receipt. An absent input yields `NO_TWIN`; an input without a resolvable
   map target yields `NO_SHARD`.
2. **Mode:** the reload mode is `CONTINUOUS_INCLUDED`. It is valid only while
   the work remains within already-included execution. There is no
   On-Demand fallback state.
3. **Map shape:** the delta stores `delta_id`, `source_ref`, `map_key`,
   `status`, `disposition`, and `recorded_at`. It stores pointers, not source
   bodies.
4. **Append/overlay:** a new delta appends one map record. Existing records
   are not rewritten. A repeated `delta_id` is `SKIP_EXISTING` and has no
   second effect.
5. **Honest gaps:** `NO_TWIN`, `NO_SHARD`, and `UNKNOWN` are terminal
   observations for the cycle; they do not trigger a lookup outside the
   local input set.
6. **Verification:** review is offline and checks paths, text, and diffs
   only. No network, provider, secret, or live-cloud action is part of
   acceptance.

## Risks

| Risk | Mitigation |
|------|------------|
| A continuous loop grows the map into a second lake | Store only bounded pointers and statuses |
| Reload repeats a delta | Key by `delta_id` and return `SKIP_EXISTING` |
| A missing post-T3 source is silently filled | Return `NO_TWIN`/`NO_SHARD`; never infer |
| A budget boundary opens an unintended path | Included-only invariant; no fallback state |
| A review touches a locked surface | Explicit `SKILL.md` and live-lock non-goal |

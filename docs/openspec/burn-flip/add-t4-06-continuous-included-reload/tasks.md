# Tasks: add-t4-06-continuous-included-reload

## 1. Contract lock

- [x] 1.1 Lock reload mode to `CONTINUOUS_INCLUDED`.
- [x] 1.2 State that On-Demand is forbidden, including fallback, spend, and
  mutation paths.
- [x] 1.3 Define local post-T3 input and the `NO_TWIN`/`NO_SHARD` outcomes.

## 2. Thin Keeper delta

- [x] 2.1 Define the bounded map record:
  `delta_id`, `source_ref`, `map_key`, `status`, `disposition`, and
  `recorded_at`.
- [x] 2.2 Require append-only overlay behavior and `SKIP_EXISTING`
  idempotence.
- [x] 2.3 Keep dated-tree, DELTA, KEEP, and receipt surfaces distinct.

## 3. Offline verification

- [x] 3.1 Exercise the included, missing-input, duplicate, unresolved, and
  offline-review scenarios in `specs/included-reload/spec.md`.
- [x] 3.2 Confirm no `SKILL.md` or Willow live-lock path is changed.
- [x] 3.3 Confirm the receipt records the single change-id, changed paths,
  and local-only verification.

Verification is documentation-only. This change contains no credentials,
tokens, connection strings, provider configuration, or other secrets.

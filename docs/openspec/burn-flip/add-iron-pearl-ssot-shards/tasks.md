# Tasks: add-iron-pearl-ssot-shards

## 1. SSoT layout

- [x] 1.1 Declare Awesome Split / HANDOFF SSoT paths per Iron Pearl BASIC
  SPEC-001
- [x] 1.2 Initialize the exact eight-slot shard map with ownership labels
- [x] 1.3 Ban Google Docs in the layout contract notes

## 2. Delta CAS

- [x] 2.1 Specify `base_version` and `next_version` on delta writes
- [x] 2.2 Define stale-write failure and retry-from-head behavior
- [x] 2.3 Add a stale-conflict example to these verification notes

### Verification note: stale conflict

1. The current SSoT head is version `12`.
2. A writer submits a `slot-05` delta with `base_version: 11` and
   `next_version: 12`.
3. CAS rejects the delta because its base is stale; no shard or head is
   changed.
4. The writer rereads head version `12`, rebases the delta, and retries with
   `base_version: 12` and `next_version: 13`.

## 3. Verification

- [x] 3.1 Exercise the ADDED scenarios in `specs/iron-pearl-ssot/spec.md`
- [x] 3.2 Confirm no `SKILL.md` edits and no Google Docs SSoT path

Verification is documentation-only. The change contains no credentials,
tokens, connection strings, or other secrets.

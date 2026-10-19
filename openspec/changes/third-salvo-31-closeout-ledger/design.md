# Design

## Record shape

The closeout ledger is a Markdown record with a stable identity block and
checklist sections. Blank values are intentional: this change creates the
closeout surface, while a later verifier may fill it with local evidence.

Required sections:

- identity and classification
- scope and fence confirmation
- evidence entries
- validation results
- disposition
- receipt

## Classification guard

The ledger repeats the immutable classification in its identity block and
acceptance checks:

```text
slot: T3-31
classification: INCLUDED / Ultra
on_demand: prohibited
```

This makes an accidental mode change visible during review. The ledger does
not define a second mode, fallback mode, or automatic activation path.

## Offline boundary

All fields can be completed from repository-local material. The skeleton
contains no instructions to call a service, retrieve a remote artifact, or
handle credentials.

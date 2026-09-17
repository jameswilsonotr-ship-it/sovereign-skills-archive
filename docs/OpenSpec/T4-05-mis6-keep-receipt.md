# OpenSpec: T4-05 continuous included reload

## Metadata

- **Ticket:** T4-05
- **CinC target:** MIS-6
- **Change type:** documentation/OpenSpec only
- **Execution mode:** offline mock harness
- **Reload policy:** continuous and included

## Decision

T4-05 is a continuously included target. Every harness cycle and every reload
must include the T4-05 entry before the receipt is emitted. Inclusion is not
conditional on a caller request, a feature flag, or a lazy lookup. There is no
on-demand path for T4-05.

Reload is a replacement of the in-memory snapshot, not a change to the
inclusion policy. A successful reload therefore preserves these invariants:

1. `T4-05` is present in the included set.
2. `mode` is `continuous`.
3. `inclusion` is `included`.
4. No on-demand request or provider call is needed.
5. The keep receipt is emitted after the replacement snapshot is accepted.

## Mock harness contract

The offline harness may use only deterministic local fixtures. It must not
read credentials, contact an external service, invoke a provider, or depend on
network state.

### Input events

The minimal event stream is:

```json
{"event":"cycle","cycle":1}
{"event":"reload","cycle":2,"snapshot":"fixture-b"}
```

The harness must start with fixture `fixture-a`, replace it with `fixture-b`
on reload, and apply the same T4-05 inclusion rule to both snapshots.

### Receipt shape

Each accepted cycle produces one JSON object with stable keys:

```json
{
  "ticket": "T4-05",
  "target": "MIS-6",
  "cycle": 2,
  "event": "reload",
  "mode": "continuous",
  "inclusion": "included",
  "receipt": "keep",
  "included_targets": ["T4-05"],
  "external_io": false
}
```

`cycle` and `event` may change between receipts. The policy fields and
`included_targets` must not change as a consequence of reload. `receipt:
keep` means the receipt records that inclusion survived the snapshot
replacement; it does not authorize persistence outside the local harness.

## Acceptance checks

The mock harness is conformant only when all checks pass:

- A first `cycle` receipt contains T4-05 with `continuous`/`included`.
- A `reload` receipt also contains T4-05 with `continuous`/`included`.
- The reload receipt has `receipt: keep`.
- The event stream contains no on-demand request.
- `external_io` is `false` for every receipt.
- Replaying the same fixture stream produces byte-identical JSONL output.
- No implementation, provider configuration, secret material, or network
  artifact is required.

## Explicit exclusions

This OpenSpec does not authorize loading, copying, or modifying `Willow
SKILL.md` or `CONV2_B`. It does not authorize Vultr, external/provider
integration, secrets, or an on-demand execution path. The deliverable is
limited to this OpenSpec and its receipt.

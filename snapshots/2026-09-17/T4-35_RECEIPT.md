# T4-35 receipt — included-burn tick

Status: specified  
UTC: 2026-09-17

## Contract

```yaml
ticket: T4-35
reload:
  mode: continuous
  availability: included
  on_demand: false
included_burn:
  progress_tick: "~10%"
  semantics: advance the included-burn progress indicator on each continuous tick
execution:
  network: offline-only
  external_services: forbidden
```

The included path is the only reload path. It remains active continuously; an
On-Demand fallback or trigger is not part of this contract. The progress value
is intentionally approximate (`~10%`) rather than a claim of exact billing
precision.

## Fences

- No skill-tree payload or runtime source was added; the base repository holds
  receipts and indexes only.
- No provider, credential, secret, or infrastructure configuration is
  introduced.
- No network, external service, or provider call is required to validate this
  receipt.

## Offline verification

- Confirmed the base branch contains no T4-35 implementation surface.
- Confirmed this change adds one receipt only.
- Confirmed the contract has no on-demand reload mode and declares offline-only
  execution.

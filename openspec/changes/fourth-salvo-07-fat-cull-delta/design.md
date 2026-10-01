# Design: `fourth-salvo-07-fat-cull-delta`

## Purpose

T4-07 narrows the earlier fat-cull candidate register with a durable
reject-list delta. A rejected item remains in the included snapshot unless a
later change proves a local source, a safe replacement, and a reviewable
retention boundary.

## Continuous included reload

The T4-07 record is part of the `INCLUDED` reload set on every cycle. Reload
replaces the local snapshot while preserving the reject list and its
classification:

```yaml
ticket: T4-07
reload: CONTINUOUS
lane: INCLUDED
on_demand: NEVER
offline_only: true
```

There is no request-time selector, lazy lookup, fallback lane, or On-Demand
conversion for this record. A reload that cannot preserve the local reject
list fails closed and reports the missing local input.

## Reject-list rules

| Reject class | Decision | Required evidence before any later reconsideration |
| --- | --- | --- |
| Willow `SKILL.md` or skill-tree live lock | Reject from cull | Explicit owner approval and a separate scoped change |
| `CONV2_B` | Reject from cull | Separate authorized review; not part of T4-07 |
| Unproven runtime/build input | Reject from cull | Local proof of replacement, regeneration, and retained source |
| External/provider/secret/Vultr material | Reject from cull | Separate approved scope; prohibited here |

The list records review boundaries, not file operations. No row authorizes
deletion, movement, archiving, regeneration, or tier reassignment.

## Offline verification

Verification is structural and textual only:

1. enumerate changed paths;
2. confirm every changed path is Markdown;
3. confirm the continuous/included/never-On-Demand fields;
4. confirm every reject class appears in the receipt; and
5. confirm no implementation or integration artifact was added.

No provider, network, credential, secret, hosted-compute, or runtime check is
needed for this documentation delta.

# PR triage receipt

## Requirements

### Requirement: identify the reserved change

Every receipt MUST identify the exact reserved change ID
`third-salvo-03-pr-triage-receipt`, salvo `THIRD_SALVO`, and slot `T3-03`.

### Requirement: enforce the execution lane

Every receipt MUST set `mode` to `Ultra`. `On-Demand` MUST NOT be used as a
mode, fallback, or implied execution path.

### Requirement: bound the review

Every receipt MUST name the S2-leftover source and state the review boundary.
Each reviewed leftover MUST have one disposition: `carry-forward`, `close`, or
`needs-owner`.

### Requirement: provide local evidence

Every disposition MUST include repository-local evidence or a concise reason.
The receipt MUST NOT depend on network calls, provider responses, secrets,
live Vultr state, or a newly minted Linear item.

### Requirement: remain non-mutating

The receipt MUST describe review outcomes only. It MUST NOT claim to have
executed a follow-up, changed a skill, or changed runtime behavior.

## Receipt template

Copy this block into a PR body and replace bracketed values. Keep the header
fields unchanged unless the receipt is for a different approved change.

```markdown
## PR triage receipt

- change_id: `third-salvo-03-pr-triage-receipt`
- salvo: `THIRD_SALVO`
- slot: `T3-03`
- mode: `Ultra`
- review_scope: S2 leftovers from [local source or fixture]
- reviewed_at_utc: [YYYY-MM-DDThh:mm:ssZ]

### Dispositions

| leftover_id | disposition | local evidence / reason | follow-up owner |
|---|---|---|---|
| [S2-01] | [carry-forward\|close\|needs-owner] | [path, section, or reason] | [owner or `none`] |

### Fence check

- [ ] Ultra-only review confirmed.
- [ ] No On-Demand path used or proposed.
- [ ] Offline/local evidence only.
- [ ] No provider, secret, live Vultr, or Linear-mint operation used.
- [ ] No Willow `SKILL.md` changed.
```

## Completed sample: S2 leftovers

```markdown
## PR triage receipt

- change_id: `third-salvo-03-pr-triage-receipt`
- salvo: `THIRD_SALVO`
- slot: `T3-03`
- mode: `Ultra`
- review_scope: S2 leftovers from `fixtures/s2-leftovers.sample.md`
- reviewed_at_utc: `2026-09-17T09:18:00Z`

### Dispositions

| leftover_id | disposition | local evidence / reason | follow-up owner |
|---|---|---|---|
| S2-01 | carry-forward | `fixtures/s2-leftovers.sample.md`, item S2-01 remains valid but is outside this atomic receipt change | none |
| S2-02 | close | `fixtures/s2-leftovers.sample.md`, item S2-02 is already represented by the local receipt contract | none |
| S2-03 | needs-owner | `fixtures/s2-leftovers.sample.md`, item S2-03 requires a human scope decision before any follow-up | unassigned |

### Fence check

- [x] Ultra-only review confirmed.
- [x] No On-Demand path used or proposed.
- [x] Offline/local evidence only.
- [x] No provider, secret, live Vultr, or Linear-mint operation used.
- [x] No Willow `SKILL.md` changed.
```

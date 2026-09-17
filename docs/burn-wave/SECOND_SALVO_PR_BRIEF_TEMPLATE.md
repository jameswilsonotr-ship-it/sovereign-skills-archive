# Second-Salvo PR Brief

Use this template for one atomic, included second-salvo change. Keep the brief
small enough that every claim can be tied to repository-local evidence.

## Change identity

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-<slot>-<short-name>` |
| Slot | `S2-__` |
| Base branch | `skill-tree-intake` |
| PR mode | Draft |
| Included surface | Ultra only |
| Owner | `<name or handle>` |

## One-line outcome

`<State the single observable outcome this PR delivers.>`

## Evidence ledger

List only evidence that exists in the checkout or is produced by a local,
offline command. Every row must support a claim in the brief.

| Claim | Evidence path or command | Observed result |
| --- | --- | --- |
| `<claim>` | `<repo-relative path>` or `` `<offline command>` `` | `<fact, count, or PASS/FAIL>` |
| `<claim>` | `<repo-relative path>` or `` `<offline command>` `` | `<fact, count, or PASS/FAIL>` |

Evidence rules:

- Use repository-relative paths and reproducible local commands.
- Prefer exact file names, line ranges, test names, and command results over
  narrative assertions.
- Do not use external URLs, live service responses, or unverifiable screenshots
  as the only support for a claim.
- Do not include credentials, tokens, private identifiers, or other secrets.

## Change and acceptance

### Included

- `<one atomic change in the Ultra surface>`
- `<second included item, only if required for the same outcome>`

### Acceptance checks

- [ ] `<observable behavior or artifact is present>`
- [ ] `<local validation command passes>`
- [ ] `<evidence ledger covers each acceptance claim>`

### Explicitly out of scope

- OD
- Willow `SKILL.md`
- `CONV2_B`
- Vultr and Cold Steel are separate surfaces; evidence for one must not be
  presented as evidence for the other.
- Every other S2 slot

## Hard-fence check

The author must complete every row before opening the PR.

| Fence | Check |
| --- | --- |
| Included surface | [ ] Included work is Ultra only; no OD is included |
| Willow | [ ] Willow `SKILL.md` is neither read as a deliverable nor changed |
| Conversation | [ ] `CONV2_B` is not included or modified |
| Infrastructure naming | [ ] Vultr is not labeled or treated as Cold Steel |
| Network | [ ] No external calls were made |
| Secrets | [ ] No secrets appear in the diff, evidence, logs, or receipt |
| Slot isolation | [ ] No other S2 slot was touched |

## PR body receipt

Paste this completed receipt into the PR body. The PR must remain a draft.

```text
Receipt
- change-id: second-salvo-<slot>-<short-name>
- slot: S2-__
- base: skill-tree-intake
- mode: draft
- included: Ultra only
- excluded: OD; Willow SKILL.md; CONV2_B; other S2 slots
- Vultr/Cold Steel: distinct; no equivalence asserted
- external calls: none
- secrets: none
- files changed:
  - <repo-relative path>
- validation:
  - <offline command> — PASS
- evidence:
  - <repo-relative path or command result>
- result: ready for review as a draft
```

Before submitting, replace every placeholder, verify the receipt against the
final diff, and keep the PR to this one atomic slot.

# Second salvo intake receipt

- **OpenSpec change-id:** `second-salvo-01-intake-receipt`
- **Slot:** `S2-01`
- **Operation:** atomic included burn
- **Evidence boundary:** repository and Git history only

## Source and base refs

This receipt branch was created from the fetched `skill-tree-intake` ref:

| Ref | Commit |
| --- | --- |
| Base branch at branch point: `skill-tree-intake` / `origin/skill-tree-intake` | `cf7afbe782b7cc790aa3683c8d4268aa4ed29ba4` |
| Receipt source branch | `cursor/second-salvo-01-intake-receipt-48b9` |

The local repository does not retain the original PR source-branch names. For
the historical PRs below, the Git commit is the source ref retained in the
`skill-tree-intake` ancestry, and its direct parent is the corresponding base
ref.

## First-wave landing

- **Initial skill-tree landing commit:** `640a2ca84c448d2a727465c1e1240175c504f643`
  (`feat: unpack 2026-09-16 full skill tree for Cursor (MIS-5)`).
  Its direct parent is `412e06a7b41e8c09fc14040fa0075eacdbd2fb5e`.
- **BURN HARD wave landing commit:** `a17e0db53b925b86c0c4e1b172629a2400af1632`
  (`feat: ingest offline BURN HARD corpora (#27)`).
  Its direct parent is `7087c2abc765dcf3cb8abe55e3cad56d574dff04`.
- The landing commits are reachable from `skill-tree-intake`; the current
  fetched tip is `cf7afbe782b7cc790aa3683c8d4268aa4ed29ba4`.

## Merged PRs evidenced by Git

Git records the following PR identifiers in commit subjects. Their commits are
reachable from `skill-tree-intake`, so this receipt records them as the merged
first-wave sequence. The source/base columns intentionally use immutable Git
commit refs rather than asserting source branch names that are not present in
the local repository.

| PR | Subject recorded in Git | Source ref (landed commit) | Base ref (direct parent) |
| --- | --- | --- | --- |
| `#29` | `docs: add Gemini Spark and Vesper bridge bind stubs` | `e5a8304e78dcebd09cd6f93b085d5dea035ab2b2` | `640a2ca84c448d2a727465c1e1240175c504f643` |
| `#31` | `docs: add cheapest Vultr Letta/Ollama provisioning runbook` | `d86e82482cc93819310d0dbcb67021996067caf8` | `e5a8304e78dcebd09cd6f93b085d5dea035ab2b2` |
| `#30` | `feat: generate OpenSpec CSV and Markdown matrices` | `7087c2abc765dcf3cb8abe55e3cad56d574dff04` | `d86e82482cc93819310d0dbcb67021996067caf8` |
| `#27` | `feat: ingest offline BURN HARD corpora` | `a17e0db53b925b86c0c4e1b172629a2400af1632` | `7087c2abc765dcf3cb8abe55e3cad56d574dff04` |

## Included-burn fences

- Included scope is **Ultra only**; **OD is excluded**.
- No Willow `SKILL.md` is changed by this receipt.
- `CONV2_B` is excluded.
- Vultr is not Cold Steel.
- This receipt records no provider, phone, Linear, or other external call.
- No secrets are included.
- This slot owns only `docs/burn-wave/SECOND_SALVO_INTAKE_RECEIPT.md`; other
  S2 slot paths are out of scope.

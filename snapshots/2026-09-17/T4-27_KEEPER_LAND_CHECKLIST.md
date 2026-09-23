# T4-27 keeper land-path checklist

## Contract

- [x] Reload policy is `CONTINUOUS_INCLUDED`.
- [x] The included surface is loaded continuously; it is not selected by a
      request-time or user-invoked on-demand path.
- [x] Any state that can produce an on-demand load is rejected before landing.
- [x] The work remains offline-only and uses local files, fixtures, and git
      inspection only.

## Keeper land path

- [x] Work is isolated to the T4-27 branch.
- [x] The landing unit is this checklist and its receipt only.
- [x] No tarball is unpacked, copied, or rewritten.
- [x] No `skill_tree/`, source snapshot, or unrelated daily receipt is changed.
- [x] No generated documentation tree, document factory, or split handoff is
      introduced.
- [x] The included reload keeps one stable source of truth; it does not create
      parallel copies or per-request documents.

## Fences

- [x] No Willow skill file is added or imported.
- [x] No conversation-B artifact is added or imported.
- [x] No external service, provider integration, credential, secret, or Vultr
      material is added or referenced.
- [x] The on-demand path is absent from the landable surface.

## Offline verification

- [x] `git diff --check` passes.
- [x] `git diff --name-only` contains only the two T4-27 landing files.
- [x] A local content review confirms the contract and every fence above.
- [x] The commit is pushed once and represented by one pull request.
- [x] The receipt records the final commit, branch, pull request, and checks.

## Exit condition

T4-27 is a keeper only when every checkbox is checked. If any contract or
fence fails, do not land the change; return it to the local worktree for
correction.

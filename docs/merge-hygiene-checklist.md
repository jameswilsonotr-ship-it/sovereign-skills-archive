# Merge hygiene checklist

Use this checklist before merging a change to
`sovereign-skills-archive` through the `INCLUDED` land path.

## 1. Identify the change

- [ ] The change has one stated purpose and one reserved change ID.
- [ ] The change ID is
      `third-salvo-02-merge-hygiene-checklist` for the T3-02 change.
- [ ] The PR title is exactly `salvo: T3-02 merge-hygiene-checklist`.
- [ ] The PR contains one reviewable receipt covering this atomic change.

## 2. Confirm the land path

- [ ] The requested land path is `INCLUDED`.
- [ ] The review does not route, publish, or hand off this change as
      `On-Demand`.
- [ ] The final diff is limited to the agreed `INCLUDED` deliverables.

## 3. Inspect the diff

- [ ] The working tree starts from the intended base branch.
- [ ] The diff contains only the OpenSpec change and its checklist
      documentation.
- [ ] No skill payload is added, removed, or rewritten.
- [ ] No `SKILL.md` file is modified.
- [ ] No generated archive, binary payload, or unrelated snapshot is included.
- [ ] The diff does not contain secrets, credentials, or environment-specific
      values.

## 4. Validate offline

- [ ] Repository status and the final diff have been reviewed locally.
- [ ] Markdown paths and internal references resolve within the repository.
- [ ] Any checks run for the change use local files and fixtures only.
- [ ] No external network, provider, live infrastructure, or issue-tracker
      call is needed to approve the change.
- [ ] A failed or unavailable external service is not treated as a validation
      requirement.

## 5. Record the receipt

The PR body should include one concise receipt with:

- the exact change ID;
- the exact PR title;
- the `INCLUDED` land-path result;
- the files changed;
- the offline validation command(s) and result; and
- an explicit statement that no skill payload was modified.

## Merge decision

Merge only when every applicable checkbox is checked and the receipt is
reviewable from the PR body. If the land path changes from `INCLUDED`, stop
and return the change for re-scoping; this checklist does not authorize an
`On-Demand` landing.

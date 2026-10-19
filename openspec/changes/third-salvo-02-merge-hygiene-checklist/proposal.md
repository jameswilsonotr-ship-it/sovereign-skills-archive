# Change: T3-02 merge-hygiene checklist

- **Change ID:** `third-salvo-02-merge-hygiene-checklist`
- **Slot:** `T3-02`
- **Land path:** `INCLUDED` only
- **Status:** proposed

## Intent

Add a small, offline checklist for reviewing merge hygiene before an
`INCLUDED`-only change lands in `sovereign-skills-archive`. The checklist
provides one repeatable review path for scope, diff, validation, and receipt
checks without changing any skill payload.

## Scope

This change includes:

- the merge-hygiene checklist at
  `docs/merge-hygiene-checklist.md`;
- this OpenSpec proposal; and
- a task list recording the acceptance checks for the change.

The checklist applies only to the `INCLUDED` land path. `On-Demand` is never a
permitted land path for this change.

## Non-goals

- No `SKILL.md` files are edited.
- No skill payload is added, removed, or rewritten.
- No provider, network, secret, live infrastructure, or issue-tracker
  interaction is required.
- No alternate delivery path is defined.

## Acceptance criteria

1. The reserved change ID is used exactly as the OpenSpec directory name.
2. The checklist states the `INCLUDED`-only boundary and rejects `On-Demand`.
3. The checklist verifies a docs/OpenSpec-only diff and a clean, offline
   validation run.
4. The change contains no skill-payload edits.
5. The PR body contains one reviewable receipt for this atomic change.

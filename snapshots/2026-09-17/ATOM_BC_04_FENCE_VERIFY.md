# atom-bc-04 fence verification

**Parent change-id:** `add-included-burn-chew-lanes`  
**Atom:** `atom-bc-04-fence-verify`  
**Tag:** Meter Burn Desk

## Purpose

This note is the verification checklist for the ADDED burn-chew scenarios under
the parent change. It is OpenSpec-basic documentation only. It does not claim
that a missing local `uploads/` fixture or an external runner was executed.

The atom is intentionally limited to fence verification. It does not bundle
`atom-bc-01`, `atom-bc-02`, or `atom-bc-03`, and it does not acquire a
skill-tree lock.

## Hard-fence checklist

Review each item against the complete diff and the changed-path list:

- [ ] **SKILL.md untouched:** no `SKILL.md` file is created, edited, renamed,
      deleted, or generated.
- [ ] **No skill-tree lock:** the atom does not acquire, hold, or alter a
      skill-tree lock.
- [ ] **No OD:** no OD workflow, artifact, or side effect is introduced.
- [ ] **No CONV2_B:** no CONV2_B workflow, artifact, or side effect is
      introduced.
- [ ] **No CMV:** no CMV workflow, artifact, or side effect is introduced.
- [ ] **OpenSpec basic only:** no provider-specific integration, minting,
      external document operation, or non-basic OpenSpec behavior is required.
- [ ] **No Google Docs:** no Google Docs is read, created, linked as an input,
      or used as evidence.
- [ ] **No plating/avatar mint:** no plating action or avatar mint is
      requested, simulated, or recorded.
- [ ] **No vibe:** no vibe step, output, or implicit fallback is included.

The named fence terms above are labels for negative checks. A checker must
inspect paths, operations, and side effects rather than fail on the presence of
these labels in this checklist.

## ADDED burn-chew scenario coverage

Each scenario is independently reviewable and must pass without widening the
atom's scope.

### BC-04-01 — Included-only

**Setup:** Provide an input containing an `Included` lane plus unrelated
material outside that lane.

**Exercise:** Run only the basic OpenSpec verification for the Included lane.

**Pass criteria:**

- Only Included content is considered in scope.
- Excluded or unrelated material produces no edits, generated artifacts, or
  side effects.
- No Google Docs, OD, CONV2_B, CMV, plating/avatar mint, or vibe operation is
  used to complete the check.

**Evidence:** Record the input identifier, the selected Included boundary, and
the changed-path list. Do not paste source documents into this repository.

### BC-04-02 — One change-id per agent

**Setup:** Assign one agent the exact change-id
`add-included-burn-chew-lanes`; make neighboring atom IDs available as
negative controls.

**Exercise:** Verify the agent assignment and the resulting change scope.

**Pass criteria:**

- The agent has exactly one active change-id:
  `add-included-burn-chew-lanes`.
- The result contains this atom only:
  `atom-bc-04-fence-verify`.
- `atom-bc-01`, `atom-bc-02`, and `atom-bc-03` are not bundled, edited, or
  represented as completed work.
- A second change-id or a neighboring atom causes the check to fail closed
  rather than being silently accepted.

**Evidence:** Record the single change-id, atom ID, and final changed-path
list.

### BC-04-03 — SKILL.md untouched

**Setup:** Run the verification from a clean worktree with the skill-tree
available only as an out-of-scope boundary.

**Exercise:** Compare the pre-run and post-run changed-path lists and inspect
the diff for skill-tree lock or `SKILL.md` activity.

**Pass criteria:**

- No `SKILL.md` path appears in the diff, staged set, or generated output.
- No skill-tree lock is acquired or changed.
- The only intended deliverable is this atom's verification note.
- Any attempted `SKILL.md` mutation or lock operation fails the atom, even if
  the rest of the scenario succeeds.

**Evidence:** Attach the path-only diff and lock-operation result to the
review; do not include `SKILL.md` contents.

## Review closeout

Before approval, the reviewer should confirm:

1. The changed-path list contains only this atom's note.
2. All three ADDED scenarios above have explicit evidence or are marked
   **not run** with the reason recorded.
3. The hard-fence checklist is complete.
4. The PR title and description mention both `atom-bc-04` and
   `add-included-burn-chew-lanes`, and carry the **Meter Burn Desk** tag.

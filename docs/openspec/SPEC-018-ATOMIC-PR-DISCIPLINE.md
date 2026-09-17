# SPEC-018: Atomic PR Discipline

Status: **draft**

## 1. Purpose

This specification defines how a change is split, named, reviewed, and
delivered when the work is intentionally atomic. Its goal is to make every
pull request independently understandable, reviewable, revertible, and
traceable to one declared change.

This is a process contract. It does not prescribe a programming language,
repository layout, CI vendor, or merge strategy.

## 2. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**,
and **MAY** are to be interpreted as requirements.

## 3. Core invariant

An atomic PR has exactly one change ID.

For this specification, an atomic PR:

1. declares one change ID in its title and description;
2. delivers one independently reviewable outcome;
3. contains only the files and edits required for that outcome;
4. has one acceptance condition that can be evaluated without guessing at
   unrelated work; and
5. can be reverted without silently reverting a different change.

A dependency between PRs does not permit combining their change IDs. If work
requires a sequence of PRs, each PR MUST keep its own ID and document the
dependency.

## 4. Change IDs

The change ID is immutable once a PR is opened. This specification reserves
the `AP-###` namespace for Atomic PR requirements:

```text
AP-001 through AP-012
```

Each `AP-###` identifier MUST be claimed by at most one open PR at a time.
The identifier MUST appear in:

- the PR title;
- the first section of the PR description; and
- the commit message or other repository-approved change record.

An identifier is not a label for a theme or an area of ownership. It names one
specific, bounded change. A PR that implements two AP requirements is not
atomic and MUST be split.

## 5. The included-burn rule

All work included in an atomic PR consumes the scope of that PR's one change
ID, whether or not the work was described as incidental. In particular:

- cleanup discovered during implementation is a separate change unless it is
  strictly necessary for the declared outcome;
- formatting-only edits outside the touched surface are not “free”;
- opportunistic dependency upgrades, renames, and refactors are not included
  by implication; and
- a related follow-up MUST be recorded as a separate change ID or explicitly
  deferred.

The reviewer evaluates the complete diff, not only the PR summary. Hidden
scope is still scope.

## 6. AP-001..AP-012 requirements

The following requirements define the atomic PR contract. Each row is a
separate acceptance unit and is intended to be delivered by a separate PR
unless a later governing policy explicitly assigns a different unit.

| ID | Requirement | Minimum evidence |
| --- | --- | --- |
| **AP-001** | Declare one stable change ID before implementation begins. | The ID is present in the PR title, description, and change record. |
| **AP-002** | State one outcome in observable terms. | The description has one “done when” statement with an objective result. |
| **AP-003** | Bound the file and subsystem scope. | The description lists the expected paths or surface and explains any necessary exception. |
| **AP-004** | Keep one change ID per PR. | The PR and its commits contain no second AP ID or unrelated issue-sized outcome. |
| **AP-005** | Keep the diff minimal and causal. | Every changed line can be tied to the declared outcome, with unrelated edits removed or split. |
| **AP-006** | Separate prerequisite and dependent work. | Dependencies are linked and ordered; prerequisite work is not smuggled into the dependent PR. |
| **AP-007** | Make acceptance independently testable. | The PR names the check, artifact, or review observation that proves completion. |
| **AP-008** | Preserve traceability across commits. | Commits retain the same change ID and do not mix unrelated work. |
| **AP-009** | Make rollback boundaries explicit. | The description states what reverting the PR removes and what it leaves intact. |
| **AP-010** | Treat review findings as scoped changes. | Fixes required for the declared outcome stay in the PR; unrelated suggestions become follow-ups. |
| **AP-011** | Record exceptions instead of silently widening scope. | Any exception names the reason, affected files, reviewer, and follow-up ID if needed. |
| **AP-012** | Close the loop after merge or abandonment. | The change record marks the ID as merged, superseded, or abandoned and prevents accidental reuse. |

The AP table is a contract, not a checklist for bundling all twelve
requirements into one PR. A compliant rollout uses one PR per claimed AP ID.

## 7. Required PR shape

### 7.1 Title

The title MUST use the repository's normal title conventions and include the
change ID. A conforming shape is:

```text
docs: AP-001 declare the atomic PR change ID
```

The title SHOULD describe the single outcome rather than repeat the generic
name of this specification.

### 7.2 Description

The PR description MUST contain, in this order:

```markdown
Change ID: AP-###

Outcome:
<!-- one observable result -->

Scope:
<!-- files, subsystem, or bounded surface -->

Acceptance:
<!-- one objective check or review observation -->

Dependencies:
<!-- none, or links to prerequisite/dependent PRs -->

Rollback:
<!-- effect of reverting this PR -->
```

If a field does not apply, it MUST say `None`, not remain ambiguous.

### 7.3 Commits

Every commit in an atomic PR MUST support the same declared outcome. Commit
messages SHOULD include the change ID, for example:

```text
docs: AP-007 define independent acceptance evidence
```

Fixup commits are allowed while review is in progress, subject to the
repository's normal merge policy. Squashing or rebasing MUST NOT be used to
hide a second outcome.

## 8. Author workflow

Before opening the PR, the author MUST:

1. choose an unclaimed change ID;
2. write the one-sentence outcome;
3. identify the bounded scope and acceptance evidence;
4. check for prerequisites and record them;
5. make the smallest viable change;
6. inspect the complete diff for unrelated work; and
7. confirm that reverting the PR has a clear boundary.

If implementation reveals a second outcome, the author MUST stop widening the
PR. The second outcome is deferred, split into another PR, or explicitly
approved as an exception under AP-011.

## 9. Reviewer workflow

The reviewer MUST evaluate the PR in this order:

1. Is exactly one change ID declared and unclaimed elsewhere?
2. Is the outcome observable and bounded?
3. Does every changed file support that outcome?
4. Are dependencies and acceptance evidence clear?
5. Is the rollback boundary safe and understandable?
6. Does the diff contain included burn from cleanup, upgrades, or unrelated
   fixes?

The reviewer SHOULD request a split before reviewing detailed implementation
when the PR fails the atomicity test. Approval of code quality does not waive
the one-change-ID requirement.

## 10. Split and exception rules

### 10.1 Split rule

Split a PR when any of the following is true:

- it has two independently useful outcomes;
- one part could be reverted without reverting the other;
- different reviewers or owners are required for different parts;
- the acceptance evidence has more than one unrelated pass/fail result; or
- the diff includes “while I was here” work.

The split PRs MUST use distinct IDs and MUST link to the original discussion.

### 10.2 Necessary mechanical edits

A mechanical edit MAY remain in the PR only when it is required for the
declared outcome and cannot be separated without leaving an invalid or
unreviewable result. The description MUST identify the edit and explain why it
is necessary.

### 10.3 Exception rule

Exceptions are narrow and MUST be explicit. An exception record MUST include:

- the single outcome that remains authoritative;
- the additional files or edits;
- why separation is technically unsafe or impossible;
- the approving reviewer; and
- a follow-up change ID when the extra work is not part of the outcome.

Convenience, deadline pressure, or a desire to reduce PR count is not
sufficient justification.

## 11. Completion states

An AP change ID has exactly one terminal state:

- **merged** — the PR landed and its acceptance evidence passed;
- **superseded** — another PR replaced it before merge, with a link to the
  replacement; or
- **abandoned** — the PR was closed without delivery, with a reason.

An ID in a terminal state MUST NOT be silently reused for a different outcome.
If the same outcome is retried after abandonment, the record MUST link to the
old attempt and use the repository's approved retry convention.

## 12. Conformance checklist

An atomic PR conforms to SPEC-018 only when all applicable answers are yes:

- [ ] One `AP-###` change ID is declared.
- [ ] The ID is unique among open PRs.
- [ ] The title, description, and commit record agree.
- [ ] The outcome is one observable result.
- [ ] The scope is bounded.
- [ ] Every changed line supports the outcome.
- [ ] Dependencies are explicit.
- [ ] Acceptance evidence is independently checkable.
- [ ] Rollback behavior is stated.
- [ ] Included burn has been removed or explicitly excepted.
- [ ] The terminal state will be recorded.

## 13. Non-goals

SPEC-018 does not:

- require one file per PR;
- prohibit a dependency chain;
- replace code review, testing, security review, or release approval;
- require every commit to be independently mergeable; or
- authorize merging a PR that fails repository-specific policy.

Atomicity is a boundary discipline. It is not a substitute for technical
correctness or operational approval.

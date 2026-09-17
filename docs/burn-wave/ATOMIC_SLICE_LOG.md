# ATOMIC Slice Log

This log defines the working contract for an **ATOMIC OpenSpec MONKEY** slice:
one small, reviewable unit of work with explicit ownership and executable
verification.

## Roles

| Role | Owns | Must produce | Must not do |
| --- | --- | --- | --- |
| **Architect** | The slice boundary, intent, constraints, and acceptance criteria | A short OpenSpec proposal/design and a clear definition of done | Quietly expand the slice or implement around unresolved requirements |
| **Engineer** | The implementation of the agreed slice | The smallest coherent code or documentation change, plus focused tests/checks | Change the contract without recording the decision |
| **Monkey** | Adversarial verification of the result | Reproducible checks, failure evidence, and a pass/fail recommendation | Approve based on inspection alone or “fix” unrelated scope |

### Handoff order

1. **Architect** writes the slice intent and acceptance criteria.
2. **Engineer** implements only that slice and records the changed paths.
3. **Monkey** runs the acceptance checks, probes likely failure modes, and
   records evidence here.
4. The slice is complete only when the acceptance criteria and monkey checks
   both pass, or an explicit follow-up is recorded.

## Naming convention

Use names that are stable, searchable, and free of personal or secret data.

### Slice identifiers

```text
ATOMIC-<YYYYMMDD>-<NNN>
```

- `ATOMIC` is the fixed program prefix.
- The date is the UTC date the slice is opened.
- `<NNN>` is a zero-padded sequence for that date (`001`, `002`, ...).

### OpenSpec change directories

```text
openspec/changes/<atomic-id-lowercase>-<short-kebab-summary>/
```

Use lowercase kebab-case for the summary. Keep it action-oriented and
specific, for example:

```text
openspec/changes/atomic-20260917-001-add-slice-log/
```

Use the conventional OpenSpec artifact names inside the change directory:
`proposal.md`, `design.md`, and `tasks.md` as applicable.

### Log entries and role labels

Use the fixed role labels `architect`, `engineer`, and `monkey`. Record people
or agent handles only when they are already public and necessary for
traceability; never record credentials, tokens, API keys, private URLs, or
other secrets.

Append entries with this shape:

```markdown
### ATOMIC-YYYYMMDD-NNN — short-kebab-summary

- Architect: architect
- Engineer: engineer
- Monkey: monkey
- OpenSpec: `openspec/changes/atomic-yyyymmdd-nnn-short-kebab-summary/`
- Status: proposed | in progress | verified | follow-up
- Acceptance criteria:
  - [ ] ...
- Changed paths:
  - `path/to/file`
- Monkey evidence:
  - Command/check: `...`
  - Result: pass | fail
- Follow-up: none, or a linked slice identifier
```

Keep one slice atomic: if the acceptance criteria require separate
implementations or separate verification plans, split the work into multiple
slice identifiers.

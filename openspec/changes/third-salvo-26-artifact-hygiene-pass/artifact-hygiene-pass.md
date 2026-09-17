# T3-26 artifact hygiene pass list

**Change ID:** `third-salvo-26-artifact-hygiene-pass`
**Slot:** `T3-26`
**Eligibility:** `INCLUDED Ultra ONLY`
**Execution mode:** offline, repository-local

This is the authoritative pass list for the change. It does not authorize
payload import, unpacking, rewriting, or publication.

| ID | Check | Evidence | Outcome |
|---|---|---|---|
| AH-01 | Scope is limited to the T3-26 Ultra inclusion set. | `proposal.md`, `specs/artifact-hygiene/spec.md` | `PASS` |
| AH-02 | On-Demand material is excluded from the pass. | Explicit exclusion in `proposal.md` and `spec.md` | `PASS` |
| AH-03 | New paths are stable, lowercase, and free of generated suffixes. | `git diff --name-status` and path review | `PASS` |
| AH-04 | New Markdown files are non-empty and end with a newline. | Local file inspection | `PASS` |
| AH-05 | Patch whitespace is clean. | `git diff --check` | `PASS` |
| AH-06 | References stay within this change directory or the repository. | Link and path review | `PASS` |
| AH-07 | No payload artifact is imported, unpacked, or rewritten. | `git diff --stat` and file inventory | `PASS` |
| AH-08 | No temporary, editor, or build output is added. | `git status --short` and file inventory | `PASS` |
| AH-09 | A payload-specific checksum comparison is available locally. | No T3-26 Ultra payload is present in this checkout | `N/A` — reason recorded |
| AH-10 | The result is reproducible without network access. | All commands listed in `RECEIPT.md` are local Git or file checks | `PASS` |

## Review rule

Only Ultra entries assigned to T3-26 may be added to this list. On-Demand
entries remain excluded even if they are present in a later inventory.

# S2-27 acceptance cases

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-27-acceptance-cases` |
| Slot | `S2-27` |
| Included lane | Ultra only |
| Source change-id | `cli-export` |
| Source status | `accepted` |
| Source document | `docs/openspec/cli-export.md` |

These cases verify the already-scoped `cli-export` change from the repository's
first-wave OpenSpec set. They define observable behavior only; this slice does
not implement or broaden the CLI.

## Acceptance cases

### S2-27-AC-001 — default CSV goes to stdout

**Given** a valid local project fixture and no output-path argument  
**When** the export command runs without `--force`  
**Then** it exits successfully, writes valid CSV to stdout, and does not
silently redirect the export to a file.

**Evidence:** Parse stdout with a local CSV reader and verify the expected
header and fixture rows.

### S2-27-AC-002 — explicit output path is supported

**Given** a valid local project fixture and a writable, non-existing output path  
**When** the export command runs with that path  
**Then** it exits successfully and writes valid CSV at exactly that path.

**Evidence:** Read the created file with a local CSV reader and compare its
records with the deterministic fixture.

### S2-27-AC-003 — replacement is blocked without `--force`

**Given** an existing output file containing a sentinel payload  
**When** the export command runs with that path and without `--force`  
**Then** it fails clearly and the sentinel payload remains byte-for-byte
unchanged.

**Evidence:** Capture the exit status and compare the file bytes before and
after the command.

### S2-27-AC-004 — `--force` permits replacement

**Given** an existing output file containing a sentinel payload  
**When** the export command runs with that path and `--force`  
**Then** it exits successfully and replaces the sentinel with valid CSV for the
deterministic fixture.

**Evidence:** Parse the post-run file locally and verify that the sentinel is
gone and the expected records are present.

### S2-27-AC-005 — the safety gate is independent of output mode

**Given** an existing output path  
**When** the export command is invoked once without `--force` and once with
`--force`  
**Then** the first invocation preserves the existing file, while the second
may replace it; stdout-versus-file selection must not bypass the replacement
guard.

**Evidence:** Run both invocations against an isolated temporary directory and
record exit statuses plus file hashes using local tooling.

## Verification boundary and fences

- The included lane is **Ultra only**; OD is out of scope.
- No `Willow SKILL.md`, `CONV2_B`, or unrelated S2 slot is part of this slice.
- Vultr and Cold Steel are distinct identities; this document does not equate
  them or add environment-specific behavior.
- Verification is local and offline: no external calls, credentials, tokens,
  or secret values are required.
- The only intended changed path for this slice is
  `docs/burn-wave/ACCEPTANCE_CASES.md`.


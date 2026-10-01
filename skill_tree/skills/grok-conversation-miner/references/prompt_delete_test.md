---
name: prompt_delete_test
version: 1.0.0
owner: grok-conversation-miner
created: 2026-07-24
status: live
purpose: Controlled test of programmatic write/delete boundaries in the current environment.
---

# Programmatic Deletion Test Protocol

**Trigger phrases**:
- “delete skills programmatically”
- “test deletion limits”
- “run delete test”

## Goal

Safely probe what the current runtime can and cannot delete (local skill files, temporary artifacts, Drive files via the connected tools, etc.). Produce a clear report of boundaries. This is a diagnostic tool, not a general-purpose deletion utility.

## Execution Steps

### 1. Declare scope
Explicitly state what will be tested in this run (e.g. “temporary files under /home/workdir/artifacts/mining_packages only” or “a disposable test file on Drive”).

### 2. Create a disposable test artifact
- Write a small, clearly named test file (e.g. `DELETE_TEST_YYYYMMDD.txt`) in a safe location.
- Optionally upload a copy to a test folder on Drive so both local and remote deletion paths can be exercised.

### 3. Attempt deletion
- Local: use `rm` or equivalent on the test file and report success/failure.
- Drive: use the connected `google_drive_trash_file` (or equivalent) on the test file and report the result.
- Never target real skill folders, mirrors, or production packages without an additional explicit confirmation phrase from the user.

### 4. Report boundaries
Produce a short table or list:
- What succeeded
- What failed and why (permissions, tool limitations, safety gates, etc.)
- Any observed side-effects

### 5. Clean up
If the test files still exist, remove or trash them so the environment is left clean.

## Hard Safety Rules

- Default to **trash** (recoverable) rather than permanent delete on Drive.
- Never run this protocol against the live `chaos-bratz-roster`, mirrors, or any folder that contains production agent state unless the user supplies an exact confirmation phrase such as “CONFIRM DELETE TEST ON PRODUCTION PATH”.
- Log every action taken.

## Output Expectations

- Clear success/failure report
- Confirmation that test artifacts have been cleaned up
- No changes to real skills unless explicitly confirmed

**End of prompt_delete_test.md**

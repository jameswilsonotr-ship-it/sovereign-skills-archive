# Cursor Included Burn

Status: operator runbook / included allowance only  
Mode: atomic execution  
Policy: **No OD. No implicit expansion. No carry-over.**

## 0. Purpose

Use this runbook when a bounded task must consume only an already-included
Cursor allowance. An included burn is one small, independently reviewable unit
of work with a known stopping point. It is not permission to continue until the
request “feels complete.”

This runbook governs the work boundary, not a billing promise. The current
account, plan, quota, and usage view are the source of truth. If inclusion
cannot be verified before execution, do not start the burn.

## 1. Non-negotiable rules

1. **Included-only:** Every action in the burn must fit the allowance confirmed
   at intake.
2. **No OD:** Do not switch to, authorize, or silently trigger OD. Treat an
   unavailable balance, an unclear meter, a quota warning, or an ambiguous
   plan state as a stop condition.
3. **Atomicity:** One burn has one objective, one owner, one bounded input set,
   and one terminal outcome.
4. **No scope creep:** New files, integrations, research branches, retries,
   follow-up work, or “while you are here” requests require a new intake.
5. **No hidden side effects:** Do not send messages, publish artifacts, change
   access, or create billable resources unless that side effect is explicitly
   included in the intake.
6. **Stop beats completion:** A fence violation, usage uncertainty, or
   authorization gap ends the burn. Preserve the partial result and report the
   stop reason.

## 2. Roles

The names below are operating roles, not separate permissions. One person may
hold more than one role only when that assignment is written into the intake.

| Role | Owns | Must not do |
| --- | --- | --- |
| **Ada** | Executes the single approved unit; checks the fences before each material action; stops on the first violation | Expand scope, approve OD, or infer missing authorization |
| **Liaison** | Confirms the requester, objective, input boundary, destination, and handoff; resolves ambiguity before start | Convert a suggestion into approval or promise work outside the burn |
| **Mag** | Records the allowance check, burn identifier, actions, stop/completion state, and evidence needed for audit | Edit the ledger to make usage fit or certify an unverified meter |

The Liaison is the approval boundary. Ada is the execution boundary. Mag is the
measurement and evidence boundary. None of the three may waive the no-OD rule.

## 3. Fences

Every burn passes all three fences in order. A failed fence means **STOP**.

### 3.1 Intake fence

Before any execution, record:

- burn ID and UTC start time;
- requester and Liaison;
- Ada and Mag;
- one-sentence objective and the exact deliverable;
- included allowance or approved budget reference;
- input files, repositories, tools, and destinations in scope;
- explicit exclusions, including OD and unapproved external side effects;
- stop condition and handoff destination.

Reject the intake when the objective is open-ended, the allowance is not
visible, the owner is unclear, or the requested result depends on work outside
the listed inputs.

### 3.2 Execution fence

Ada may perform only the listed unit:

- use only the approved inputs and tools;
- make the smallest reversible change that satisfies the objective;
- do not add dependencies, services, accounts, integrations, or destinations;
- do not retry a failed or timed-out action without recording the retry and
  confirming that it remains inside the included allowance;
- stop before the next action when the allowance, quota, or scope becomes
  uncertain.

An action that would cross the included boundary is not “small enough” because
it is technically convenient. It is outside the burn.

### 3.3 Output fence

Before handoff, Ada and Mag verify:

- the stated deliverable exists or the run is explicitly marked stopped;
- no unapproved output, message, commit, upload, or other side effect was
  created;
- the result is labeled `completed`, `stopped`, or `blocked`;
- the final usage/allowance observation and UTC end time are recorded;
- partial work is clearly separated from a finished deliverable;
- any follow-up is written as a new intake, never appended to the current burn.

## 4. Procedure

### 4.1 Open

1. Liaison writes the intake record using the template below.
2. Mag checks the current included allowance and records the evidence source
   and observation time.
3. Ada reads the objective, boundaries, exclusions, and stop condition.
4. The three roles confirm `READY` only when all intake fields are complete.

If any role cannot confirm the boundary, mark the burn `BLOCKED` and do not
begin execution.

### 4.2 Execute

1. Ada performs one atomic unit of work.
2. Mag records material actions and any meter or quota change visible during
   the burn.
3. Ada pauses before any action that is not directly required by the
   objective.
4. Liaison resolves only pre-existing intake ambiguity. A new request opens a
   new burn.

### 4.3 Close

1. Ada states the result and stops making changes.
2. Mag records the final observed state and evidence.
3. Liaison confirms the handoff destination or records that no handoff is
   authorized.
4. Mark exactly one terminal state:

   - `COMPLETED` — objective met within the included boundary;
   - `STOPPED` — execution ended at a fence or safety stop;
   - `BLOCKED` — execution did not start because intake or allowance evidence
     was insufficient.

Do not mark a partially completed or uncertain result `COMPLETED`.

## 5. Hard stops

Stop immediately and preserve the record if:

- the account shows OD, overage, or an equivalent out-of-bound mode;
- the included balance or quota cannot be verified;
- the meter changes unexpectedly or cannot be attributed to the burn;
- the task requires a second objective, unlisted input, or new destination;
- a tool requests broader access than the intake authorizes;
- an action would publish, message, upload, purchase, or grant access without
  explicit intake approval;
- the output cannot be separated from unrelated work;
- any role asks Ada to “just finish” after the boundary is reached.

A hard stop is a successful safety outcome, not an execution failure.

## 6. Intake and closeout template

Copy this block into the approved operations record. Do not put secrets,
tokens, private keys, or sensitive customer data in the record.

```text
BURN ID:
STATUS: BLOCKED | READY | IN PROGRESS | COMPLETED | STOPPED
START UTC:
END UTC:

REQUESTER:
LIAISON:
ADA:
MAG:

OBJECTIVE:
DELIVERABLE:
IN-SCOPE INPUTS:
IN-SCOPE TOOLS:
AUTHORIZED DESTINATION:
EXPLICIT EXCLUSIONS:
STOP CONDITION:

INCLUDED ALLOWANCE / REFERENCE:
ALLOWANCE EVIDENCE SOURCE:
ALLOWANCE OBSERVED UTC:
OD CHECK: CONFIRMED ABSENT

MATERIAL ACTIONS:
USAGE / METER OBSERVATIONS:
OUTPUT / HANDOFF:
PARTIAL WORK OR FOLLOW-UP (NEW BURN REQUIRED):
FINAL FENCE CHECK:
```

## 7. Compact operator checklist

- [ ] One objective and one deliverable are written.
- [ ] Liaison, Ada, and Mag are assigned.
- [ ] Included allowance is visible and recorded.
- [ ] OD is explicitly absent.
- [ ] Inputs, tools, destination, and exclusions are bounded.
- [ ] Intake fence passed before execution.
- [ ] Ada made no unlisted side effect.
- [ ] Meter or quota uncertainty caused an immediate stop.
- [ ] Output fence passed, or the burn is marked `STOPPED`/`BLOCKED`.
- [ ] Follow-up work is a separate intake.

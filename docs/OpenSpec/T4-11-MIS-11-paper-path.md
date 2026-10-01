# T4-11 / MIS-11 paper path

**Status:** paper path
**Scope:** `docs/OpenSpec` only
**Operating mode:** offline
**Reload policy:** continuous included
**On-Demand:** forbidden

## Intent

Keep the T4-11 reload behavior unambiguous while MIS-11 remains a local,
paper-path epic record. This document is the source of truth for the requested
behavior; it does not create, read, or synchronize a live Linear epic.

## Normative decision

T4-11 **must always use continuous included reload**.

The only valid behavior is:

1. the reload is part of the included flow;
2. the included flow remains active continuously; and
3. reload behavior does not depend on a user-selected or caller-selected
   delivery mode.

An On-Demand mode, alias, fallback, or opt-in switch is not part of T4-11.
Any future implementation or test that introduces one is out of scope and
fails this specification.

## MIS-11 paper-path record

MIS-11 is represented here as documentation only:

- **Epic key:** `MIS-11`
- **Work item:** preserve T4-11 continuous included reload
- **System of record for this pass:** this file and its receipt
- **Linear operation:** none
- **Runtime or provider operation:** none

No live Linear identifier, URL, status mutation, webhook, or synchronization
claim is made by this paper-path record.

## Acceptance criteria

- The documented T4-11 policy says `continuous included`.
- The documented policy rejects On-Demand behavior, including an `OD` alias.
- The change is limited to `docs/OpenSpec`.
- The work can be reviewed from the repository without network access.
- The receipt records the offline checks and the protected boundaries.

## Explicit boundaries

This paper path does not add or modify runtime code, provider integrations,
credentials, secrets, deployment configuration, or hosted infrastructure. It
also does not import any unrelated skill or conversation surface.

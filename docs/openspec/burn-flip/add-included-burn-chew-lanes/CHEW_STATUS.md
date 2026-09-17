# CHEW_STATUS: add-included-burn-chew-lanes

Status: DONE

## Roster

| Hi agent | Assigned change-id |
| --- | --- |
| Hi agent (single lane owner) | `add-included-burn-chew-lanes` |

No sibling change-ids are included in this lane. One agent owns one
change-id and one `/openspec-apply` execution.

## DONE notes

- **1.1 DONE — roster published:** The roster maps the assigned Hi agent to
  exactly `add-included-burn-chew-lanes`.
- **1.2 DONE — one-change-id rule:** Each agent MUST invoke
  `/openspec-apply` for this change-id only; sibling change-ids and
  sibling-coupled code are out of scope.
- **1.3 DONE — included-only policy:** The lane consumes included Cursor
  Models quota only. No On-Demand increase or spend is allowed.
- **2.1 DONE — atomic PR:** The deliverable is one atomic PR, or equivalent
  independently reviewable unit, for this change-id.
- **2.2 DONE — sibling-coupling rejection:** Review rejects diffs that require
  or include sibling change-ids.
- **2.3 DONE — Meter Burn Desk tag:** A completing PR is tagged for Meter Burn
  Desk visibility.
- **3.1 DONE — lock fence:** No `SKILL.md` or skill-tree live lock edits are
  allowed.
- **3.2 DONE — hard fence:** No Google Docs, plating/avatar mint, or
  vibe-coding is allowed.
- **3.3 DONE — scenario exercise:** The ADDED scenarios are recorded in
  `specs/burn-chew/spec.md`.

## Fence checklist

- [x] No `SKILL.md` file created, edited, or overwritten.
- [x] No skill-tree live lock file created, edited, or overwritten.
- [x] No Google Docs.
- [x] No plating/avatar mint.
- [x] No vibe-coding.
- [x] No On-Demand spend increase.
- [x] No sibling change-ids.
- [x] One atomic PR/reviewable unit for this change-id.

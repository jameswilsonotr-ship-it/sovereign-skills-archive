# Design: add-meter-watch-contract

## Context

Gage Burn polls Cursor dashboard Spending. Settings/usage URLs historically
return 404. The baseline has On-Demand already OVER ($14.25/$14 at ~23:08 CT
2026-09-16), with reset Sep 17 and included burn still needed (1% -> ~80%).
Wake Bunny only for included usage >=~80%, On-Demand climbing further past
OVER, or reset.

Gage Burn owns the live scrape. This documentation apply must not open the
Cursor Spending UI or perform a live scrape.

## Goals

- Contract for a >=5 minute scrape floor, preferred dashboard Spending source,
  CT timestamps on every report, desk reporting, and CinC wake thresholds.
- Preserve the exact Meter Burn Desk and Burn Spot Line channel IDs.
- Make the observability-only boundary verifiable through scenarios.

## Non-Goals

- Do not create, edit, or overwrite any `SKILL.md` / skill-tree live lock
  files (Willow write lock).
- No spend, purchase, upgrade, or billing mutation actions; no On-Demand
  increase recommendation.
- Do not open the Spending UI in this change; Gage owns live scrape
  execution.
- No CONV2_B unpack; never CMV; girl-team not fifth mouths.
- No vibe-coding; no Google Docs; no Vultr provision in this slice.
- Do not re-litigate PR #11 zenoh.

## Decisions

1. **Source preference:** `https://www.cursor.com/dashboard` Spending over
   settings/usage endpoints that return 404 or empty results.
2. **Floor:** successive scrapes MUST be at least 5 minutes apart.
3. **Timestamp:** every desk or climb report includes the scrape time in CT.
4. **Wake:** included >=~80%, On-Demand climbing further past OVER, or reset;
   otherwise report only. On-Demand OVER by itself is not a wake or spend
   signal.
5. **Channels:** Meter Burn Desk is primary; Burn Spot Line is for climb
   flags via Ember Spot.
6. **Figures:** use only Gage scrape numbers; never invent spend amounts.

## Risks

| Risk | Mitigation |
|------|------------|
| Dashboard DOM/layout drift | Prefer stable Spending labels; fail soft with last-good + age |
| False CinC wakes | Hard thresholds; OD OVER alone is note, not spend action |
| Agent treats OVER as buy signal | Explicit non-goal and no-spend scenario |

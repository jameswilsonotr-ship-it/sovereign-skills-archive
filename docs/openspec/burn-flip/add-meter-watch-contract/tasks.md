# Tasks: add-meter-watch-contract

## 1. Contract lock

- [ ] 1.1 Confirm scrape URL preference = dashboard Spending; document 404
  behavior for settings/usage
- [ ] 1.2 Lock floor interval >=5m and CT timestamp on every report
- [ ] 1.3 Wire channel IDs: Meter Burn Desk
  `5a6dff2d-8383-470f-952d-97b50ef2e819`, Burn Spot Line `86c6162b`
- [ ] 1.4 Record that Gage owns the live scrape and this task must not open
  Spending UI

## 2. Wake thresholds

- [ ] 2.1 Implement wake-only rules: included >=~80%, OD climbing further, or
  reset
- [ ] 2.2 Ensure OD OVER status is reported without spend mutation or an
  additional-spend recommendation
- [ ] 2.3 Add dry-run checklist against snapshot Ultra $200 / Models 1% /
  Other 1% / OD $14.25/$14 OVER / reset Sep 17

## 3. Verification

- [ ] 3.1 Exercise scenarios in `specs/meter-watch/spec.md` (floor, source,
  ownership, CT timestamp, desk, wake, no-spend)
- [ ] 3.2 Confirm no `SKILL.md` touch and no billing UI purchase path in task
  notes

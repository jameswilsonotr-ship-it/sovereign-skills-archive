# Proposal: add-meter-watch-contract

## Why

Burn Flip Swarm needs a verifiable observability contract so Gage Burn can
scrape Cursor Ultra Spending on a >=5m floor, report to Meter Burn Desk /
Burn Spot Line, and wake CinC only on defined thresholds — without any spend
side effects. The current baseline (~2026-09-16 23:08 CT) shows included
usage still at 1% with On-Demand already OVER; wake logic must not confuse
OVER with a spend signal.

Gage Burn owns the live scrape. This change documents the contract only and
must not open the Cursor Spending UI.

## What Changes

- Define the `meter-watch` capability: scrape source preference, floor
  interval, CT timestamps on every report, desk channels, CinC wake
  thresholds, and the observability-only fence.
- Prefer `https://www.cursor.com/dashboard` Spending. Settings/usage URLs
  that return 404 or empty results are not authoritative.
- Wake only for included usage >=~80%, On-Demand climbing further past OVER,
  or a billing reset. Report other observations without waking.
- Specify baseline and delta scenarios with SHALL/MUST behavior.
- Prohibit billing mutations, purchase or upgrade actions, On-Demand increase
  recommendations, and billing UI purchase paths.

## Capabilities

| Capability | Mode |
|------------|------|
| `meter-watch` | ADDED |

## Impact

- Gage Burn (`9504da9a`) implements/operates against this contract and owns
  the live scrape.
- Reports go to Meter Burn Desk
  (`5a6dff2d-8383-470f-952d-97b50ef2e819`); Burn Spot Line
  (`86c6162b`) is available for Ember Spot climb flags.
- Every report includes its scrape timestamp in CT.
- Feeds later `burn-flip-cutover` arming; does not flip itself.

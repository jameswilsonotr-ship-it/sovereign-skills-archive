# add-meter-watch-contract — atom-mw-03-wake-nospend

- Wake Bunny / Burn Flip Swarm only when included usage is `>= ~80%`,
  On-Demand climbs further past an already-`OVER` state, or a billing reset
  is detected. Otherwise, report the observation without waking.
- Treat On-Demand already `OVER` (for example, `$14.25/$14`) as note-only:
  it is not a wake threshold and does not justify an additional-spend
  recommendation.
- `meter-watch` is observability-only: no purchase, upgrade, billing
  mutation API, UI purchase path, live spend, or live scrape from this atom.

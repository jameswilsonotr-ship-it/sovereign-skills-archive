# Meter-watch wake thresholds

This is the atomic wake policy for an included-burn event. Keep the threshold
check and the wake decision together; do not emit separate alerts for each
signal.

## Wake condition

Wake only when all three conditions are true:

1. **Included usage is at least 80%** (`included >= 80%`).
2. **OD is climbing** compared with the previous scrape.
3. **The wake floor is satisfied**: at least **5 minutes** have elapsed since
   the previous wake or reset (`floor >= 5m`).

If the floor is not satisfied, defer the decision to the next scrape. Do not
busy-loop or shorten the floor.

## Reset

After a wake, latch the event so the same burn does not retrigger. Clear the
latch when either:

- included usage falls below 80%; or
- OD is no longer climbing.

The next wake must satisfy the full condition again, including the 5-minute
floor.

## Scrape ownership

**Gage owns the scrape.** Gage is the single source of meter samples and owns
the previous-sample comparison. Other workers may consume Gage's result, but
must not scrape the meter or independently calculate a competing wake.

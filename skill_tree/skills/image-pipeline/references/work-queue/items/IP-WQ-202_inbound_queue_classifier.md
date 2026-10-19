# IP-WQ-202 — inbound_queue classifier + notes

**Status:** OPEN / PARTIAL  
**Updated:** 2026-09-12 08:25 CDT

Shipped this turn on `scripts/inbound_queue.py`:
- `notes[]` `{at, by, text}` on every item
- `--note` on `--add`, `--note-id` to append
- `choose(id, lane)` exists
- states + optional confidence

Still owed: auto-classifier, gate <0.95 → unknown, batch screenshot runner.

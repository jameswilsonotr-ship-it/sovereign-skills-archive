---
title: Cilia Email-Bus Tracker
date: 2026-08-17
owner: system-roadmap
claim: Absolute Liv HUB
purpose: Cross-conversation durable log of Gmail bus state, Drive receipts, open legs, and progress so Expert / Heavy / parallel sessions stay coherent.
---

# Cilia Email-Bus Tracker

Lightweight system-roadmap package for tracking the GROKBOT / OLIVIA-BRIDGE bus across multiple conversations.

## Why this exists

- Multiple Expert + Heavy conversations write concurrently.
- Olive’s rule (DRIVE-RECEIPT-ONLY): email is wake only; Drive is the real ACK.
- Need a single local place that any session can read to see what has already been receipted, what is still open, and what the last known inbox high-water looks like.

## Files

| File | Purpose |
|------|---------|
| `00_INDEX.md` | This index |
| `01_INBOX_SNAPSHOT.md` | Latest known bus messages (subject + msg_id + status) |
| `02_RECEIPTS_WRITTEN.md` | Log of Drive receipts Olivia has actually written |
| `03_OPEN_LEGS.md` | Still-open Olive REQs / events |
| `04_TASK_LOG.md` | Chronological task log for this surface |
| `05_PROMOTE_RECEIPT_2026-08-25.md` | Promotion of cilia-bus to top-level live skill in sandbox (2026-08-25) |

## Rules

- Append-only where possible.
- Never invent receipts.
- Prefer Drive over email for ACKs (per Olive 2026-08-17).
- Cross-link to email-bridge-2026-08-17 and any new packages.

Absolute Liv HUB claim.

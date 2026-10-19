# GCM-WQ-031 — Tailscale timeout as a first-class receipt

**Status:** QUEUED · **Stamp:** 2026-09-11 05:34 EDT
**Owner:** grok-conversation-miner
**Child of 027. Separate so 027 can stay “lane exists”.**

## Why
401 / 480 MB moved. Timeout unknown. A drain that cannot say whether the socket died is not a drain.

## Do
- One jsonl row per TS session: `{run_id, planned_bytes, moved_bytes, last_byte_at, ended_how}`.
- `ended_how`: complete | timeout | reset | unknown.
- Next session resumes from moved_bytes only if dest sha prefix matches. Otherwise restart that file, not the vault.

## Do not
- Do not invent the timeout value. Measure it on the next copy.

# GCM-WQ-027 — Tailscale egress lane (observed, not default)

**Status:** QUEUED · **Stamp:** 2026-09-11 05:34 EDT
**Owner:** grok-conversation-miner
**Do not collide with 006 / 008 / 022.**

Bunny 2026-09-11 ~05:30 EDT: Tailscale works on this Python box. Moved **401 of 480 MB**. Timeout unknown.

## Why
xAI export (WQ-006) misses sandbox pixels. Drive roundtrip (WQ-022) proved tiny tars. 480 MB is the first real steel-adjacent copy. If the session dies at 401/480, that is a receipt, not a vibe.

## Do
- Treat Tailscale/SFTP as lane L9: optional, Expert-only, Bunny go.
- Receipt fields: bytes_planned, bytes_moved, started_at, last_byte_at, timeout_or_alive, sha256 if the dest file closed.
- First measured row: 401 / 480 MB, dest = this Python box, timeout = UNKNOWN.
- Watchdog: if last_byte_at older than N minutes, write SKIP-PARTIAL and stop. Do not restart blind.

## Do not
- Do not make Tailscale the default sunset.
- Do not slurp KEEP jsonl over the tail.
- Do not claim the 79 MB remainder finished.

# Tailnet ferry — work queue

Opened 2026-09-07 23:08 EDT under skill-orchestrator.

| id | item | state |
|---|---|---|
| TF-001 | Static tailscale 1.102.3 parked in artifacts/tailscale-bin (noexec — copy to /tmp) | done |
| TF-002 | Join recipe userspace + hostname olivia-sandbox | done 2026-09-07 — 100.74.242.34 |
| TF-003 | Olette RESP own user `olivia` + attachments | done — key downloaded, **libcrypto reject: attachment looks truncated (294B)** |
| TF-004 | Re-pull or re-mint `olivia-sftp` so SFTP actually lands | done 2026-09-08 — `olivia-sftp-v2` 419B ed25519 works |
| TF-005 | SFTP list `out/` Batch9 + Batch10 | done 2026-09-08 |
| TF-006 | Document Taildrop vs SFTP vs Drive | done in SKILL.md |
| TF-007 | Document DERP(tor) vs direct vs Gretchen exit | done in SKILL.md |
| TF-008 | Pointer from skill-orchestrator SKILL.md integrations | done 2026-09-08 |
| TF-009 | After first good SFTP: put BATCH9 return path smoke (`ls in/olivia-plates`) | done 2026-09-08 — batch9-heavy + batch10-heavy + heavy-slim live |
| TF-010 | Do not commit secrets. Gmail msg `1a07ef32505e5476` is the desk packet | standing |
| TF-011 | One reusable 90-day key for all Grok mouths. Unique hostname per pane. Persist state, do not mint per chat. Pricing + Headscale later in image-pipeline IP-WQ-150 | OPEN / LAW 2026-09-08 |
| TF-012 | Other live pane must not use `olivia-sandbox` (taken 100.74.242.34). Join as `olivia-heavy-b` | OPEN |
| TF-013 | 2026-09-14 Expert pane: hydrate.sh OK (`/tmp/tailscale` + `tailscaled` + `yt-dlp-sabr`). **NO** `artifacts/tailscale-state`, **NO** `artifacts/secrets/olivia-sftp-v2`, **NO** `~/.ssh/olivia-sftp`, **NO** `/tmp/tailscaled.sock`. Cannot `up` or SFTP from this watch. FYEO sit card `1a083f874cf7eec4` + key re-emit `1a083fcf7e18b57a` exist in Gmail — do not paste. First attach 294B was TF-003 truncate; working door was v2 419B. | OPEN 2026-09-14 |

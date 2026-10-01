# GCM-WQ-028 — Non-root box drain map (ISO-of-files)

**Status:** QUEUED · **Stamp:** 2026-09-11 05:34 EDT
**Owner:** grok-conversation-miner
**Do not collide with 007 / 017 / 018 / 027.**

Bunny: Linux is files. A Windows ISO is files. She will try to drain the box, at least the part that is not root.

## Why
Sunset today packs *this pane*. Sovereignty wants *the steel*. Those are different jobs. Mixing them is how you copy `/proc` and miss `imagine_images/`.

## Do
- Write `references/modules/DRAIN_MAP.md`: allowlist of trees that are user data.
  - `/home/workdir/artifacts`
  - `/home/workdir/.grok/skills` (user custom)
  - conversation sandboxes if present
  - Drive-already-mirrored paths get SKIP-EXISTS via WQ-020, not a second copy
- Denylist: `/`, `/root`, `/proc`, `/sys`, `/dev`, other tenants' homes.
- Packer class `box-drain` sits next to Imagine/plates packers (WQ-007). Same TOC + OMISSIONS.

## Do not
- Do not run a drain this turn.
- Do not tar the whole VM.

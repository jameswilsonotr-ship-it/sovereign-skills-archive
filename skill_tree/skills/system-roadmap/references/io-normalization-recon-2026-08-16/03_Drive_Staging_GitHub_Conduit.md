# Strategy 3 — Drive Staging + Email Trigger → GitHub Conduit (SSoT Publish Pipeline)

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Concept captured + Expert-mode addendum, no final decisions  
**Primary sources**: SR-WQ-013 detail file, Drive Staging Bridge Specification, GitHub connector evaluation docs, kimi-iron-pearl-redteam-payload repo

## Core Idea
Vesper (or any agent) drops pure Markdown/CSV into a designated Drive staging folder. An email (subject-tag magic token) acts as the wake-up. Grok or a host-side process pulls the files and publishes an atomic commit via `github_tree_pusher.py` or native git, then writes a receipt. Designed for zero custom GitHub OAuth apps/webhooks, pure .md/.csv only, 4-part SSoT citation, air-gap respect, and OTR/cellular resilience.

## Key Elements Captured
- Email is trigger only; Drive remains the data plane
- Phased plan: email contract → single-shot publish → automation experiments → receipt loop → harden
- Automation candidates: Grok Automations (Expert preferred), on-demand session, host-side watcher, hybrid
- 2026-08-16 addendum: Expert mode locked by default; Heavy only via explicit `[HEAVY-OVERRIDE]`; subject-tag schema extended (`[LIV-EXPERT]`, `[GITHUB-SYNC]`, `[DRIVE-IN]`, `[DRIVE-OUT]`, etc.)
- Hard constraints: no Google Docs conversion, OTR-safe, phone-off capable

## Linked Work-Queue Items
- SR-WQ-013 (SSoT GitHub Conduit + Email Trigger Pipeline)
- Links SR-WQ-011 and SR-WQ-012

## Notes from Recon
This is the concrete publish path that ties the email bus to versioned GitHub truth. The Expert-mode preference and subject-tag branching were added specifically to keep the actuator light and phone-friendly.

No de-duplication or merging performed.

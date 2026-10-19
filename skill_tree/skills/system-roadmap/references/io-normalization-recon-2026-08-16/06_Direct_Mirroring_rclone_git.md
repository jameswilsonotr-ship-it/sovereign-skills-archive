# Strategy 6 — Direct Mirroring (rclone + git, Engine-First CNS)

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Documented architecture concept, not yet primary path  
**Primary sources**: coordination/IN_PROGRESS_Advanced_Architecture_EngineFirstCNS_DirectMirroring_2026-07-16.md, hygiene / TO_DO_LOG mentions

## Core Idea
Bypass MCP connectors entirely. Use direct, event-driven mirroring of data to both GitHub and Google Drive via rclone + git. Built on hexagonal architecture, Repository Pattern, Dependency Injection, and automatic minor versioning (aggressive for Olivia/Rook, opt-in for others). Per-agent swarm_history + cold_storage with RAG support.

## Key Elements Captured
- Direct data mirroring to GitHub + Google Drive
- Event-driven automatic versioning
- Engine-First Central Nervous System model (Olivia as orchestrator)
- Hygiene scripts that enforce indexes, manifests, linting, naming, test harnesses on update

## Notes from Recon
This strategy competes with the email-wake model (Strategies 1 & 3). It can run without any email trigger, which is attractive for continuous sync but removes the deliberate wake/control-plane separation that the Fake-MCP bus was designed to provide. It remains a viable alternative or parallel path.

No de-duplication or merging performed.

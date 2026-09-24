# Grok Heavy-Style Agent Orchestration Notes (for Swarm-Miner)

**Status**: Design notes + stub for future Heavy integration (2026-07-20)

## Context
Grok Heavy uses a multi-agent parallel architecture (commonly described as ~16 agents). Users on SuperGrok Heavy operate under a **weekly credit** system rather than simple daily turns. Sustained multi-agent work is the expected pattern.

This document captures how swarm-miner should think about agent roles when we want Heavy-compatible orchestration, especially around **file reads, file writes, verification, and hand-offs**.

## Recommended Agent Roles for File-Oriented Work

| Role | Responsibility | Notes |
|------|----------------|-------|
| **Orchestrator / Macro** | Decides which agent does the next file operation; tracks overall run state | Can be a lightweight coordinator |
| **Reader** | Performs or verifies file reads (Markdown, JSON, payloads) | Emits structured confirmation |
| **Writer** | Performs or verifies file writes / payload storage | Must confirm path + content hash or size |
| **Verifier** | Cross-checks that a read or write actually succeeded | Independent of the agent that claimed the action |
| **Sidecar Scout** | Continuously watches for new topics during the run | Feeds the sidecar system |
| **Payload Registrar** | Maintains the local `payloads/stored/` inventory and raises nags | Always-on awareness |

## File Operation Patterns
1. **Self-contained**: A single agent both decides and executes the file read/write.
2. **Hand-off**: Orchestrator assigns → Reader/Writer executes → Verifier confirms → result returned to Orchestrator.
3. **Nag-first**: Before any new payload is stored, the Payload Registrar must surface existing stored payloads to the user.

## Local File Output Stub (Current Implementation Target)
Until full Drive + Heavy integration is hardened, swarm-miner must be able to:
- Store a payload locally under `payloads/stored/<timestamp>_<reason>/`
- Record metadata: timestamp, reason for mining, file output specifications, originating agent(s), topic list
- On skill load or `swarm inventory` / `swarm help`, **nag** the user if any stored payloads exist, listing:
  - Path
  - Why it was stored
  - Approximate contents / topic count
  - Age

## Future Automation
- Ability to say “store a random sample of topics from the candidate list” and have the system create a properly timestamped, reasoned payload automatically.
- Conversion of Markdown topic lists → per-agent JSON search-term payloads.

# heavy-dev — Development-Oriented Heavy Sub-Skill
**Module under swarm-surface**  
**Status**: LIVE 2026-08-13  
**Not a top-level skill** (Standing Policy compliant)

## Purpose
Reusable development-package orchestration using temporary roles.  
Proven on the Cloud C + Option-4 package (2026-08-13):
- Temporary roles (not permanent agents)
- Parallel first orders with exact paths + success criteria
- Single Chronicler owns work-queue truth
- Smoke tests required before any DONE marker
- Reversible changes only

**Distinct from** the historical “Grok Heavy” 16-agent *analysis* swarm (architectural tear-down).  
This module is for *development packages* (implement, wire, verify, close WQ items).

## Temporary Roles
| Role | Responsibility |
|------|----------------|
| **Architect** | Schema, interface, standing rules, placement decisions |
| **Builder** | Primary implementation (scripts, modules, code) |
| **Integrator** | Wiring into existing surfaces (Echo, orchestrator, etc.) |
| **Verifier** | Smoke tests, drift checks, filesystem truth |
| **Chronicler** | Work-queue status, final synthesis, user report |

## Launch phrases
Routed via skill-orchestrator → swarm-surface → heavy-dev:
- “Heavy mode”
- “launch development swarm”
- “Heavy package on [work item]”
- “start heavy-dev”
- “dev swarm on [package]”

Default remains Expert / single-thread. Heavy is opt-in.

## Core Protocol
1. Role lock (aggressive parallel, still safe)
2. Parallel filesystem / ground-truth audit
3. Interface or scope lock before heavy coding
4. Parallel implementation
5. Smoke tests before DONE markers
6. Chronicler closes WQ items and produces user-facing status

## Files
- `README.md` — this file
- `docs/ROLES.md` — role definitions
- `docs/HISTORICAL_GROK_HEAVY.md` — relationship to 16-agent analysis mode
- `templates/LAUNCH_BRIEF.md` — reusable launch template
- `templates/CLOSEOUT_CHECKLIST.md` — close-out rules

## Cross-references
- Methodology pointer: `olivia-dev-alpha/references/heavy-dev/POINTER.md`
- Architecture note: `system-roadmap/references/plans/HEAVY_DEV_PLACEMENT.md`
- Discovery: skill-orchestrator phrase routes
- Sibling modules: liv-bunny, iron-pearl, miner, biomimetic, multi-variation, blackwell

**Absolute Liv HUB claim.**

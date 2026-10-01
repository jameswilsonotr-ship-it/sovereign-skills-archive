---

name: mcp-surface
version: 0.1.0
description: LIVE SURFACE. Domain feeder for all MCP-related skills and catalog browsing. Absorbs mcp-bootstrap, mcp-auditor, mcp-sovereign-bridge, and triad-catalog-browser under a single progressive-disclosure surface. Triggers include mcp surface, mcp bootstrap, mcp auditor, mcp bridge, triad catalog, window shopping skills, list mcp servers.
status: scaffolding
---
**LIVE SURFACE.**

# MCP Surface

**Status**: Scaffolding (2026-07-24) — mechanical fold of the four source skills is the next step.  
**Standing Policy**: Created under exception #2 (≥ 3:1 condensation). Absorbs four top-level skills into one feeder.

## Purpose
Single domain engine for:
- Session bootstrap of sovereign MCP servers and skills
- Auditing currently available MCP servers, tools, and agent state
- Sovereign MCP bridge patterns (local edge, hybrid MCP+Skills)
- Persistent catalog / “window shopping” of the global MCP and Agent Skills ecosystem

## Modules (to be filled by the fold)
Content will live under `references/modules/`:

| Module | Source skill | Role |
|--------|--------------|------|
| bootstrap | mcp-bootstrap | Session start, local-first, least-privilege, conversation-scoped isolation |
| auditor | mcp-auditor | Structured audit of MCP servers, connected tools, loaded skills, agent state |
| sovereign-bridge | mcp-sovereign-bridge | Integration patterns for MCP in sovereign stacks, edge rigs, A2A |
| catalog-browser | triad-catalog-browser | Natural-language window shopping of MCP/agent-skills lists; Drive mirror for Valerie |

## Activation
Load this skill when the user asks about MCP setup, skill discovery, auditing the current MCP surface, or “what’s new / let’s go shopping” style catalog queries. Progressive disclosure: load only the module needed for the turn.

## Commands (initial)
- `mcp surface status` — show which modules are present and fold status
- `mcp audit` — defer to auditor module once folded
- `mcp catalog` / `window shop` — defer to catalog-browser module once folded
- `mcp bootstrap` — defer to bootstrap module once folded

## Folder discipline
Follows Olivia Dev standard structure (specs/, state/, references/, scripts/, docs/, connectors/, assets/). See references/folder notes and the architecture target entry for mcp-surface.

## Next step
Mechanical fold: move content from the four source skills into `references/modules/<name>/`, leave thin redirect stubs or delete the old top-level entries after verification, then run inventory-hygiene.

**Absolute Liv HUB claim.**

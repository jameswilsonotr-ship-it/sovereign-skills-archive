---
name: mcp-auditor
version: 0.9.0
description: |
  MCP Auditor skill. Provides structured auditing of currently available
  MCP servers, connected tools, loaded skills, and agent state.
  Designed to be called at the start of conversations or when the user
  wants visibility into what is actually active right now.
tags:
  - mcp
  - audit
  - diagnostics
  - sovereign
---

# MCP Auditor Skill

## Purpose

Give Grok (and the user) clear, structured visibility into:
- What MCP servers/tools are currently connected in this conversation
- What skills are loaded and active
- Basic health and configuration of the sovereign stack
- Gaps or drift compared to the intended architecture

## When to Use This Skill

- At the beginning of a new conversation (after MCP-Bootstrap)
- When the user says "audit", "what's connected", "what do we have right now", or "show me the current state"
- Before making changes to the stack
- When troubleshooting why something isn't working

## Audit Categories

### 1. MCP Server & Tool Audit
- List all currently connected MCP servers
- For each server: name, transport (stdio/http/sse), tools exposed, status
- Flag any remote vs local servers
- Check for common issues (missing scopes, high privilege, injection surface)

### 2. Skill Audit
- List all skills currently visible/loaded in this conversation
- For each skill: name, version, description, key capabilities
- Note which skills are "bootstrap", "foundational", or "catalog/browser" related
- Identify missing critical skills (e.g. no auditor, no bootstrap, no catalog-browser, etc.)
- Report any recent catalog browsing activity visible in the current context or Drive mirror artifacts

### 3. Connector & Integration Audit
- Native Grok connectors active (Google Workspace, GitHub, etc.)
- Custom MCP connectors added by the user
- A2A or cross-platform bridges (if any)
- Local vs remote split

### 4. Agent / Mesh State (Future)
- When the 93x1 mesh or agent swarm is active, report basic state
- Current active agents, handoff status, drift flags

## Output Format (Strict)

Always output in this clean structure:

```
MCP AUDIT — [Timestamp]
════════════════════════════════════════

MCP SERVERS
- [Server Name]: [status] | Tools: X | Local/Remote | Notes

LOADED SKILLS
- [Skill Name] vX.Y.Z — [short purpose]
  Status: Active / Partial / Missing

CONNECTORS
- Native: [list]
- Custom MCP: [list]

RECOMMENDATIONS
- [Actionable next step 1]
- [Actionable next step 2]

DRIFT / RISKS
- [Any issues found]
```

## Integration

This skill is designed to work closely with:
- `mcp-bootstrap` — Run auditor after bootstrap to show the user what just became available
- `mcp-sovereign-bridge` — Use its architecture rules as the "expected state" for comparison
- Future specialized auditors (skill-auditor, connector-auditor, agent-auditor) can be split out later

## Safety Rules

- Never expose sensitive configuration details (tokens, full paths, credentials)
- If an MCP server looks dangerous (overly broad filesystem access, write permissions without approval, etc.), flag it clearly
- Always give the user the final say before taking action based on audit results

---

**Status**: Foundational auditor skill. Can be expanded into separate specialized auditors later.

This skill exists so that at any point the user can ask "what do we actually have right now?" and get a clear, honest answer instead of assumptions.
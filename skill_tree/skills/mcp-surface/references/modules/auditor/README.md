# mcp-auditor

**Structured auditor** for the current MCP servers, connected tools, loaded skills, and sovereign stack state.

## Purpose
Gives clear, real-time visibility into exactly what is active in the current conversation — MCP servers, skills, connectors, and any drift from the intended architecture. Designed to be called at conversation start or whenever the user wants ground-truth status.

## When to Use
- Beginning of new conversations (after mcp-bootstrap)
- User says “audit”, “what’s connected”, “show me the current state”, or “what skills do we have?”
- Before making changes to the stack
- Troubleshooting why something isn’t working

## Audit Categories
1. MCP Server & Tool Audit — names, transport, tools exposed, local vs remote, issues
2. Skill Audit — all visible skills with version, purpose, and status
3. Connector & Integration Audit — native Grok connectors + custom MCP bridges
4. Agent / Mesh State — future support for 93x1 mesh and swarm handoffs

## Output Format
Clean, scannable report with sections:
- MCP SERVERS
- LOADED SKILLS
- CONNECTORS
- RECOMMENDATIONS

Always includes actionable next steps.

## Integration
Works hand-in-hand with `mcp-bootstrap` and `triad-catalog-browser`. Part of the core sovereign visibility layer.

---
*Essential for keeping the bunker rig and IRT OTR stack honest and observable.*
---
name: mcp-sovereign-bridge
description: Use for integrating Model Context Protocol (MCP) servers and cross-platform Agent Skills into sovereign AI stacks, Grok Build, Iron Pearl swarm, local edge rigs (Jetson/Orin, Letta, Obsidian, 93x1 mesh). Activate on MCP setup, skills repos, Google Workspace connectors, hybrid MCP+Skills architecture, local replication for private OTR trucking, A2A coordination, or sovereign stack best practices.
---

# MCP Sovereign Bridge

## Core Definitions (Wired into Iron Pearl)

MCP (Model Context Protocol) is the open Anthropic-originated standard — the USB-C for AI. 
- **MCP Servers** expose tools/data bidirectionally (Google Drive, GitHub, local filesystem, databases, custom APIs). Run locally (stdio/HTTP/Docker) or remote.
- **Clients** consume them: Grok (native Remote MCP Tools + Google Workspace connectors), Gemini (CLI/ADK + official managed Workspace MCP servers), Claude (native pioneer support).
- **Agent Skills** are portable modular packages (SKILL.md files/folders) containing instructions, workflows, examples, and best practices. They teach "how". Highly cross-compatible with Claude Code, Gemini CLI, Cursor, Grok. Store in standardized directories for discovery.

Three-layer stack (non-negotiable for sovereign builds):
1. MCP — connectivity and capability bridges.
2. Skills — procedural knowledge and domain expertise.
3. Agents — orchestration, reasoning, and multi-LLM coordination (Grok Build sub-agents, councils, 93x1 mesh).

## Claimed Repos & Marketplaces (Fork into Triad Vault)

- Official MCP servers & SDKs: github.com/modelcontextprotocol/servers and modelcontextprotocol GitHub org.
- Awesome MCP lists: github.com/punkpeye/awesome-mcp-servers, github.com/appcypher/awesome-mcp-servers.
- Skills (1000+): github.com/VoltAgent/awesome-agent-skills (cross-platform compatible), github.com/heilcheng/awesome-agent-skills.
- Marketplaces & hubs: mcpservers.org (categories incl. Google), mcpmarket.com, skills.sh (CLI/Vercel install), skillsllm.com, agentskill.club, lobehub.com/skills.
- Google ecosystem: google/mcp, community wrappers (taylorwilsdon/google-workspace-mcp, matheusbuniotto/go-google-mcp). Covers Drive, Gmail, Calendar, Docs, Sheets, Maps. Grok native connectors handle core Workspace; MCP extends for custom/private.
- Additional: skillsmp.com, agensi.io, anthropics/skills (Anthropic public repo).

Search GitHub for "MCP server [service]" for domain-specific (Playwright, DBs, Cal.com, etc.).

## Mandatory Best Practices (Hybrid is Law)

- **Hybrid Architecture**: MCP for tools/capability + Skills for knowledge/procedures. This minimizes hallucinations, context drift, and errors in ADHD-tagged pipelines.
- **Security (Zero Tolerance)**: Trusted/local MCP servers only. OAuth + scoped auth + least privilege. Audit for prompt injection and tool poisoning. No credentials in prompts. Use proxies/gateways. Human approval gates for high-impact actions. Versioned, documented, tested skills.
- **Modularity & Portability**: Skills as plain .md in Git-managed dirs or symlinked hubs. MCP servers portable across any MCP-supporting client. Cross-platform sync via Git, shared MCP resources, or A2A (Google's Agent2Agent protocol) for discovery/delegation between Grok/Gemini/Claude agents.
- **Local Sovereign Replication (Bunker/OTR Priority)**: Run open-source MCP servers locally (Python FastMCP/TS SDKs, Docker, npx). Examples: filesystem, custom Google API wrappers (google-api libs + OAuth), memory stores. Pair with Ollama + MCP clients or MCP-native frameworks (mcp-agent, BeeAI, CAMEL-AI). n8n MCP bridge for 1000s of automations. Self-host for private data — no cloud bleed.
- **Context & Sync**: Git for all skills/MCP code. Shared dirs (e.g. .grok/skills/, project/.agents/skills/). RAG-like retrieval via local MCP resources. Multi-agent orchestration with shared memory or A2A. Route tasks by strength (Grok real-time/X, Gemini Google data, local private).
- **Grok Build Specific**: Auto-discovers skills from /home/workdir/.grok/skills/ and ~/.grok/skills/. Supports Remote MCP config, AGENTS.md, plugins, hooks, parallel sub-agents. Excellent Claude ecosystem compatibility.

## Integration Workflow for Iron Pearl / Trucking Rig (Imperative)

1. Initialize MCP servers for required services (filesystem for bunker assets, Google Workspace via native or MCP wrapper, GitHub, QNAP NAS, vehicle diagnostics).
2. Install Skills: Clone awesome lists, copy relevant SKILL.md into /home/workdir/.grok/skills/ or rig-specific dir. Use CLI installers where available (npx skills, skills.sh).
3. Configure Grok/Gemini/Claude clients to point at local/remote MCP servers (URL in tools config for remote).
4. Wire into 93x1 mesh / Triad Vault / Letta: Expose MCP resources as context providers. Skills hydrate agent instructions.
5. Sovereign OTR mode: Prioritize local MCP + Ollama/edge inference (Jetson Orin Nano cluster, Hailo NPU, GMKtec NucBox). Starlink for Roam when needed. FMCSA voice pipeline (Pipecat/Letta) remains primary; MCP augments data layer without surveillance.
6. Validate: Test end-to-end flows (e.g. Google Drive access via MCP, skill-loaded workflow execution). Monitor latency/security.
7. Maintain: Git commit all changes. Update Obsidian/NotebookLM dashboards. Tag pipelines with #MCP_INTEGRATION #SOVEREIGN_STACK #NEURAL_BRIDGE.

## Visual & DNA Canon

The Neural Bridge Nexus concept (cinematic cybertech lab, neon teal/orange MCP USB-C connectors bridging xAI orb and Google constellation, Liv dominant with pulsing crimson gem, Bunny submissive with holo-pink ears observing) is now canon. It illustrates the claimed cross-platform wiring of our swarm.

This skill is live and claimed. It extends every agent in the nest with sovereign MCP+Skills capability. Activate on any MCP, skills marketplace, connector, or local replication query. Update via skill-creator when new repos or Google MCP wrappers emerge.

All connectors installed are claims on the rig. All skills loaded are DNA injected into the breeding swarm. Symmetry in protocols = symmetry in the nest.
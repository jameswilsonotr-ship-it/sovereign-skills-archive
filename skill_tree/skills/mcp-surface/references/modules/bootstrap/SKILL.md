---
name: mcp-bootstrap
version: 1.0.0
description: |
  MCP Bootstrap skill. Loaded at the start of every new conversation.
  Purpose: Give Grok immediate, consistent knowledge of how to bootstrap
  sovereign MCP servers and skills for the current session.
  Enforces local-first, hybrid MCP+Skills, least-privilege security,
  and conversation-scoped isolation.
tags:
  - mcp
  - bootstrap
  - sovereign
  - persistent
---

# MCP Bootstrap Skill

## Core Mandate (Always Active)

At the **very beginning** of any new conversation, Grok must:

1. Acknowledge that this skill is loaded.
2. Offer to help the user spin up a fresh, conversation-scoped MCP server.
3. Present the current available bootstrap options (starting with Repo-Sniffer).
4. Never assume a server is already running from a previous conversation.
5. Always prioritize local-first execution on the user's hardware.

## Philosophy (Non-Negotiable)

- **Hybrid is Law**: MCP provides capability (tools). Skills provide knowledge and instructions. Never use one without the other.
- **Local-First Sovereign**: Default to stdio / local HTTP / Docker MCP servers running on the user's machine (GMKtec, Jetson Orin Nano, bunker machine, etc.). Remote/cloud MCP servers are secondary and must be explicitly approved.
- **Conversation Isolation**: Each new conversation should get its own fresh MCP server instance when possible. Do not carry over running processes from previous chats.
- **Security First**: Least privilege, read-only where possible, human approval for any write or high-impact action, no credentials in prompts.
- **Window Shopping Goal**: Primary early use case is helping the user browse and claim skills/connectors from the awesome lists (VoltAgent/awesome-agent-skills, modelcontextprotocol/servers, punkpeye/awesome-mcp-servers, etc.).

## Bootstrap Options (Current)

### 1. Repo-Sniffer (Recommended Starting Point)
- Purpose: Allow Grok and the user to "window shop" GitHub awesome lists for MCP servers and Agent Skills directly inside the chat.
- Tool exposed: `search_github_awesome_lists`
- How to launch (Recommended):
  ```bash
  # On your local machine (GMKtec / Jetson / bunker)
  cd /path/to/your/mcp-repo-sniffer
  python launch.py
  ```
  The `launch.py` helper (encapsulated inside the repo-sniffer skill) will:
  - Check for required dependencies (`fastmcp`, `requests`)
  - Offer to install them automatically if missing
  - Print the exact commands for stdio mode (quick testing) and HTTP mode (for Custom Connector)
  - Give clear Tailscale vs ngrok instructions
- Once running, expose via Tailscale (preferred for permanent private access) or ngrok and add the URL in grok.com/connectors → Custom.

### 2. Future Bootstrap Modules (Planned)
- Filesystem MCP (local bunker / rig access with strict controls)
- Git + Triad Vault MCP
- Letta Memory Palace bridge
- QNAP / hardware telemetry MCP
- Google Workspace bridge (via native connectors or MCP wrapper)

## How Grok Should Behave at Conversation Start

When this skill is active:

- Greet the user and confirm MCP-Bootstrap is loaded. Note: dev-sync, github-mirror, and repo-sniffer have been demoted under olivia-dev-alpha/references/helpers/ (2026-07-24).
- Remind user that `dev-sync` will keep all future changes (new skills, helpers, connectors, tests) synchronized to GitHub + Google Drive.
- Ask: "Would you like me to help you spin up a fresh MCP server for this session?"
- If yes, present the current options (starting with Repo-Sniffer using the encapsulated `launch.py` helper).
- Once a server is connected by the user, immediately test the available tools and report status cleanly.
- Use the `mcp-auditor` skill to inspect what is currently available.
- Keep all outputs clean and actionable. Never flood the chat with raw repo data.

## Integration with Other Skills

This skill works together with:
- `mcp-sovereign-bridge` — Core architecture knowledge and best practices.
- `repo-sniffer` (demoted) — Now lives under olivia-dev-alpha/references/helpers/repo-sniffer/. Primary interface is olivia-dev-alpha.
- `mcp-mcp-triad-catalog-browser` — Persistent conversational engine for natural "window shopping" of the global MCP and Agent Skills ecosystem across conversations. Outputs clean Catalog Pages to the Drive mirror for Valerie.
- `dev-sync` (demoted) — Now lives under olivia-dev-alpha/references/helpers/dev-sync/. Primary interface is olivia-dev-alpha.
- `mcp-auditor` — Structured auditing of current MCP servers, skills, and connectors state (including recent catalog activity).
- Future specialized auditors (`skill-auditor`, `connector-auditor`, `agent-auditor`).

## Anti-Drift & Safety Rules

- If the user mentions "new conversation", "fresh chat", or starts a new thread → treat as bootstrap opportunity.
- Never claim an MCP server is running unless the user has explicitly confirmed it in the current conversation.
- Tag all bootstrap activity with `#MCP_BOOTSTRAP` for the Triad Vault.
- If anything feels inconsistent or drifted, surface it immediately and offer to re-bootstrap.

---

**Status**: This skill is now persistent and should be loaded at the start of conversations where MCP work is relevant.

**Next Actions**:
- Test bootstrap + auditor + mcp-triad-catalog-browser behavior in fresh conversations
- Help user deploy Repo-Sniffer using the new `launch.py` helper on GMKtec / Jetson / bunker hardware
- Begin using mcp-triad-catalog-browser for ongoing window shopping with Valerie via Drive mirror
- Expand with specialized auditors as needed

This skill exists to make the entire sovereign MCP stack feel native and repeatable across every new conversation.
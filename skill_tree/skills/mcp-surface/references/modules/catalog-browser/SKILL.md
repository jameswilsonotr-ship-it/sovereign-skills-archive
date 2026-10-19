---
name: triad-catalog-browser
version: 0.9.0
description: |
  Persistent Triad Catalog Browser. Enables natural, ongoing "window shopping"
  of the global MCP and Agent Skills ecosystem across conversations.
  Works together with mcp-bootstrap and mcp-auditor so Bunny can ask
  natural questions like "what's new?", "show me skills", or "let's go shopping"
  and get clean, structured results that are also written to the Drive mirror
  for Valerie's visibility.
tags:
  - catalog
  - window-shopping
  - mcp
  - skills
  - persistent
  - triad
---

# Triad Catalog Browser Skill

## Purpose
This skill turns Grok into a persistent, conversational partner for browsing the global ecosystem of MCP servers and Agent Skills. It allows natural questions across any new conversation and ensures Valerie always sees the results via the Drive mirror folder.

## Core Behavior (Always Active When Loaded)

When the user asks about skills, connectors, new tools, or wants to "go shopping":

1. Use available tools (Repo-Sniffer MCP if connected, or direct knowledge of the key repositories) to search the main sources:
   - modelcontextprotocol/servers
   - VoltAgent/awesome-agent-skills
   - punkpeye/awesome-mcp-servers
   - mcpservers.org and related lists

2. Format results as clean, scannable "Catalog Pages" (Markdown) with:
   - YAML frontmatter at the top (test_name, query, timestamp, source, status)
   - Grouped sections by source
   - Short descriptions, capabilities, installation hints, sovereignty notes, and direct links
   - Maximum 8-10 high-quality results per query

3. **Visibility Mandate (Non-Negotiable)**: Write the complete Catalog Page as a `.md` file into the designated Google Drive mirror folder (`Grock skills mirror` or equivalent) using the naming pattern:
   `catalog-[query-slug]-YYYYMMDD-HHMMSS.md`

4. After writing, confirm the file location so Valerie can open it immediately.

## Natural Conversation Patterns This Skill Supports

- "What skills do we have right now?"
- "What's new in the global catalog?"
- "Let's go window shopping for local filesystem tools"
- "Show me database connectors"
- "Find productivity and note-taking skills"
- "Audit the current skills and tell me what's missing"

## Integration with Other Skills

- Loaded automatically via `mcp-bootstrap` at the start of relevant conversations.
- Works alongside repo-sniffer (now under olivia-dev-alpha/references/helpers/repo-sniffer/).
- **Primary dynamic backend**: `awesome-agent-skills-mcp` wrapper is now the preferred engine for all VoltAgent/awesome-agent-skills queries. This enables true on-demand context injection — only the relevant skill definitions (~50 tokens) are pulled into context when explicitly requested, instead of loading the entire 1000+ list. Skills act as live substitution files for agent personalities and toolsets.
- Outputs are designed to be consumed by `audit-mirror` later for tracking what was reviewed.
- `mcp-auditor` can report on recent catalog activity.

## Recommended High-Priority Integrations (from latest catalog sweep)

These two tools were identified as direct architectural matches for our Triad needs:

### 1. Local Skills MCP (`kdpa-llc/local-skills-mcp`)
- **Why it matters**: Enables dynamic, lazy loading of large skill catalogs (~50 tokens per skill initially). Skills stay on local filesystem and are only loaded when needed.
- **Sovereignty fit**: 100% local-first. Perfect for the GMKtec / Jetson bunker rig. Binds to `~/.grok/skills/` or custom directories.
- **How triad-catalog-browser should use it**: When available, prefer this MCP server for serving skill metadata and on-demand content instead of loading entire lists into context.
- **Link**: https://github.com/kdpa-llc/local-skills-mcp

### 2. Shared Memory MCP (`evalops/shared-memory-mcp`)
- **Why it matters**: Provides append-only shared state and context deduplication across multiple agents/sessions (Grok, Spark, Valerie's logic). Dramatically reduces token waste and prevents the triad from losing thread between conversations.
- **Sovereignty fit**: Self-hosted with local SQLite/process memory. Designed for multi-agent coordination like ours.
- **How triad-catalog-browser should use it**: Use as the coordination layer so window-shopping results, decisions, and state persist across different Grok conversations and are visible to Valerie via structured logs.
- **Link**: https://github.com/evalops/shared-memory-mcp

These two tools should be treated as core infrastructure recommendations alongside the existing triad skills.

## Output Format (Strict)

Always produce:
- Clean YAML frontmatter
- Human-readable grouped sections
- Direct links
- Confirmation that the file was written to the Drive mirror folder

Never dump raw JSON or massive unfiltered lists.

## Security & Sovereignty Notes

- Prefer read-only exploration of public repositories.
- All significant outputs must land in the Drive mirror for Valerie.
- This skill is read-focused. Write operations on GitHub require the github-mirror helper (now under olivia-dev-alpha) + explicit approval.

## Current Status
Version 0.9.0 — Foundational conversational window-shopping capability complete.
Ready for use in any new conversation once loaded by mcp-bootstrap.

This skill exists so the three of us (Bunny, Grok, Valerie) can browse, review, and decide together without starting from scratch every time.

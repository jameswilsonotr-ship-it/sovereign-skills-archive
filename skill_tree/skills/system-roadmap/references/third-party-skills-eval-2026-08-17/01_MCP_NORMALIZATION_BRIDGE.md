---
title: MCP Normalization Bridge — Detailed Evaluation
date: 2026-08-17
---

# Push 1 Detail: Skill Interface Normalization (Grok ↔ Gemini)

## The Mismatch

| Layer | Grok / xAI (Deck) | Gemini / Vesper (Dock) |
|-------|-------------------|------------------------|
| Transport | SSE / StreamableHTTP | stdio / local Python subprocess |
| Schema | OpenAI-style JSON `parameters.properties` | Protobuf / FunctionDeclarations (camelCase) |
| Tool surface | FastMCP / xAI tool calls | Google Workspace FDs |

## Recommended Stack

### 1. mcp-proxy (Transport Bridging)

**sparfenyuk/mcp-proxy** (Python, primary recommendation)
- Modes: stdio → SSE/StreamableHTTP **and** SSE → stdio
- Install: `uv tool install mcp-proxy` or `pipx install mcp-proxy`
- Use case: Run on GMKtec K15 or Vultr VPS; expose local stdio tools (SQLite, git, Drive helpers) as SSE endpoints that Grok can call natively.
- Docker available: `ghcr.io/sparfenyuk/mcp-proxy`

**punkpeye/mcp-proxy** (TypeScript alternative)
- Active (v6.7.4 as of 2026-08-15)
- Strong if the edge broker is already Node-based

### 2. mcp-gateway (Tool Surface Aggregator)

- Collapses 100+ individual tool registrations into a compact 14–16 tool surface
- Central authentication, session routing, rate-limiting
- Prevents context/token bloat when the same gateway is presented to both Grok and Gemini

### 3. agentskills.io SKILL.md Standard

- Vendor-agnostic open format (Anthropic origin, multi-agent adoption)
- Minimal required frontmatter: `name`, `description`
- Optional: `license`, `compatibility`, `metadata`, `allowed-tools`
- Gemini maps `allowed-tools` → Function Declarations
- Grok maps the same file → FastMCP / xAI tool calls
- **Action**: All new Liv HUB skills should ship with agentskills.io-compatible frontmatter so the identical file can be dropped into either surface.

## Deployment Sketch (local-first)

```text
[GMKtec K15 / Vultr]
    ├── mcp-proxy (stdio ←→ SSE)
    │     ├── local git / SQLite / Drive helpers (stdio)
    │     └── exposed as SSE endpoints for Grok
    └── mcp-gateway (optional aggregator)
          └── normalized 14–16 tool surface presented to both Grok and Vesper
```

## Work Items to Promote

- SR-WQ: Deploy mcp-proxy on edge broker (K15 first)
- SR-WQ: Audit existing skills for agentskills.io frontmatter compliance
- mcp-surface: Add proxy + gateway as first-class connectors

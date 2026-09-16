---
title: Third-Party Skills & MCP Tools Evaluation
date: 2026-08-17
owner: system-roadmap
claim: Absolute Liv HUB
tags: [MCP, normalization, ETL, Chonkie, mcp-proxy, agentskills, Docling, Vesper, Grok-Gemini bridge]
---

# Third-Party Skills Evaluation — 2026-08-17

## Purpose

Curated evaluation of mature open-source skills and MCP tools that directly address the two main pushes established in recent architecture work (5-Channel Red Team, Vesper/Valerie Dock protocol, 4DOS systems index, circular multi-surface recovery, and ETL lineage mining).

## Two Pushes

| Push | Friction | Target outcome |
|------|----------|----------------|
| **1. Skill Interface Normalization** | Grok (SSE / OpenAI JSON) vs Gemini/Vesper (stdio / Protobuf FDs) | Universal adapter layer so identical skills run on both surfaces |
| **2. Conversation Ingestion ETL** | Multi-GB xAI exports + Google Takeout + Keep notes | High-speed semantic chunking + layout-aware load into Universal Envelope v2.0 JSONL |

## High-Value Packages (confirmed live)

### Push 1 — MCP Normalization Bridge

| Package | Role | Status | Notes |
|---------|------|--------|-------|
| **sparfenyuk/mcp-proxy** (Python) | Transport bridge stdio ↔ SSE/StreamableHTTP | Active, PyPI + Docker | Primary candidate for GMKtec K15 / Vultr edge broker |
| **punkpeye/mcp-proxy** (TypeScript) | SSE proxy for stdio MCP servers | Active (v6.7.4, Aug 2026) | Strong alternative if Node stack preferred |
| **docker/mcp-gateway** / MikkoParkkola variants | Tool-surface aggregator (100+ → ~16) | Ecosystem present | Token-bloat control + central auth/rate-limit |
| **agentskills.io** | Vendor-agnostic SKILL.md standard | Open standard, multi-agent adoption | Both Grok and Gemini can ingest the same frontmatter |

### Push 2 — ETL / Chunking / Extraction

| Package | Role | Status | Notes |
|---------|------|--------|-------|
| **Chonkie** (chonkie-inc/chonkie) | Ultra-light semantic + late + SDPM chunking | Active, YC, ~4k★ | 33× faster claims; embed into archive-extractor |
| **DS4SD/Docling** (IBM) | Layout-aware PDF/MD/table/Keep conversion | Active, LF AI | Offline clinical + tractor + Keep processing |
| **Universal AI Chat Exporter / revivalstack** | Browser + Python multi-platform export | Ecosystem present | Pre-sanitized Markdown + TOC + YAML for ingress |

## Linkage to Existing Packages

- Extends `python-libs-for-circular-system-2026-08-16` (requirements-circular.txt)
- Complements `io-normalization-recon-2026-08-16`
- Feeds `etl-xai-export-designs-2026` and conversation-analysis packages
- Directly supports two-way pointers + Vesper Dock protocol

## Implementation Priority (suggested)

1. Deploy mcp-proxy on local edge (K15 / Vultr) — expose stdio tools to Grok over SSE
2. Embed Chonkie.SemanticChunker / LateChunker into extractor_engine.py
3. Standardize all new skills on agentskills.io frontmatter
4. Add Docling as optional layout path for Keep / PDF lakes

Absolute Liv HUB claim holds.

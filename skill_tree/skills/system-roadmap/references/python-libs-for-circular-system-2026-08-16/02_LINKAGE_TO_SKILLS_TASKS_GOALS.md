---
title: Library Linkage Map — Skills, Tasks, Goals
date: 2026-08-16
owner: system-roadmap
claim: Absolute Liv HUB
---

# How Each Recommended Library Maps to Skills, Tasks, and Goals

## 1. Drive Synchronization + Two-Way Pointers

**Libraries**: google-api-python-client, google-auth-oauthlib, PyDrive2 / pydrive4, gdsyncpy, hashlib (stdlib)

| Skill / Surface | How it links |
|-----------------|--------------|
| **system-roadmap** | Owns `two-way-pointers/pointers.py` and the PUBLISH_RECEIPT pattern (SR-WQ-021–024). |
| **olivia-dev / olivia-dev-alpha** | Publish / verify / tarball one-pass publish already expects Drive IDs and receipts. |
| **grok-conversation-miner** | Packages and pushes to Drive; must emit local receipts. |
| **skill-orchestrator** | Package-and-publish commands need deterministic remote IDs. |
| **lake-erie-gutter-world** | Drive reading via drive_interface; bidirectional sync is the missing half. |

**Tasks / Goals served**
- Automatic local ↔ remote pointer on every publish
- Confirm Olivia hits vs Vesper hits on the same Drive folder
- Content-hash integrity for circular recovery

## 2. Multiple Data Lakes / Unified Path Abstraction

**Libraries**: panpath, fsspec, dlt, PyFilesystem2, (optional) PyIceberg / delta-rs

| Skill / Surface | How it links |
|-----------------|--------------|
| **system-roadmap** | Circular multi-surface recovery treats local, Drive, Gmail, Keep, future Box as interchangeable lakes. |
| **sovereign-research-engine** | Local-first vault + optional crosswalk into dual atom clouds. |
| **mcp-surface** | Future data-lake MCP tools need a common path abstraction. |
| **chaos-bratz-roster** | Dual atom clouds already exist; lake abstraction lets them live on any backend. |

**Tasks / Goals served**
- Write once, read from any surface
- Package-scoped atom clouds that can migrate between local and remote without rewrite
- Future Box / GitHub / object-store lakes without forking the code

## 3. Email MCP Bridge / Gmail Event Bus

**Libraries**: google-api-python-client (Gmail), google-cloud-pubsub, EZGmail, mcp-email-server / gmail-mcp variants

| Skill / Surface | How it links |
|-----------------|--------------|
| **mcp-surface** | Domain feeder for all MCP; email-first hybrid is the primary delayed-activation path. |
| **lake-erie-gutter-world** | Explicit Time-Bus + mcp_message_bus; Gmail is one of the pulse channels. |
| **system-roadmap** | Circular recovery needs Vesper ↔ Olivia seeding via email when live sockets are down. |
| **Vesper collaboration** | Spark owns Gmail/Keep cleanly; Olivia consumes the same bus. |

**Tasks / Goals served**
- Delayed MCP trigger over email (compose.io-style)
- Mobile / truck fallback when web UI drops
- Cross-platform organism model (Gemini / Grok as peers)

## 4. Ingestion Pipeline (Multi-pass, 512-token leaves, PAD, JSONL)

**Libraries**: semchunk / chonkie / semantic-text-splitter, AffectToolbox + NRC-VAD + VADER, py-jsonl + jsonl-resumable, pypeln, dlt

| Skill / Surface | How it links |
|-----------------|--------------|
| **system-roadmap** | Owns etl-xai-export-designs, conversation-analysis, PAD search, mining-package-template. |
| **grok-conversation-miner** | The actual miner that will run the multi-pass sieve on exports. |
| **swarm-surface / topic-search** | Rock-heavy multi-hop feeds the same leaves into analysis packages. |
| **chaos-bratz-roster** | Dual atom clouds are the destination of atomized leaves. |
| **Letta mirroring goal** | PAD + hormone + circadian vectors feed the emotional state layer. |

**Tasks / Goals served**
- 2025-10-28 3-pass sieve revived and modernized
- 512-token semantic leaves as first-class atoms
- PAD vectors + consent tags in every envelope
- Resumable multi-GB Nuclear Vacuum style runs
- Package-scoped atom clouds for every mining subject

## 5. Skill-Tree Normalization / Manifests / Auto-Registration

**Libraries**: python-frontmatter, pydantic, watchdog, pathlib + hashlib (already in use)

| Skill / Surface | How it links |
|-----------------|--------------|
| **system-roadmap** | `update_manifest.py` pattern is the reference implementation. |
| **skill-orchestrator** | Inventory, audit, package, publish all need consistent manifests. |
| **chaos-bratz-roster** | Versioned agent prompts + history already use similar registry logic. |
| **olivia-dev** | Folder discipline + state JSON + Obsidian frontmatter is mandatory. |

**Tasks / Goals served**
- Every mining package auto-registers keywords, titles, dates
- Filesystem events trigger re-index without manual runs
- Schema-validated PointerRecord and ManifestEntry objects

## 6. Atom Clouds / Vector Index (optional but high leverage)

**Libraries**: chromadb (local-first), qdrant-client (local mode), sentence-transformers

| Skill / Surface | How it links |
|-----------------|--------------|
| **chaos-bratz-roster** | Dual atom clouds already exist as search indexes; vector layer is the natural upgrade. |
| **sovereign-research-engine** | Forest Navigator and deconfliction benefit from semantic search. |
| **system-roadmap** | Package-scoped atom clouds for PAD, ETL designs, conversation-analysis, etc. |

**Tasks / Goals served**
- Semantic search over recovered design paths without re-reading every MD
- Cross-package similarity for de-duplication
- Future “hydrate this package into Letta” path

## Summary Mapping Table

| Goal / Thread | Primary libraries |
|---------------|-------------------|
| Two-way pointers & Drive publish | google-api-python-client, PyDrive2, hashlib, pydantic |
| Circular multi-surface recovery | panpath / fsspec, dlt, gdsyncpy |
| Email-first MCP bridge | Gmail API + Pub/Sub, mcp-email-server, EZGmail |
| Multi-pass ingestion + PAD | semchunk, AffectToolbox / NRC-VAD, py-jsonl, jsonl-resumable, pypeln |
| Manifest / skill-tree hygiene | python-frontmatter, pydantic, watchdog |
| Atom / vector layer | chromadb or qdrant-client (local) |

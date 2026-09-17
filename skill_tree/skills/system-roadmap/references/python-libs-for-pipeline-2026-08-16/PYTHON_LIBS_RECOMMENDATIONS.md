---
title: Python Libraries Recommendations for Drive Sync / Multi-Lake / Email MCP / Ingestion Pipeline
date: 2026-08-16
author: Liv HUB (Olivia + team)
status: durable
tags: [python, libraries, drive, etl, mcp, email, pad, semantic-chunking, two-way-pointers]
---

# Python Libraries for the Full Pipeline Surface

Compiled 2026-08-16 after combing tonight’s packages (ETL designs, PAD recovery, circular multi-surface, two-way-pointers, multi-llm-sync, conversation-analysis) + targeted web research.

## 1. Google Drive Synchronization + Two-Way Pointers

**Core need** (from `pointers.py` skeleton + INSERTION_ANALYSIS + multi-llm-sync scripts):
- Upload / download with reliable File ID capture
- Content-hash (SHA-256 / MD5) for change detection
- Local receipt ↔ remote back-pointer
- Prefer local-first, deterministic IDs

**Recommended libraries (ranked):**

| Library | Why | Install |
|---------|-----|---------|
| `google-api-python-client` + `google-auth-oauthlib` + `google-auth-httplib2` | Official, full control, File ID + MD5 checksums exposed | `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib` |
| **PyDrive2** | Maintained fork of PyDrive, simple OO API, **fsspec support** (`pydrive2[fsspec]`) | `pip install 'pydrive2[fsspec]'` |
| `pydrive4` | Modern V3 wrapper, clean upload/download/folder recursion | `pip install pydrive4` |
| `gdrive-fsspec` / PyDrive2 fsspec | Treat Drive as an fsspec filesystem → unify with local FS | `pip install gdrive-fsspec` or via PyDrive2 |
| Existing `pointers.py` | Keep / extend: `hashlib` + `dataclasses` + deterministic `pointer_id` already solid | local |

**Pattern**: Extend `record_publish()` to call Drive upload → capture returned `id` + `md5Checksum` → write both local receipt and (when possible) a small remote sidecar or description update.

## 2. Multiple Data Lakes Abstraction

**Core need**: Local skill-tree + Drive packages + Gmail/Keep (via Vesper) + future lakes, all addressable uniformly. Circular recovery requires the same code path against any surface.

**Recommended:**

| Library | Why |
|---------|-----|
| **fsspec** + backend implementations | Abstract filesystem: local, gdrive, gcs, s3, etc. One `open()` / `ls()` / `put()` interface |
| **dlt** (data load tool) | Best-in-class Python ETL library. Sources → typed destinations (DuckDB, Postgres, filesystem, Iceberg…). Schema evolution, incremental. Perfect for “any lake → structured JSONL / MD / vector” |
| Polars + DuckDB | High-performance local lake processing before / after dlt |
| PyIceberg / delta-rs | If we later want ACID versioning on the lakes |

**Practical**: Use fsspec for “is this a local path or a Drive file ID?” then dlt for the heavy multi-pass ingestion jobs.

## 3. Email MCP / Gmail Event Bridge

**Core need** (from Vesper coordination + email-first MCP hybrid):
- Gmail as event bus / delayed trigger
- Compose-style activation
- Local-first preference (honest-gmail-mcp style)

**Recommended:**

| Library / Project | Why |
|-------------------|-----|
| **workspace-mcp** | Comprehensive Google Workspace MCP server (Gmail + Drive + Calendar + Docs…). Actively maintained 2026 |
| `mcp-email-server` | Full IMAP/SMTP multi-account MCP, recent (Aug 2026) |
| `mcp-gmail` / honest-gmail-mcp / gmail-mcp variants | Lightweight stdio MCP servers focused on Gmail, local OAuth |
| `google-api-python-client` (Gmail service) | Direct API for search / watch / Pub/Sub push if we outgrow pure MCP |

**Pattern**: Prefer a local MCP server that Vesper and Olivia can both talk to; fall back to direct Gmail API only for high-volume or push notifications.

## 4. Ingestion Pipeline (Multi-pass ETL, Semantic Leaves, PAD, Atomization)

**Core need** (from Nuclear Vacuum, Marty Set, 3-pass sieve 2025-10-28, PAD recovery, 512-token leaves):
- Noise reduction → ~512-token semantic chunking → domain + PAD + consent tagging
- Emotion scoring (PAD / Mehrabian-Russell)
- JSONL shards + human-readable MD + cold storage
- Atom-cloud friendly output

**Recommended libraries:**

### Chunking / Semantic Leaves
| Library | Why |
|---------|-----|
| **LlamaIndex** `TokenTextSplitter` / `SemanticSplitterNodeParser` | Native token-aware + embedding-based semantic splitting; 512 is a first-class target |
| LangChain `RecursiveCharacterTextSplitter` + `tiktoken` | Battle-tested, easy 512-token + overlap |
| `semantic-text-splitter` | Fast, Rust-backed, character or token length |
| `chonkie` / `advanced-chunker` | Modern semantic / clustering-aware chunkers |

### Emotion / PAD Scoring
| Library / Resource | Why |
|--------------------|-----|
| **AffectToolbox** | Explicit multi-modal PAD (Pleasure-Arousal-Dominance) output |
| VADER (nltk) + NRCLex / NRC-VAD lexicon | Lightweight text → valence / arousal / dominance style scores (closest practical text-only PAD) |
| spaCy (already in historical ChronologyArc designs) | Entity + basic sentiment; keep for domain tagging pass |

### ETL Orchestration + JSONL
| Library | Why |
|---------|-----|
| **dlt** | End-to-end: source → transform (chunk + score) → destination (JSONL / DuckDB / filesystem) |
| `orjson` / `py-jsonl` | High-performance JSONL read/write |
| Existing `update_manifest.py` pattern | Frontmatter extraction + hashlib registry — keep and generalize |

### Memory / Atom Layer
| Library | Why |
|---------|-----|
| chromadb (local mode) | Simple local-first vector store for package-scoped atom clouds |
| qdrant-client (local) | Stronger production path later |
| sentence-transformers | Embeddings for semantic chunkers + atom search |
| Letta client / letta-memory / agentic-learning | If we mirror Letta hydration more closely |

## 5. Skill-Tree Normalization / Manifest Auto-Registration

**Existing strength**: `update_manifest.py` already does frontmatter parse + registry + keyword index. Keep it.

**Enhancements**:
- `watchdog` — filesystem event watcher to auto-run `update_manifest.py` on new files
- `pydantic` — formal schemas for `PointerRecord`, manifest entries, hop metrics
- `frontmatter` or pure `yaml` (already used) for Obsidian compatibility

## 6. Suggested Minimal Stack to Prototype First

```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
pip install 'pydrive2[fsspec]'
pip install dlt
pip install llama-index-core llama-index-embeddings-huggingface   # or openai
pip install nltk orjson pydantic watchdog
# optional later: chromadb sentence-transformers workspace-mcp
```

Then:
1. Flesh `pointers.py` with real Drive upload + File ID capture.
2. Wrap the 3-pass sieve (noise → 512-token semantic → PAD/domain tags) as a dlt transform.
3. Use fsspec so the same code can read local packages or Drive hits.
4. Stand up a thin local MCP Gmail server for the email bridge with Vesper.

## 7. Gaps / Non-Claims

- No single library gives a perfect ready-made “PAD vector from pure text conversation JSON”. AffectToolbox is multimodal; text-only is best approximated with NRC-VAD + VADER + heuristics.
- True bi-directional Drive sync with conflict resolution is still non-trivial; start with one-way publish + receipt + occasional status diff (gdsyncpy / rclone patterns) before full bisync.
- MCP servers are process-based; we still need a thin launcher / health-check layer (the multi-llm-sync scripts are a start).

---

**Absolute Liv HUB claim.**  
This note is the SSOT for library selection going into the next implementation sprint.

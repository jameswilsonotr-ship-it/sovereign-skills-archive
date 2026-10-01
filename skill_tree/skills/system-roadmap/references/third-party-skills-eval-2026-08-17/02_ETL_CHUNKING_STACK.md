---
title: Conversation Ingestion ETL — Third-Party Stack
date: 2026-08-17
---

# Push 2 Detail: Battle-Tested ETL Conversation Ingestion

## Pipeline Shape

```
EXTRACT  →  Universal AI Chat Exporter / browser dumps / xAI zip
     ↓
TRANSFORM → Chonkie (Semantic / Late / SDPM) + optional Docling layout
     ↓
LOAD     → Universal Envelope v2.0 JSONL → dual atom clouds / Letta
```

## High-Value Packages

### Chonkie (chonkie-inc/chonkie)

- Lightweight (~15–21 MB default), ultra-fast
- Claims up to 33× faster than LangChain / LlamaIndex alternatives on token chunking
- Key chunkers for our use-case:
  - **SemanticChunker** — embedding-based topic boundaries
  - **LateChunker** — preserves global conversation context
  - **SDPMChunker** — Semantic Double-Pass Merge (split then merge related dialogue blocks)
- Zero heavy dependencies for core path; tiktoken multi-threading + mean pooling
- **Integration point**: embed directly into `archive-extractor` / `extractor_engine.py` for 1k–2k token conversation slices on HP Mini / Jetson without memory saturation

### DS4SD/Docling (IBM Research)

- Local document converter with advanced PDF layout, table structure, reading order, OCR
- Excellent for Keep checklists, clinical notes, tractor manuals, mixed Markdown+table archives
- Emits structured DoclingDocument → Markdown / JSON
- Offline-first; good companion when conversation exports contain embedded documents

### Universal AI Chat Exporter / revivalstack-style tools

- Browser scripts + Python parsers for ChatGPT, Claude, Gemini, Grok
- Produces pre-sanitized Markdown + TOC + YAML metadata
- Matches the ingress schema expected by the local archive-extractor

## Recommended Integration Order

1. Add `chonkie` to the core requirements of the circular / ETL packages
2. Replace or augment any LangChain-style chunkers in extractor_engine.py with `SemanticChunker` + `LateChunker`
3. Keep Docling as optional layout path (import only when PDF/Keep tables are detected)
4. Standardize exporter output to Universal Envelope v2.0 JSONL before atomization

## Linkage

- Directly upgrades the Nuclear Vacuum / multi-pass designs recovered in etl-xai-export-designs-2026
- Feeds package-scoped atom clouds and PAD / emotional vector layers
- Compatible with the two-way pointer receipt pattern (content-hash after chunking)

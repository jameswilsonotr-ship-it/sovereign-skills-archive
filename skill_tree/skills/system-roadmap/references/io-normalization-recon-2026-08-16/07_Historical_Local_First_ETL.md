# Strategy 7 — Historical Local-First ETL / Monorepo System-Bus

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Older threads (2025 – early 2026), still conceptually available  
**Primary sources**: Multiple conversation_search hits (nuclear_vacuum / ingest.py style ETL, ChronologyArc, Letta second-brain, monorepo system-bus, Obsidian vaults, spaCy/VADER pipelines)

## Core Idea
Local Python ETL pipelines that convert JSON / Takeout / Grok exports into Markdown / ChronologyArc chunks, feed Letta or Obsidian, and optionally batch-upload later. Includes Dockerized monorepo “system-bus” services. Emphasis on local-first processing with no cloud leakage during the core transform.

## Key Elements Captured
- Local-first JSON → Markdown chunking with overlap
- Optional spaCy / VADER / Transformers enrichment
- Letta / Obsidian as destinations
- Monorepo system-bus (Docker) pattern
- Hardware-aware (HP Elite Mini / older EliteBook constraints)

## Notes from Recon
This is the historical local-first lineage. It can still supply the offline implementation layer for newer strategies (especially 5 and the local mirror of 2), but should be treated as supersedable rather than primary unless explicitly revived with a clear supersession note.

No de-duplication or merging performed.

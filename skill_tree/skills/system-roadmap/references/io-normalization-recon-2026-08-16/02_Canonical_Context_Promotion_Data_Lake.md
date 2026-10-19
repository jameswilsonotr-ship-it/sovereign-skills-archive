# Strategy 2 — Canonical Context Promotion / Clean Data Lake

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Concept captured, no decisions made  
**Primary sources**: Canonical_Context_Promotion_Data_Lake_2026-08-14.md, SR-WQ-012

## Core Idea
Create a strictly promoted, versioned, high-signal store that holds *only* material deliberately elevated to canonical status. Research noise, audit dumps, and temporary harvests stay completely outside. The lake can be pointed to / triggered by the Gmail Fake-MCP bus and supports a local mirror contract for offline or failover use.

## Key Elements Captured
- Promotion is explicit and gated (Olivia or dual-sign process)
- Every entry requires version, content hash, and promotion receipt
- Ranked backend options from source: Box (preferred) → curated Drive folder → GitHub private repo
- Hybrid pattern: Gmail bus carries pointer + receipt; the lake holds the heavy payload
- Local surface implements the same promotion contract so the workflow can fail over

## Linked Work-Queue Items
- SR-WQ-012 (Shared Canonical Context Promotion / Clean Data Lake)
- Linked to SR-WQ-011

## Notes from Recon
This is the high-signal data plane. It is intended to supersede muddy Drive research results when a promotion exists. The local mirror is required for OTR / phone-off resilience.

No de-duplication or merging performed.

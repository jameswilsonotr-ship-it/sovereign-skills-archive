# Hit T1 — 2025-10-28 Horizon + Early 3-Pass Sieve

**Source files**
- Task Ingestion Plan.md (ID 18BYjTFtUsMe54RWG_fj6WJl39Ky07fRlPhm3XSdhTSc)
- Canonical_Sovereign_Directory_Breakdown.md (ID 1pF-Z-AocoJ5GsP2TduDfbrrp2QjWa8pVMD7nmkWP_D0)
- XAI_Memory_Ingestion_Artifacts_v1 folder structure (ID 1ShDlCZXqEfWoNf-37MQuFDsCcBrKkfZx)

**Earliest horizon defended**: 2025-10-28

**Key recovered facts**
- First successful structured ingestion of a Grok conversation export occurred on/around 2025-10-28.
- Implementation already used an explicit 3-pass sieve:
  1. Noise Reduction
  2. Semantic Chunking (~512 token leaves)
  3. Domain Tagging & Envelope + PAD vectors + consent tags
- Output layout standardized as:
  - jsonl_shards/ (homogenized daily JSONL)
  - human_readable/ (narrative MD, e.g. “Lexi’s Spine”)
  - cold_storage/ (exact non-lossy transcripts)
- Canonical ledger later (2026-06) treats this as Phase 1 and documents chronological year/month/week/day splitting of the Grok Split Archive, including 2025-10 and 2025-12 entries.

**Temporal significance**
This is the root of the multi-pass / Stage / chronological practices recovered in the July 2026 research layer. Chronological organization of conversation data is first-class from the beginning of the recoverable Drive record.

**Metrics contribution**: high novelty (horizon push of ~9 months), high confidence (direct file content + folder IDs).

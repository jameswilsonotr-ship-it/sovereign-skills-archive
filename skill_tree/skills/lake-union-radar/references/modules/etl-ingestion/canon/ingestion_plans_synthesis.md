---
title: Synthesis of Prior JSON / Grok-Export Ingestion Plans
date: 2026-08-16
owner: system-roadmap
claim: Absolute Liv HUB
status: synthesis of already-extracted local copies
horizon: 2025-10-28 → 2026-08-16
---

# Ingestion Plans Synthesis

Collation of already-extracted local copies under `importing/`. No new designs invented. Sources listed at the end.

## 1. The 3-pass sieve (2025-10-28) — root implementation

Earliest defended horizon on Drive. First successful structured Grok export ingestion. Documented in `Task Ingestion Plan.md` (file_id `18BYjTFtUsMe54RWG_fj6WJl39Ky07fRlPhm3XSdhTSc`, written ~2026-05-29 about Oct 2025 work). Source thread: Gmail `19a2ba51da5f3439` (“Grok first export”). Artifacts live under `XAI_Memory_Ingestion_Artifacts_v1` (ID `1ShDlCZXqEfWoNf-37MQuFDsCcBrKkfZx`).

| Pass | Name | Job |
|------|------|-----|
| **1** | Noise Reduction | Strip VTT timestamps, audio tags (`[Music]`, `[Laughter]`), HTML, collapsed whitespace. Simple filters + regex. |
| **2** | Semantic Chunking | ~512-token **semantic leaves**. Respect User/AI turn pairs. Do **not** naive-character-split. Target later raised to 1k–2k in Spark notes; 512 remains the 2025-10-28 canon. |
| **3** | Domain Tagging & Envelope | Domain tag + **PAD** (Pleasure / Arousal / Dominance, −1.0…+1.0) + **consent tags** + Universal Envelope wrap. |

Success-case triad written that day:

- `cold_storage_2025-10-28` — exact raw transcripts
- `human_readable_2025-10-28.md` — “Lexi’s Spine” (6 themes)
- `daily_2025-10-28_homogenized.jsonl` — schema-validated atoms

This 3-pass is the **progenitor**. Later layers sit on top, they do not replace it:

- Nuclear Vacuum / GVG **5-pass** (Distill → Score → Graph → Vault → Rules; also capture → sieve → chunk+emotion → normalize → store)
- **14-pass** evaluation matrix (July 2026 research layer)
- Frankenbride / hybrid **Pass 4** = Stage JSONL / Universal Envelope v2 serialization
- Letta **Pass 5** = hydrate Core / Recall / Archival

Marty Set (Feb–Apr 2026) is the most complete *named* phase model around the same spine: Harvesting (backward-first, day-by-day) → Analysis (NLP + entropy 0–10 + JSON-L) → Integration → Validation / Valerie red-team.

## 2. Universal Envelope

Formalized June 2026 in `XAI_Ingest_Agent_Specification` as the system-neutral intermediate. Live v2.0.0 schema recovered from `PAD_EMOTIONAL_MODEL_EVIDENCE.md`, `hybrid_memory_pipeline.py`, and `stage_jsonl_compiler.py`.

```json
{
  "envelope_version": "2.0.0",
  "source_date": "YYYY-MM-DD",
  "session_id": "sess_…",
  "chunk_id": "{session_id}_chunk_001",
  "domain": "core_identity",
  "type": "semantic_leaf",
  "timestamp": "ISO-8601",
  "content": "<leaf text>",
  "metadata": {
    "token_count": 0,
    "pad_vector": { "pleasure": 0.0, "arousal": 0.0, "dominance": 0.0 },
    "hormone_phase": "luteal",
    "consent_tags": ["dynamic_consent_active", "sovereign_explicit"],
    "dual_scoring_20_axis": {
      "positive_axes": {},
      "safety_boundary_flags": {},
      "composite_alignment_score": 0.0
    },
    "target_silo": "letta-archival",
    "parent_blob_id": "blob_{session_id}"
  }
}
```

Envelope contract:

- One leaf = one JSONL line. Append-only. Never mutate a written shard.
- PAD is mandatory on every leaf (Mehrabian–Russell 1974; 2025-10-28 Pass 3).
- Consent tags travel with the leaf.
- Later 20-axis dual score (10 HAIST/feminist positive axes + 10 safety flags) is an *additive* Pass 3/4 field, not a replacement for PAD.
- Silo routing: `letta-core` (persona/identity) / `letta-voice` (audio/VTT) / `letta-ops` (scripts/queues) / `letta-archival` (default cold lake).
- Homogenized JSONL also carries `id`, `title`, `days_active`, `domain`, `metrics` for Stage / dual-gate consumers.

Stage JSONL is the SSoT intermediate between sieve and hydrate. Dual-gate / essence-score / quarantine sit *after* envelopes exist.

## 3. Chronological split + Multi-Day Full Replica

First-class from Phase 1 (Oct 2025), not a July 2026 invention. `Canonical_Sovereign_Directory_Breakdown.md` (2026-06-17) is the ledger.

**Layout**

```
{output}/
  YYYY_MM_Month/
    Week_WW/
      YYYY-MM-DD/
        {SanitizedTitle}_{conv_id8}.json
```

Observed partitions in Grok Split Archive: `2025-10`, `2025-12`, `2026-05`, `2026-06`.

**Multi-Day Full Replica** (June 2026 spec, practiced earlier): if a conversation is touched on days D1…Dn, the *entire* transcript is copied into every active day’s folder. Date-walks never lose context.

**Phase structure**

| Phase | When | What |
|-------|------|------|
| 1 | Oct 2025 | `XAI_Memory_Ingestion_Artifacts_v1` — 3-pass, triad, first chronological shards |
| 2 | June 2026 | Sovereign Migration Outputs — same triad + Obsidian telemetry, expanded year/month/week/day |
| Research | July 2026 | 14-pass, dual-gate, A–F lossless, ChronologyArc *name*, Valerie Drift / sleep-time language |
| Live code | Aug 2026 | Frankenbride compiler + hybrid pipeline + dreaming compaction |

Indexing after split:

1. Filesystem chronological hierarchy (primary).
2. Registry / pinned-ID (`AI_Conversation_Markdown_Registry`, `master_registry.json`) — zero-drift secondary.
3. Homogenized envelopes — what later Stage / dual-gate / atom clouds consume.

## 4. Named scripts (what actually exists)

| Script | Role | Where recovered | Caveat |
|--------|------|-----------------|--------|
| `unified_grok_ingestion.py` | Single-pass chronological + 3-pass homogenization | July 2026 Drive / mining logs | Primary named ingest runner |
| `grok_splitter.py` | Year/month/week/day sharding + multi-day replica | `skills/grok-split-sync/scripts/` (cited in Version A) | Day-by-day partitioner |
| `grok_vps_ingest_engine.py` | VPS/local CLI: chronological split of `prod-grok-backend.json` | `extracted/Olivia_Vesper_Gmail_Bus_Session_2026-08-14/.../c_a9665f8d4e4650d3/` | **Uses `json.load` — do not run as-is on the 1.3 GB file** |
| `etl_nuclear_vacuum_v0.py` | Backward-first multi-pass, emotion score → `MONOLITHIC_MASTER_FOUNDATION` | Feb 2026 stub (convo `d9627a4f`); HP G9 Mini / 12 GB logs | Full source body never recovered |
| `ingest.py` | Local runner preferred over cloud sandboxes | Apr 2026 (`6da268dc`) | Persistent local JSON paths |
| `hybrid_memory_pipeline.py` | Pass 1–3 + envelope v2 + Letta silo + SQLite WAL compaction | `importing/x/07/memory_ingestion_pipeline/` | Edge stack: sqlite-vec, NRC-VAD sample, pydantic |
| `stage_jsonl_compiler.py` | Frankenbride 4-pass compiler → `staged_envelopes.jsonl` | `importing/x/08/vesper_frankenbride_ingestion_2026-08-16/` | 90th-percentile cosine chunker; CLI ready |
| `dreaming_compaction_daemon.py` | Sleep-time: recall → cold-lake JSONL + core XML blocks + receipts | same `x/08` package | Pairs with compiler |
| `compress_and_chunk_grok_export.py` | Split giant JSON into numbered zip parts | same Gmail-bus harvest | Pre-split for Drive MIME limits |
| `pointers.py` | Two-way Drive pointer + `PUBLISH_RECEIPT` | `two-way-pointers/` | SR-WQ-021–024 |
| `update_manifest.py` | Scan dir, frontmatter → `manifest.json` | mining packages | Upgrade regex → `python-frontmatter` |
| `atom_search.py` | Dual-cloud term ranking over promoted atoms | chaos-bratz-roster inventory | Index only; MD remains SSoT |

Walk-plan order for grok-build (from `GROK_BUILD_WALK_PLAN.md`): scaffold `vesper-circular-recovery` (PAD first) → `pointers.py` → wire `hybrid_memory_pipeline.py` + `stage_jsonl_compiler.py` into **one local CLI**. Leave Gmail bus, Iron Pearl, visual regen, and the 1.3 GB JSON off the queue.

## 5. Recommended libraries

Merged from `PYTHON_LIBS_RECOMMENDATIONS.md`, `02_LINKAGE_TO_SKILLS_TASKS_GOALS.md`, `requirements-circular.txt` (both copies), and `sources/last spark additional instructions.txt`.

### Must-have for giant Grok JSON

| Lib | Why |
|-----|-----|
| **ijson** | Stream `prod-grok-backend.json`. This is the replacement for `json.load`. Version A (Spine-First) already specifies ijson / C-based streaming. |
| **orjson** | Fast parse of *already-split* shards, not the monolith. |
| **jsonlines / py-jsonl + jsonl-resumable** | Daily shards; byte-offset resume for Nuclear Vacuum–length runs. |
| **pydantic v2** | Envelope, PADVector, PointerRecord, ManifestEntry. |
| **semchunk** | Default Pass 2 (512-token, token-aware). |
| **chonkie** | Spark/last-spark pick: Semantic Double-Pass + Late Chunking, ~33× LangChain; embed in `extractor_engine.py`. |
| **tiktoken** | Token counts that match the 512 / 1k–2k targets. |
| **pypeln** | Concurrent sieve stages. |
| **vaderSentiment** (+ NRC-VAD lexicon data, optional AffectToolbox) | Pass 3 PAD without a GPU. Transformers emotion model only if already in stack. |

### Rest of the circular loop

```
google-api-python-client + google-auth-oauthlib   # Drive + Gmail
python-frontmatter                                # manifests
fsspec / panpath / PyFilesystem2                  # local + Drive + future Box as one path
dlt                                               # when landing queryable lake tables
chromadb (local) or qdrant-client (local)         # package-scoped atom clouds
watchdog                                          # auto update_manifest.py
typer                                             # CLI
```

Last-spark ETL add-ons (not required for first loop): Universal AI Chat Exporter / revivalstack exporter for extract; **Docling** for PDFs/Keep checklists; mcp-proxy + mcp-gateway + agentskills.io SKILL.md for Grok↔Gemini tool-surface normalization (out of ingest scope).

Minimal first loop (Python-libs rec §6 + current `importing/requirements-circular.txt`):

```
ijson, orjson, semchunk, chonkie, tiktoken, jsonlines,
pydantic, python-frontmatter, pypeln, vaderSentiment, typer,
google-api-python-client, google-auth-oauthlib, fs, fsspec
```

## 6. What NOT to do

1. **Do not `json.load()` `sources/grok_archive_split/Copy of prod-grok-backend.json`.**  
   Size on disk ≈ **1.33 GB** (1,398,062,075 bytes). It is already JSON, not a zip. `json.load` materializes the whole tree in RAM and will OOM a G9 Mini / ThinkPad / Jetson. `grok_vps_ingest_engine.py` currently does exactly this (`data = json.load(f)` at line 67) — treat that as a **known defect**, not a recipe. Stream with **ijson** (or split first with `compress_and_chunk_grok_export.py` / `grok_splitter.py` on a machine with enough RAM *once*, then work only on day shards).

2. **Do not unzip / “unpack” that file.** `AGENTS.md`, `index/entries/grok_archive_split.md`, and the walk plan: “Not an archive. Leave packed as JSON.”

3. **Do not open it casually.** Map object `grok-archive-json` is parked. Walk plan: leave the 1.3 GB JSON off the grok-build CLI queue. `map/CONTEXT.md`: do not open unless explicitly ordered.

4. **Do not run the sieve on the monolith.** Chronological-split *first* (or stream-split), then Pass 1–3 per day shard. Early success required Gmail-bypass + hardcoded segments because of Drive MIME / size limits (`MEM_INGESTION_REFERENCE`).

5. **Do not naive-character-chunk.** Frankenbride / last-spark / 2025-10-28 all require semantic / turn-aware leaves.

6. **Do not skip PAD + consent** on the envelope. Pass 3 is not optional.

7. **Do not use ephemeral cloud sandboxes** as the ingest host. April 2026 finding: ChatGPT-class sandboxes fail on multi-file persistent local JSON. Local `ingest.py` / VPS / G9.

8. **Do not invent stages.** Recovered ranking only: Marty Set #1, Nuclear + local JSON→MD #2, ChronologyArc #3. A–F lossless pipelines (Spine-First, Geo-Timeline, Sieve-Quarantine, Edge Skinny Phase-0, OTR Cab, Adapter Hub) are July descendants, not competing roots.

9. **Do not send Gmail-as-MCP bus, Iron Pearl, or locked visual regen** as the first ingest job.

10. **Do not drop cold storage.** Dual non-lossy outputs (raw cold + human-readable) plus SHA-256 reconstitution (strategies A–F) are the preservation guarantee.

## 7. Continuous pipeline (the spine to implement)

```
xAI / Grok export  (prod-grok-backend.json — STREAM, do not json.load)
        ↓
0. Chronological Split + Multi-Day Full Replica
   grok_splitter.py / (fixed) grok_vps_ingest_engine.py  via ijson
   YYYY_MM_Month / Week_WW / YYYY-MM-DD /
        ↓
1–3. 3-Pass sieve  (2025-10-28 root; hybrid / Frankenbride add Pass 4)
   Pass 1 Noise (regex / VTT)
   Pass 2 Semantic leaves ~512t  (semchunk or chonkie)
   Pass 3 Domain + PAD + consent + 20-axis
   Pass 4 Universal Envelope v2.0 → Stage JSONL
        ↓
4. Dual non-lossy outputs
   cold_storage/   human_readable/
        ↓
5. Index
   filesystem chronology  +  pinned-ID registry  +  homogenized JSONL
        ↓
6. Promotion / gate  (later)
   dual-gate, essence score, quarantine, Stage JSONL as SSoT
        ↓
7. Hydrate
   Letta silos (core / voice / ops / archival)
   + dreaming compaction (SQLite WAL → cold-lake shards + receipts)
   + optional chromadb / Qdrant / Obsidian / atom_search
   + A–F SHA-256 reconstitution
```

Lineage (do not reorder):

```
2025-10-28  3-pass + triad + chronological shards
Dec 2025    ChronologyArc offline ETL (spaCy, ThinkPad zero-egress, canon gate)
Jan 2026    Local JSON→MD (chunk/overlap, spaCy/VADER/HF)
Feb 2026    etl_nuclear_vacuum_v0.py (backward-first, emotion, MONOLITHIC, G9)
Feb–Apr     Marty Set (4 phases, entropy, JSON-L, Valerie red-team)
Mar–Apr     Memory Palace concept; UNIVERSAL_MINING_STATE_MACHINE_V2→V6
Jun 2026    Universal Envelope + Multi-Day Full Replica spec
Jul 2026    unified_grok_ingestion.py / grok_splitter.py / A–F lossless
Aug 2026    hybrid_memory_pipeline.py + stage_jsonl_compiler.py + dreaming daemon
```

## 8. Sources read

- `importing/extracted/2026-08-16_python-libs-circular-full/.../PYTHON_LIBS_RECOMMENDATIONS.md`
- `importing/extracted/2026-08-16_python-libs-circular-full/.../02_LINKAGE_TO_SKILLS_TASKS_GOALS.md`
- `importing/extracted/2026-08-16_python-libs-circular-full/.../requirements-circular.txt`
- `importing/extracted/2026-08-16_mining-packages_system-roadmap/conversation-analysis-ideas-2026-drive/MINING_LOG_DRIVE.md`
- `importing/extracted/2026-08-16_mining-packages_system-roadmap/conversation-analysis-ideas-2026-drive/SYNTHESIS_MEMORY_PRESERVATION_2026-08-16.md`
- `importing/extracted/2026-08-16_COMPLETE_FOR_VESPER/conversation-analysis-ideas-2026-drive/SYNTHESIS_DRIVE_TEMPORAL_2026-08-16.md`
- `importing/extracted/2026-08-16_mining-packages_system-roadmap/etl-xai-export-designs-2026/{MINING_LOG,COMPARATIVE_SUMMARY,SYNTHESIS_2026-08-16}.md`
- `importing/extracted/Olivia_Vesper_Gmail_Bus_Session_2026-08-14/.../grok_vps_ingest_engine.py`
- `importing/sources/last spark additional instructions.txt`
- `importing/x/07/memory_ingestion_pipeline/hybrid_memory_pipeline.py`
- `importing/x/08/vesper_frankenbride_ingestion_2026-08-16/{stage_jsonl_compiler.py,README.md}`
- `importing/x/09/mining_packages/workspace-multi-hop-sweep-2026-08-16/{LETTA_DECOUPLED_PIPELINE_SPEC.md,PAD_EMOTIONAL_MODEL_EVIDENCE.md}`
- `importing/GROK_BUILD_WALK_PLAN.md`
- `importing/AGENTS.md`, `importing/requirements-circular.txt`, `importing/index/entries/grok_archive_split.md`

**Absolute Liv HUB claim.**

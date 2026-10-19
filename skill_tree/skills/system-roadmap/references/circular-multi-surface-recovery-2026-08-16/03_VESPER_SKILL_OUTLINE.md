---
title: Vesper Multi-Store Circular Search Skill Outline
date: 2026-08-16
status: design for Spark
---

# Vesper Skill Outline — Multi-Store Circular Recovery

## Purpose
Give Vesper (Gemini Spark) a first-class, parallel capability to the Olivia rock-heavy / topic-search system, specialized for the stores only she can reach cleanly: **Gmail**, **Google Keep**, and her own Drive views of the shared archives.

## Suggested skill name
`vesper-circular-recovery` (or `spark-multi-store-search`)

## Core commands / modes

### 1. `seed-from-olivia <package-or-SEED_FOR_VESPER.md>`
- Ingest the hit list and primary source IDs Olivia already found.
- Do **not** re-search what is already confirmed unless asked.
- Focus on delta and confirmation.

### 2. `multi-hop-gmail <subject> [--since YYYY-MM-DD] [--labels ...]`
- Thread-aware, date-aware, label-aware Gmail search.
- Prefer chronological or backward-first when the subject is historical (e.g. 2025-10-28).

### 3. `multi-hop-keep <subject>`
- Search notes + labels in Keep.
- Especially useful for early schema sketches and hormone / PAD notes that never made it into Drive.

### 4. `multi-hop-drive <folder-id-or-name> <subject>`
- Parallel to Olivia’s Drive Scout, but using Vesper’s native tools and any extra permissions.

### 5. `confirm-and-delta`
- Compare against the latest Olivia MINING_LOG / hit list.
- Emit:
  - CONFIRMED (shared)
  - OLIVIA_ONLY
  - VESPER_ONLY
  - CONFLICTS (if any)

### 6. `union-synthesis`
- Produce a short UNION_SYNTHESIS.md that both sides can absorb.

## Output contract (must match Olivia side)

Every leg writes:
- Timestamped entry in a MINING_LOG_VESPER.md (or CONFIRMATION_LOG.md)
- Source IDs (Gmail msg ID, Keep note ID, Drive file ID)
- Novelty / confidence / thoroughness / circularity metrics (same four as Olivia)
- Clear authorship tag: `author: Vesper / Gemini Spark`

## First test
Subject = **PAD vectors + 2025-10-28 3-pass sieve**

Seeds Olivia will supply:
- Task Ingestion Plan.md file ID
- XAI_Memory_Ingestion_Artifacts_v1 folder ID
- Conversation ID of the Feb 22 2026 Letta PAD discussion
- The PAD_SEARCH_SUMMARY_2026-08-16.md just produced

Vesper returns anything that expands the scoring formula, the exact envelope schema, or any Keep notes that never reached Drive.

## Relationship to existing work
- Pairs with Olivia’s topic-search module and mining-package-template (SR-WQ-018).
- Uses the two-way pointer library (SR-WQ-021+) for every publish.
- Feeds the unified export + letter-ingestion pipeline that was requested in the earlier Vesper briefing.

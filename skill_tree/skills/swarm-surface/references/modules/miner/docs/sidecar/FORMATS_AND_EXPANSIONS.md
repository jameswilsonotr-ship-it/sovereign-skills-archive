# Sidecar Formats + Helper Expansions — Wired Reference

**Status**: Active wiring document (2026-07-20)  
**Purpose**: Single place that ties the formal schema, the four note formats, and the six helper expansions together so the skill can load them as a coherent unit.

---

## 1. Note Formats (from SIDECAR_NOTE_SCHEMA.md)

Every sidecar note must declare one of:

| Format     | Primary Use                          | Key Characteristics |
|------------|--------------------------------------|---------------------|
| `standard` | Default human review & aggregation   | Full fields, readable Markdown |
| `compact`  | High-volume runs                     | Drops low-value prose fields |
| `detailed` | Complex or high-stakes discoveries   | Adds evidence_quotes + related_topics |
| `machine`  | Downstream automation                | Strict key-value / JSON-friendly |

Validation and error-correction rules are defined in `SIDECAR_NOTE_SCHEMA.md` and must be applied before aggregation.

## 2. Helper Expansions (from MARKDOWN_TO_SEARCH_TERMS_HELPER.md)

These are now considered first-class extension points of the conversion helper:

1. **Topic Weighting** — `[weight: high|medium|low]` influences term count/strength.
2. **Negative / Exclusion Terms** — explicit include/exclude lists per topic.
3. **Agent Affinity Hints** — `[agent: slug]` steers which agent receives the topic.
4. **Alias / Variant Expansion** — automatic generation of common term variants.
5. **Confidence-Aware Generation** — when source is a sidecar list, use recorded confidence.
6. **Dry-Run / Diff Mode** — show proposed changes before overwriting any payload.

## 3. Loading Order Inside Swarm-Miner

When the skill needs sidecar or conversion behavior it should load in this order:

1. `docs/sidecar/SIDECAR_NOTE_SCHEMA.md` (authoritative field & validation rules)
2. `docs/sidecar/FORMATS_AND_EXPANSIONS.md` (this file — human-readable index)
3. `docs/MARKDOWN_TO_SEARCH_TERMS_HELPER.md` (conversion rules + expansions)
4. Any active payload under `payloads/stored/`

## 4. Implementation Notes (Current State)

- Schema and format selector are defined and documented.
- Expansion ideas are recorded and ready for progressive implementation.
- No runtime code yet enforces the format selector or the expansions; that is the next engineering layer.
- Research notes (including Grok Heavy findings) live under `research/` and are cited with timestamps.

This document exists so that a new conversation can instantly see what has been wired conceptually even before the executable enforcement is complete.

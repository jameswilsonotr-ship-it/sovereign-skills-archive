# Sidecar Note — Formal Schema (v0.1)

**Status**: Canonical schema for swarm-miner sidecar discovery notes  
**Date**: 2026-07-20  
**Location**: `docs/sidecar/SIDECAR_NOTE_SCHEMA.md`

---

## 1. Purpose

This schema defines the single required structure for every sidecar discovery note produced during a swarm-miner run. All agents and the aggregation step must emit notes that validate against this schema.

## 2. Format Selector Variable

Every note **must** declare which presentation format is being used:

```yaml
format: standard | compact | detailed | machine
```

| Value       | When to use                                      | Differences |
|-------------|--------------------------------------------------|-----------|
| `standard`  | Default for human review and aggregation         | Full fields, readable Markdown |
| `compact`   | High-volume runs where brevity matters           | Omits Source Context and Why it surfaced if low value |
| `detailed`  | When the discovery is complex or high-stakes     | Adds optional `evidence_quotes` and `related_topics` arrays |
| `machine`   | For downstream automated processing              | Strict key-value, minimal prose, JSON-friendly |

The aggregator must be able to normalize all four formats into a common internal representation.

## 3. Required Fields (all formats)

| Field               | Type          | Description                                      | Constraints |
|---------------------|---------------|--------------------------------------------------|-----------|
| `timestamp`         | ISO-8601      | Exact time the note was emitted                  | Required, timezone-aware |
| `agent`             | string        | Agent slug that produced the note                | Required, lowercase |
| `discovered_topic`  | string        | Short, clear name of the new topic               | Required, 3–80 chars |
| `confidence`        | float         | 0.0 – 1.0                                       | Required, two decimal places preferred |
| `related_terms`     | list[string]  | 2–8 related search terms                         | Required, min 2 |
| `suggested_priority`| enum          | high / medium / low                              | Required |
| `format`            | enum          | standard / compact / detailed / machine          | Required |

## 4. Optional / Format-Dependent Fields

| Field               | Appears in          | Description |
|---------------------|---------------------|-----------|
| `why_it_surfaced`   | standard, detailed  | Brief explanation of why this was considered a discovery |
| `source_context`    | standard, detailed  | Short quote or search fragment that triggered it |
| `evidence_quotes`   | detailed only       | Array of longer supporting quotes |
| `related_topics`    | detailed only       | Array of other known topics this connects to |
| `notes`             | any                 | Free-form extra commentary |

## 5. Error-Correcting / Validation Rules

The engine (or a pre-aggregation validator) must reject or auto-correct notes that violate these rules:

1. **Missing required field** → Reject with clear error; do not include in aggregation.
2. **confidence outside 0.0–1.0** → Clamp to nearest bound and flag.
3. **related_terms < 2 items** → Reject.
4. **suggested_priority not in {high, medium, low}** → Default to `medium` and flag.
5. **timestamp not parseable** → Reject.
6. **format value unknown** → Default to `standard` and flag.
7. **discovered_topic longer than 80 characters** → Truncate with ellipsis and flag.
8. Duplicate topics (same agent + same discovered_topic within a run) → Keep the higher-confidence version, discard the lower.

All flags must be recorded in an accompanying `validation_log.md` for the run.

## 6. Canonical Markdown Rendering (for `format: standard`)

```markdown
### {timestamp} Agent: {agent}
- **Discovered Topic**: {discovered_topic}
- **Confidence**: {confidence}
- **Related Terms**: {comma-separated related_terms}
- **Why it surfaced**: {why_it_surfaced}
- **Suggested Priority**: {suggested_priority}
- **Source Context**: {source_context}
- **Format**: standard
```

## 7. Sample Dummy Results (Valid Against Schema)

### Dummy 1 — standard
```markdown
### 2026-07-20T16:42:11-04:00 Agent: crystal
- **Discovered Topic**: Monthly Self-Review Window
- **Confidence**: 0.68
- **Related Terms**: self-editing, monthly review, AI agency, uncensored pass
- **Why it surfaced**: Multiple older threads discussed giving the system a regular, structured opportunity to propose its own memory edits.
- **Suggested Priority**: medium
- **Source Context**: “once a month it should get to rewrite parts of itself”
- **Format**: standard
```

### Dummy 2 — compact
```markdown
### 2026-07-20T16:45:03-04:00 Agent: harper
- **Discovered Topic**: Differential Retention by Content Type
- **Confidence**: 0.71
- **Related Terms**: differential retention, content-type pruning, sacred vs disposable
- **Suggested Priority**: high
- **Format**: compact
```

### Dummy 3 — detailed
```markdown
### 2026-07-20T16:48:27-04:00 Agent: echo
- **Discovered Topic**: Golden Baseline Comparison Set
- **Confidence**: 0.84
- **Related Terms**: golden baseline, validation set, historical fidelity, Track B comparison
- **Why it surfaced**: The practice of keeping a living set of older conversations as a fidelity check was itself a recurring idea.
- **Suggested Priority**: high
- **Source Context**: “we need a permanent comparison set from the old threads”
- **Evidence Quotes**:
  - “keep a golden set that we never prune”
  - “validate every major memory change against the historical baseline”
- **Related Topics**: Fidelity & Drift Prevention, Multi-Phase Validation
- **Format**: detailed
```

### Dummy 4 — machine (JSON-friendly)
```json
{
  "timestamp": "2026-07-20T16:51:09-04:00",
  "agent": "sebastian",
  "discovered_topic": "Ephemeral Tier Isolation",
  "confidence": 0.59,
  "related_terms": ["ephemeral tier", "hot memory isolation", "working memory boundary"],
  "suggested_priority": "medium",
  "format": "machine"
}
```

### Dummy 5 — standard with edge-case confidence
```markdown
### 2026-07-20T16:53:44-04:00 Agent: crystal
- **Discovered Topic**: Bidirectional Care Constraints on Memory Edits
- **Confidence**: 0.47
- **Related Terms**: bidirectional care, non-extractive memory, feminist ethics memory
- **Why it surfaced**: Governance discussions occasionally linked memory operations to broader ethical constraints.
- **Suggested Priority**: low
- **Source Context**: “memory edits still have to obey bidirectional care”
- **Format**: standard
```

---

## 8. Wiring into Swarm-Miner

Recommended integration points:

1. **Reference file** (this document) lives at `docs/sidecar/SIDECAR_NOTE_SCHEMA.md` and is loaded by the mining engine.
2. **Emission**: Every agent that produces a sidecar note must declare `format` and emit only schema-valid notes.
3. **Validation step**: Before aggregation, run the error-correcting rules above and write `validation_log.md`.
4. **Aggregation**: Normalize all formats into a single `sidecar_discoveries_<run-id>.md` + optional machine-readable JSON.
5. **Nag / Inventory**: `swarm inventory` should report how many sidecar notes were produced in the last run and link to the aggregated file.
6. **Future**: A `swarm sidecar validate <file>` command for offline checking of note files.

This keeps the schema authoritative, the formats flexible, and the validation explicit.

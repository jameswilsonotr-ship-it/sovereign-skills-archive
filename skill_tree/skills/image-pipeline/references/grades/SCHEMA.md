# Platonic Grade Artifacts — Schema (IP-WQ-034)

**Status**: LOCKED 2026-08-13  
**Store root**: `references/grades/`  
**Tracks**: `generate/` and `overlay/` (never mixed)

## Record

```json
{
  "id": "grade-YYYYMMDD-HHMMSS-<short>",
  "engine": "generate | overlay",
  "pack_ids": ["implication.anime-glam-kinky-internet"],
  "character_ids": ["olivia", "bunny"],
  "artifact_id": "ZPl5g",
  "prompt": "full prompt text",
  "scores": {"dna": 0.0, "pose": 0.0, "outfit": 0.0, "overall": 0.0},
  "tingly": "yes | no | meh",
  "emit_without_generate": "pass | fail",
  "reasoning": "why this grade matters",
  "outlier": false,
  "created_at": "ISO8601"
}
```

## API
`scripts/grade_store.py` — `add` / `list --engine generate|overlay [--outliers]`

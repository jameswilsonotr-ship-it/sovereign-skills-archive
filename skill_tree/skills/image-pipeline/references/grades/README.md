# Platonic Grade Artifacts (IP-WQ-034)

- Schema: `SCHEMA.md`
- Writer: `scripts/grade_store.py`
- Tracks: `generate/`, `overlay/` (never mixed)

```bash
python scripts/grade_store.py add --json '{"engine":"generate","pack_ids":["implication.manara"],"artifact_id":"x","scores":{"overall":8.5},"emit_without_generate":"pass"}'
python scripts/grade_store.py list --engine generate
```

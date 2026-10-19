# skill-orchestrator scripts

| Script | Role | Inventory home |
|--------|------|----------------|
| `inventory_scripts.py` | Scan all skills for scripts | `references/inventory/scripts/` |
| `search_scripts.py` | Keyword search over script bodies + docstrings | stdout / `--json` |
| `audit_references_completeness.py` | SKILL.md paths vs disk + stubs | `references/inventory/completeness/` |
| `emit_stale_facts.py` | 7-day inactivity STALE_FACT lines | `completeness/stale_facts_latest.json` |
| `package_skills.py` | Tarball / publish helper | — |
| `discipline_check.py` | Folder discipline checks | — |
| `library_export.py` | Library export | `inventory/export_*` |
| `diagram_skill_structure.py` | Structure diagrams | — |
| `on_skill_change.py` | Hook helper | — |
| `migrate_image_pipeline_pack.py` | One-shot migration | — |

Auditing pair (completeness + stale) and scripts inventory share the **registry + schema + latest** pattern under `references/inventory/`.

## wq_bidir.py (SR-WQ-042)
System-wide depends_on ↔ blocks scan + optional --fix. Writes BIDIR_REPORT.json under work-queue-surface.
```
python3 wq_bidir.py
python3 wq_bidir.py --fix
```

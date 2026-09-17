# OpenSpec matrix

Generated from `docs/openspec/*.md` by `scripts/gen_openspec_matrix.py`.

| id | title | status | owner | priority | summary | tags | dependencies | requirements | acceptance | checklist_total | checklist_done | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| api-rate-limits | API rate limits | proposed | platform | high | Add predictable per-client request limits to the public API. | api; reliability | auth-service | 2 | 2 | 2 | 0 | docs/openspec/api-rate-limits.md |
| cli-export | CLI export command | accepted | developer-experience | medium | Provide a machine-readable export command for local project data. | cli; export | config-loader; filesystem | 3 | 3 | 3 | 2 | docs/openspec/cli-export.md |
| SPEC-017-OFFLINE-CI | Offline pytest CI | proposed | quality-engineering | high | Make the required pytest burn deterministic and fail-closed when CI has no network. | ci; pytest; offline; reproducibility | pytest; test-fixtures | 15 | 15 | 15 | 0 | docs/openspec/SPEC-017-OFFLINE-CI.md |

# Strategy 5 — Context Store Skills + Python CLI (Vesper / Valerie style)

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Concrete skill + scripts already exist on Drive and local mirrors  
**Primary sources**: Vesper Context Store skill (SKILL.md, cli.py, ingest_context.py, manifest_manager.py), Valerie Context Store parallel structure, git_staged_trees folders

## Core Idea
Per-organism local-first skill that owns the full cycle: ingest → query → manifest → SHA256 content-addressed storage → Git readiness. Categories are partitioned (telemetry / taskops / git_staged_trees for one; governance / contracts / ssot_ledgers for the other). Pure Markdown only; no Google Docs conversion. Designed so each organism can maintain its own normalized local view while remaining Git-ready for publish.

## Key Elements Captured
- Python CLI surface (ingest, query, manifest)
- SHA256 CAS
- Obsidian-friendly Markdown
- Partitioned categories per organism
- Ready for Git commits / staged trees

## Notes from Recon
This is a fully realized local normalization surface that can serve as the offline implementation of the Canonical Lake promotion contract or as the local side of the Drive Staging pipeline. Parallel stores (Vesper vs Valerie) introduce a coordination requirement if they are to stay consistent.

No de-duplication or merging performed.

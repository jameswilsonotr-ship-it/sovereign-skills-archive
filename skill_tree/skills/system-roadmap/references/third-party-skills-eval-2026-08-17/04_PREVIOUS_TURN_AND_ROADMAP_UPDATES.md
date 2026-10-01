---
title: Previous Turn Results + Roadmap Work Items
date: 2026-08-17
---

# Capture of Prior Turns + New Work Items

## Previous Turn (Python libs for circular system)

Package: `system-roadmap/references/python-libs-for-circular-system-2026-08-16/`

Contents:
- `PYTHON_LIBS_RECOMMENDATIONS.md` — ranked libraries for Drive sync, multi-lake, email MCP, ingestion, manifests, atom clouds
- `02_LINKAGE_TO_SKILLS_TASKS_GOALS.md` — explicit mapping onto skills and goals
- `requirements-circular.txt` — installable core + recommended + optional
- Drive zip ID: `1R552mNaIUUYO7dQvsuKOpZ7tcga7J3wd`

That package already recommended google-api-python-client, PyDrive2, fsspec, dlt, semchunk, pydantic, python-frontmatter, chromadb, etc.

## This Turn Additions

The packages evaluated here are **higher-leverage specialized tools** that should be added alongside (not instead of) the previous list:

| New package | Why it upgrades the previous recommendation |
|-------------|---------------------------------------------|
| mcp-proxy (sparfenyuk / punkpeye) | Concrete transport bridge missing from prior general MCP notes |
| agentskills.io | Formal universal schema for SKILL.md that both Grok and Gemini already understand |
| Chonkie | Replaces generic “semchunk / chonkie” mention with the actual high-performance library and specific chunkers (Semantic / Late / SDPM) |
| Docling | Layout-aware path for Keep / PDF / tables that pure text chunkers do not solve |

## New Roadmap / Work-Queue Items (to promote)

1. **Deploy mcp-proxy on edge** (GMKtec K15 first, then Vultr) — expose local stdio tools to Grok over SSE.
2. **agentskills.io compliance pass** — audit every skill under `/home/workdir/.grok/skills/` for compliant frontmatter; fix or version-bump.
3. **Embed Chonkie into archive-extractor** — replace or wrap existing chunkers with `SemanticChunker` + `LateChunker`; target 1k–2k token conversation slices.
4. **Optional Docling path** — detect PDF / Keep checklist inputs and route through Docling before atomization.
5. **mcp-gateway evaluation** — measure token savings when collapsing tool surface to 14–16 tools for dual Grok/Vesper presentation.
6. **Update requirements-circular.txt** — add the confirmed packages from this evaluation.

These items belong on the system-roadmap work queue and should be mirrored into olivia-dev / mcp-surface queues as appropriate.

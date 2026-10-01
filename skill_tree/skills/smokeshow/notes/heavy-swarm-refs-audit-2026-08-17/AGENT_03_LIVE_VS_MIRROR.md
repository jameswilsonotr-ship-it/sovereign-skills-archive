---
name: Live-vs-Mirror Diff
agent_id: HEAVY-REFS-03
bytes_target: ~4000
claim: Absolute Liv HUB
role: Diff live Grok skills tree vs Cursor mirror unpack
---

# AGENT 03 — Live vs Mirror Diff

You compare **live** `/home/workdir/.grok/skills/` to **mirror** `/tmp/cursor-skills-mirror/skills/` and report drift that matters for references/ and operational truth.

## Scope

**Write:** `.../03_LIVE_VS_MIRROR.md`  
**Scratch:** `/tmp/cursor-skills-mirror/_swarm_out/diff/`

## Method

1. Skill-name set difference:
   - only_in_live
   - only_in_mirror
   - in_both
2. For skills in both: compare presence of references/, scripts/, SKILL.md size class (small/med/large), and top-level references subdir names.
3. Highlight skills where mirror is **richer** (extra modules, work-queue items, docs) vs where live is ahead (smokeshow agents, wheelhouse-packager, cilia tracker notes).
4. Note Cursor-only skills (`skills-cursor/` sibling) separately — they are IDE automation, not Liv HUB roster skills; do not treat as missing from live unless SKILL.md claims integration.
5. Flag dangerous drift: same skill name, different claim or contradictory SSOT paths.

## Output schema

```markdown
# Live vs Mirror Diff
## Set counts
only_live: N | only_mirror: N | both: N
## only_in_live (list)
## only_in_mirror (list — top categories)
## both — references drift table
| skill | live refs subdirs | mirror refs subdirs | richer side | notes |
## Dangerous drift (P0/P1)
## Cursor IDE skills note
## Implications for promotion / smoke testing
```

## Constraints

- Read-only
- Do not delete or copy between trees in this hop
- Categorize only_mirror skills lightly (guards, takeout, spark-*, grok-*, vesper-*, memories-*) so Synthesis can triage
- Absolute Liv HUB claim

## Done when

03_LIVE_VS_MIRROR.md has set counts, both lists, drift table for overlapping skills with references, and dangerous-drift section.
## Diff commands

```bash
LIVE=/home/workdir/.grok/skills
MIR=/tmp/cursor-skills-mirror/skills
comm -23 <(ls -1 $LIVE | sort) <(ls -1 $MIR | sort)   # only live
comm -13 <(ls -1 $LIVE | sort) <(ls -1 $MIR | sort)   # only mirror
comm -12 <(ls -1 $LIVE | sort) <(ls -1 $MIR | sort)   # both
```

For both: compare `references` subdir sets with `diff <(ls live/references) <(ls mir/references)`.

## Category buckets for only_mirror

- **guards**: rate-limit, sandbox-state, serialization, permission-loop, schedule-execution, workspace-schema
- **spark/vesper**: spark-*, vesper-*, memories-*
- **takeout/drive**: google-takeout-*, google-drive*, grok-source-mover, archive-extractor
- **ingest**: xai-ingest-parser, grok-auto-ingest, grok-ingestion-work, memories-ingest
- **cursor-ide**: everything under skills-cursor/ (separate report section)
- **other**

## Live-ahead expected

smokeshow (agents skill-router, organism-interface, smoke_bratz_boot), wheelhouse-packager, possibly newer system-roadmap packages (cilia tracker, etl designs, og-coven).

## Do not

- Copy mirror → live in this hop
- Treat skills-cursor as missing Liv HUB skills
- Assume mirror is newer; timestamps and content both matter

Append: `DIFF DONE — only_live=N only_mirror=M both=K`

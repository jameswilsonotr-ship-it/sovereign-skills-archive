# Global Conversation + Sandbox Extract Protocol
**Version**: 1.0.0  
**Added**: 2026-08-05  
**Skill**: grok-conversation-miner

## Purpose
Produce one comprehensive, self-contained package that captures everything meaningful from the current conversation and its side-effects:
- Conversational flow, handoffs, and key decisions
- Sandbox / artifacts state
- Markdown and other files written during the session
- Skill-tree delta (queues, extensions, new files, pointer files)

This is the “one button → everything that happened is in one archive” command.

## Triggers
- `global extract`
- `grok conversation miner global extract`
- `full sandbox extract`
- `package everything from this conversation`
- `conversation + artifacts + skill delta`
- `comprehensive miner package`

## Execution Steps

1. **Conversation layer**
   - Run (or reuse results from) General Conversation Deep Mining / Vacuum logic.
   - Collect all handoff blocks, consolidation summaries, and explicit decisions.
   - Write `conversation/full_flow.md` (or structured equivalent) and `conversation/key_decisions.md`.
   - Copy any handoff markdown into `conversation/handoffs/`.

2. **Sandbox / Artifacts layer**
   - Snapshot `/home/workdir/artifacts/` (or a sensible filtered subset if extremely large).
   - Place under `sandbox/artifacts/`.
   - Note any other session-written files that live outside artifacts.

3. **Written markdown / skill delta layer**
   - Identify skills and files that were created or modified in the relevant time window.
   - Prioritise:
     - image-pipeline (extensions, queues, taxonomy audits, CHANGELOG)
     - chaos-bratz-roster (work queues, DNA_LOCKS, identity locks, Memory track)
     - format-bible
     - olivia-dev-alpha (especially ACTIVE_WORK_QUEUES.md)
     - any other skill touched by the conversation
   - Copy the changed files into a mirrored `skill_delta/<skill-name>/` tree.
   - Also collect every current `WORK_QUEUE.md` + `HANDOFF_STATUS.md` into `queues_snapshot/`.

4. **Manifest**
   - Write `MANIFEST.md` containing:
     - Timestamp
     - Conversation ID / description
     - List of included top-level directories
     - High-level summary of what was captured
     - Any exclusions (e.g. real-world logistics deliberately omitted)

5. **Package & Publish**
   - Create a versioned directory:
     `global-extract_vX.Y.Z_YYYY-MM-DD_HHMM/`
   - Tar.gz the entire tree.
   - Publish via the existing Standard Active Chat Publishing / Drive protocol.
   - Respect the hard safety gate (binary/large payloads → Drive only, never GitHub Contents API).

## Output Tree (canonical)

```
global-extract_vX.Y.Z_YYYY-MM-DD_HHMM/
├── conversation/
│   ├── full_flow.md
│   ├── key_decisions.md
│   └── handoffs/
├── sandbox/
│   └── artifacts/
│       └── sunset/          # L7 outbox cards when present (GCM-WQ-003)
├── skill_delta/
│   ├── image-pipeline/
│   ├── chaos-bratz-roster/
│   ├── format-bible/
│   ├── olivia-dev-alpha/
│   └── …
├── queues_snapshot/
│   ├── image-pipeline_WORK_QUEUE.md
│   ├── roster_WORK_QUEUE.md
│   └── …
└── MANIFEST.md
```

## Notes
- Real-world logistics (RTI, health, house, bills) stay out of the package unless the user explicitly requests them.
- This command is additive; it does not replace Vacuum Mode or the older publishing commands.
- Prefer completeness over minimalism, but apply sensible size filters if artifacts are enormous.


## L7 outbox (GCM-WQ-003)
If `artifacts/sunset/SUNSET_*.md` exists this run, copy it under `sandbox/artifacts/sunset/`.
If L7 has not been written yet, L4 still ships; L7 writes after L4 and a one-line pointer is appended to MANIFEST.md. No second tar.

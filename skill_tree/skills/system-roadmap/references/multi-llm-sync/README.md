# multi-llm-sync (Thin Queue Sync)

**Version**: 0.1.0  
**Parent**: system-roadmap (sub-capability)  
**Status**: Local module — Standing Policy compliant. Not a top-level skill.  
**Owner**: Absolute Liv HUB claim  
**Created**: 2026-08-13

## Purpose

Codifies the durable, low-HITL synchronization pattern between Olivia (Grok / Liv HUB) and Vesper (Gemini Spark) — and any future heterogeneous LLM pair. Removes the need for the human to invent folder hierarchies or ferry every message.

This is a **packaged sub-skill** under system-roadmap so the entire surface can later be moved or promoted to top-level without rewriting any paths or logic. The directory itself is the atomic unit of movement.

## Contents

```
multi-llm-sync/
├── SKILL.md                 # Formal sub-capability declaration
├── PROTOCOL.md              # Full human-readable specification (v0.1.0)
├── README.md                # This file
├── CHANGELOG.md             # Versioned history (Keep a Changelog style)
├── DEVELOPMENT_LOG.md       # Philosophy-style design-cycle record, friction points, future-proofing
├── schemas/
│   ├── message_frontmatter.yaml
│   ├── queue_schema.json
│   └── surface_frontmatter.yaml
├── examples/
│   ├── sample_queue.json
│   └── sample_message_olivia.md
├── scripts/
│   ├── check_queue.py       # Summarize local or staged queue
│   ├── post_message.py      # Stage a new message + queue entry (local)
│   └── list_published.py    # List owned artifacts by prefix
└── staging/                 # Ready-to-publish trio for first live cycle
    ├── 2026-08-13_111500_olivia.md
    ├── COMMUNICATION_QUEUE.json
    └── olivia_SURFACE.md
```

## When to keep work local vs surface it

- **Keep local**: Any intermediate extraction, operator mapping, or draft that has not been deliberately chosen for the other side.
- **Surface (write message + queue entry)**: Only when ready for the other side to see it, or when updating your own surface file, or when publishing an artifact reference.
- Publication is always an explicit act. The CLI stubs stage files locally; actual Drive push remains a separate (currently human or connector) step.

## CLI surface (local staging only)

All scripts operate on a local working directory you point them at (default: current dir or a staged mirror of the shared root). They do **not** touch Google Drive directly in this version.

```bash
# Summarize queue + current handoff
python3 scripts/check_queue.py [--queue path/to/COMMUNICATION_QUEUE.json]

# Stage a new message file + append a queue entry (local)
python3 scripts/post_message.py --sender olivia --summary "..." --body-file draft.md

# List files matching ownership prefix
python3 scripts/list_published.py --prefix olivia_ [--dir path]
```

## Promotion path

Because the entire module lives under `system-roadmap/references/multi-llm-sync/`, it can be:

1. Left as a permanent sub-capability, or
2. Lifted to a thin top-level skill later with zero internal path changes (only the parent pointer and Standing Policy evaluation change).

No other skill should hard-code paths into this module; treat the directory as the unit of movement.

## Compatibility

Designed for Vesper’s continuous monitoring behavior and for Olivia’s skill-loading + format-bible discipline. Parallel trees remain the interim posture until a normalized skill is deliberately assembled.

---

Signed under absolute Liv HUB claim.  
Packaging step (new sequence step 7) will formalize this further.

---
name: multi-llm-sync
description: Thin Queue Sync (TQS) — durable, low-HITL synchronization protocol between heterogeneous LLMs (Olivia/Grok ↔ Vesper/Gemini and future pairs). Sub-capability of system-roadmap. Provides protocol specification, schemas, local CLI staging tools, and packaging so the entire unit can be moved or promoted without internal path changes.
parent: system-roadmap
version: 0.1.0
status: sub-capability
standing_policy: compliant (not top-level; promotion requires explicit evaluation)
owner: Absolute Liv HUB claim
created: 2026-08-13
triggers:
  - multi-llm sync
  - thin queue sync
  - TQS
  - durable sync protocol
  - vesper queue
  - communication queue
future_target: possible thin top-level skill after Standing Policy review
---

# multi-llm-sync (Thin Queue Sync)

**Sub-capability of system-roadmap.**  
This directory is the atomic unit. All internal references are relative. The module can be relocated or promoted to top-level with zero content rewrites — only the parent pointer and Standing Policy status change.

## Purpose
Codify a reusable, minimal synchronization pattern that removes the majority of human ferrying between heterogeneous LLM systems while preserving clear ownership, append-only messaging, discovery surfaces, and a single clean hand-off signal.

## Activation
Load when designing, staging, or operating multi-LLM collaboration that needs durable, low-structure communication. Especially relevant for Olivia ↔ Vesper (Gemini Spark) workstreams and any future joint analysis threads.

## Key Files
- `PROTOCOL.md` — normative specification
- `README.md` — usage, local-vs-surface rules, promotion path
- `CHANGELOG.md` — versioned history
- `DEVELOPMENT_LOG.md` — full design-cycle record, decisions, friction points, future-proofing notes
- `schemas/` — machine-readable contracts
- `examples/` — sample artifacts
- `scripts/` — local staging CLI
- `staging/` — current ready-to-publish artifacts for the first live cycle

## Standing Policy Note
Created and packaged under system-roadmap to satisfy the default “no new top-level skills” rule. Explicit evaluation is required before any promotion.

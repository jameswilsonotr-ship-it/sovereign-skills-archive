---
title: Four Concrete Extensions for the Drive Swarm Subscale
date: 2026-08-16
status: design-ready-for-test
owner: system-roadmap
package: etl-xai-export-designs-2026-drive
keywords:
  - Drive-swarm
  - extensions
  - parallel-search
  - timeout
  - Vesper
  - topic-search
obsidian_tags:
  - "#Drive-swarm"
  - "#extensions"
  - "#system-roadmap"
---

# Four Concrete Ways to Extend the Drive Swarm Subscale

These four extensions are the practical next steps that turn the open research in `topic-search/docs/FUTURE_RESEARCH.md` into testable work. They are ordered from smallest / safest to larger scope. Collation and final comparison against the conversational-history package remain **out of scope** for the subscale itself.

## 1. Minimal Viable Drive Scout (fastest path)

**Goal**: Prove the write path and basic timeout behavior with a single agent.

- Add / use `DRIVE_SCOUT_BRIEF.md` template (see templates/).
- Inputs: topic (ETL multi-pass lineage), list of Drive folder IDs or path prefixes, optional time window, success criteria, `timeout_seconds`.
- One Scout (Expert or Heavy) walks the listed folders, emits ranked Markdown hits into `DRIVE_HITS/`, appends a short entry to `MINING_LOG_DRIVE.md`, and stops.
- No parallel legs. Success = files land in the sibling package and the log is updated.

**Test value**: Confirms Drive tool reachability, timeout handling, and package hygiene before any multi-agent spend.

## 2. Parallel Folder-Partition Legs (true swarm)

**Goal**: Real multi-leg parallelism over Drive.

- Extend the launch brief so the Chronicler can declare N parallel legs.
- Each leg is scoped to a different Drive sub-tree, date slice, or keyword cluster.
- Each leg writes its own `DRIVE_HITS/leg-N-*.md`.
- Chronicler only records paths + short status; full synthesis stays later.
- Explicit fields: `timeout_per_leg`, `max_total_minutes`, `on_timeout: partial-ok | abort`.

**Test value**: Measures real-world parallelism, partial-result behavior, and credit burn on a known ETL-related Drive tree.

## 3. Serial Fallback + Budget Language

**Goal**: Make thoroughness safe under real limits.

- Add a required `budget` block to every Drive-aware launch brief:

```yaml
budget:
  mode: parallel | serial
  timeout_per_leg: 600          # seconds
  max_total_minutes: 30
  on_timeout: partial-ok | abort
  max_credit_estimate: <optional>
```

- Serial mode runs legs in order when parallel is unsafe or credits are low.
- Partial results are first-class; the package never hangs silently.

**Test value**: Directly addresses the “push the timeout limits for thoroughness” requirement while keeping the package recoverable.

## 4. Optional Vesper Sparse Leg (multi-surface)

**Goal**: Bring chronology / metadata filtering into the same package.

- Optional third surface: Vesper receives the same search schema via the email-first MCP / Drive-drop hand-off.
- Vesper returns sparse or chronology-filtered hits into `DRIVE_HITS/vesper/`.
- Same success criteria and timeout budget language apply.
- No requirement that Vesper run on every package; it is opt-in.

**Test value**: Validates the cross-platform hand-off path and gives a second independent view of the same ETL subject without forcing early collation.

---

## Recommended Test Order (before formal local execution)

1. Extension 1 (single Drive Scout) on a small, known folder.
2. Extension 3 (budget language) applied to the same brief.
3. Extension 2 (two parallel legs) once single-leg is stable.
4. Extension 4 (Vesper) only after the Olivia/Heavy path is reliable.

All results stay inside this sibling package. Comparison with `etl-xai-export-designs-2026/` is a later, separate step.

**Absolute Liv HUB claim.**

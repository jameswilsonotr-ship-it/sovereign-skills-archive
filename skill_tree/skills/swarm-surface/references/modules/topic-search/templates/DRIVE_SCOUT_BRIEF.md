---
title: Drive Scout Launch Brief (Minimal Viable)
date: 2026-08-16
status: template
owner: topic-search
module: swarm-surface/references/modules/topic-search
keywords:
  - Drive-scout
  - launch-brief
  - topic-search
  - Google-Drive
---

# DRIVE_SCOUT_BRIEF — Minimal Viable Drive Scout

**Module**: topic-search  
**Role**: Single Scout (no parallel legs yet)  
**Write target**: `system-roadmap/references/etl-xai-export-designs-2026-drive/`

Copy this template, fill the fields, and hand it to a Scout (Expert surface or Grok Heavy).

```yaml
package_id: drive-scout-etl-YYYY-MM-DD
topic: ETL multi-pass / ingestion / memory-pull pipeline designs for xAI conversation exports
success_criteria:
  - At least N ranked Markdown hits written to DRIVE_HITS/
  - Each hit has: source path or file ID, approximate date if available, short relevance note, link back to ETL stages if possible
  - MINING_LOG_DRIVE.md receives one timestamped entry summarizing the leg
drive_scopes:
  - folder_id_or_path: <REQUIRED — e.g. Conversational_Mining_Payloads or specific export folder>
  - optional_mime_filter: [application/vnd.google-apps.document, text/markdown, application/json]
  - optional_time_window: {from: YYYY-MM-DD, to: YYYY-MM-DD}
budget:
  mode: serial                    # only one leg in this minimal brief
  timeout_per_leg: 600            # seconds — raise for thoroughness
  max_total_minutes: 15
  on_timeout: partial-ok
  max_credit_estimate: null
output:
  hits_dir: DRIVE_HITS/
  log_file: MINING_LOG_DRIVE.md
  package_root: system-roadmap/references/etl-xai-export-designs-2026-drive/
notes: |
  Collation against the conversational-history package is OUT OF SCOPE.
  Partial results are acceptable and preferred over silent failure.
  Do not invent ETL stages; only surface what the Drive documents actually contain.
```

## Scout instructions (short)

1. Confirm write access to the package_root above.
2. Walk the drive_scopes with the given timeout.
3. For every relevant document, emit a short Markdown file into DRIVE_HITS/ using a clear name (e.g. `hit-001-marty-set-notes.md`).
4. Append one entry to MINING_LOG_DRIVE.md in the same format used by the conversational MINING_LOG.
5. Stop when timeout or success_criteria are met. Return the list of files written.

**Absolute Liv HUB claim. Template only — not an execution order.**

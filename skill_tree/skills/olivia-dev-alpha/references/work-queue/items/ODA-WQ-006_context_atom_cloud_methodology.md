---
id: ODA-WQ-006
title: Context Atom Cloud methodology + Obsidian export hygiene
status: OPEN
created: 2026-08-17
updated: 2026-08-17
owner: olivia-dev-alpha
related:
  - SR-WQ-025
  - claim-runtime/curator
tags:
  - methodology
  - atom-cloud
  - obsidian
  - whoop-ass
priority: high
---

# ODA-WQ-006 — Context Atom Cloud methodology + Obsidian export hygiene

## Purpose
Alpha owns the *how* of the new context cloud:

- Exact field order and YAML style so every generated note is Obsidian-clean.
- Whoop-ass gate on any script that writes atoms.
- Explicit link to the existing **porn-curator / claim-runtime atom cloud** so it is never orphaned.
- Lightweight migration / seed script that can be run from any conversation.

## Required outputs
1. Pointer file under `references/integrations/context-atom-cloud/POINTER.md`.
2. Seed generation helper that prints ready-to-save Obsidian notes.
3. Three initial atoms covering tonight’s package work (hardware + VIPEK rack + tarp context).
4. Standing rule: every context atom that references a Drive file must carry a real `drive_file_id`.

## Linkage rule
The curator (porn) atom cloud stays under `claim-runtime/references/modules/curator/atoms/`.  
Cloud D only *references* it; it does not absorb or rewrite those atoms.

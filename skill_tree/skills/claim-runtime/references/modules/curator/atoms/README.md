# Curator Atom Cloud — Session / Canonical Layout

**Status**: live (2026-08-06)  
**Schema**: session uses `0.4.0-session` (owner / excitement / interaction_log / kind)  
**Architecture**: mirrors the main dual-cloud pattern (session-overlay → explicit promote → durable canonical)

## Layout

```
atoms/
├── sessions/                          # working overlays (write here during a conversation)
│   ├── curator_session_atom_cloud_2026-08-06_v0.4.json   ← current rich 32-atom set
│   └── … prior sessions
├── canonical/                         # last promoted good state
│   └── curator_atom_cloud.json
├── schemas/
│   └── CURATOR_ATOM_SCHEMA_0.4_SESSION.md
├── curator_atom_cloud.json            # LEGACY global (591 atoms, older schema) — DO NOT auto-overwrite
├── promote_union.py                   # explicit merge + promote
├── search.py                          # preferred search helper
├── porn_atom_search.py                # older thin search (still works on legacy)
├── manifest.json                      # last promote metadata
└── README.md                          # this file
```

## Rules (non-negotiable)

1. **Write only to session** during active work. Create / update a file under `sessions/`.
2. **Promotion is explicit**. Run `python3 promote_union.py --apply` when the session set is ready to become durable.
3. The legacy top-level `curator_atom_cloud.json` is left untouched unless you pass `--also-legacy` (not recommended until schema migration is complete).
4. Ownership defaults to `olivia`. Only move a concept to `shared` / `bunny` when the user explicitly begs it in.
5. All content remains descriptive potential under RACK + safewords. Execution is consent-gated.

## Promote policy

- Merge by stable `id`.
- Conflict resolution order:
  1. Higher `excitement` wins.
  2. If equal → newer `last_interaction` wins.
  3. If still tied → session atom wins.
- Manifest records counts, source session, and timestamp.

## Search

```bash
# prefers newest v0.4 session, then canonical, then legacy
python3 search.py "feet"
python3 search.py "inflation" --limit 5
python3 search.py "hyena" --session-only
python3 search.py "tattoo" --owner olivia --kind visual_style
```

## How other conversations should use this

- **During a curator session**: append / edit only the current session JSON under `sessions/`.
- **When ready to harden**: run promote_union.py --apply (or dry-run first).
- **For lookup**: always call `search.py` (or import its `search()` function). Never hand-edit the canonical or legacy files.
- Future: align fully to bi-temporal fields (`created_ts`, `promoted_ts`, `geo`) so this cloud shares shape with the main memory + skill_surface clouds.

## Confirmation (2026-08-06)

- 32 session atoms (v0.4 schema) installed and intact under sessions/.
- Initial canonical written from that session (32 atoms).
- Legacy global left untouched.
- Search and promote scripts operational.

---

## Stability roadmap (CR-WQ-001 / 002 / 003)

Formal work lives in the **local claim-runtime work-queue**:

- `claim-runtime/references/work-queue/WORK_QUEUE.md`
- Items: CR-WQ-001 (overall architecture), CR-WQ-002 (per-conv isolation + staged holding), CR-WQ-003 (backups + Drive versioning)

Current gaps that keep the system from being fully stable under concurrent conversations:

1. No conversation-local isolation root yet (everything still lands in `sessions/`).
2. No `staged/` holding queue + manifest that every new curator instance can discover.
3. No automatic pending report on load.
4. No rotating local backups of canonical + no versioned Drive export after promote.

Target four-stage write path (once the WQ items close):

1. Conversation-local → `/home/workdir/artifacts/curator_sessions/<id>.json`
2. Explicit stage → `atoms/staged/` + manifest
3. Explicit promote → `atoms/canonical/`
4. On promote → local backup rotation + Drive versioned copy

Until those land, the current session/canonical/search/promote scripts remain safe for single-conversation use and for the 32-atom seed already promoted.

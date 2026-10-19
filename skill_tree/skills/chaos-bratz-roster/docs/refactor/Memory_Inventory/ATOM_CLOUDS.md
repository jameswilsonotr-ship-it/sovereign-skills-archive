# Atom Clouds — Discovery Index (equal specificity)

**Status**: live  
**Updated**: 2026-08-05  
**Owner**: Memory track / chaos-bratz-roster inventory tooling  
**Schema version**: 0.2.0 (bi-temporal + geo)  
**Architecture**: session-overlay + explicit-promote (durable canonical inside skill)

Any conversation that needs sentence-level search over roster content should know **both** clouds. They are first-class peers.

---

## Durable Canonical vs Session Overlay

| Layer | Location | Role |
|-------|----------|------|
| **Canonical (durable)** | `data/atom_clouds/canonical/` inside this skill | Last-promoted good index. Survives session resets of artifacts/. Never auto-loaded into context. |
| **Session overlay** | `/home/workdir/artifacts/` | Working copies. Regenerated or copied on demand. Preferred by search. |
| **Manifest** | `data/atom_clouds/manifest.json` | Schema version, last_promoted_ts, atom counts. |

**Rules**
1. Generation (atomizers) always writes to artifacts/ (session overlay).
2. Search prefers artifacts/; falls back to canonical if missing.
3. Explicit promote only: `python3 scripts/inventory/promote_clouds.py` copies overlay → canonical and updates manifest. Session-only experiments stay out until promoted.
4. Do not bloat skill load: JSON files are never read into agent context at boot. Only atom_search / promote / explicit tools load them.
5. Source of truth for content remains the markdown under references/; clouds are indexes only.

---

## Cloud A — Memory (durable promoted homes)

| Field | Value |
|-------|-------|
| **Name** | `memory` |
| **Purpose** | Sentence-level ownership of content that used to live in memory.md; drift detection; keep memory.md pointer-only |
| **Scope** | `references/system/` · `personal/` · `visual/` · `hub/` · `archive/` **only** |
| **Script** | `scripts/inventory/memory_atomizer.py` (v0.2) |
| **JSON (session)** | `/home/workdir/artifacts/memory_atomizer.json` |
| **JSON (canonical)** | `data/atom_clouds/canonical/memory_atomizer.json` |
| **Report** | `docs/refactor/Memory_Inventory/reports/atomizer_report.md` |
| **Atoms (2026-08-05)** | 1 629 |
| **Does not include** | agents/, mirrors/, scripts/, queues, docs |

## Cloud B — Skill surface (live skill)

| Field | Value |
|-------|-------|
| **Name** | `skill_surface` |
| **Purpose** | Sentence-level index of the living skill surface for search and ownership hygiene |
| **Scope** | mirrors, agents (read-only), scripts, work-queues, to-do, docs, specs, root SKILL/CHANGELOG/README, layer_manifests, shared |
| **Script** | `scripts/inventory/skill_surface_atomizer.py` (v0.2) |
| **JSON (session)** | `/home/workdir/artifacts/skill_surface_atomizer.json` |
| **JSON (canonical)** | `data/atom_clouds/canonical/skill_surface_atomizer.json` |
| **Report** | `docs/refactor/Memory_Inventory/reports/skill_surface_atomizer_report.md` |
| **Atoms (2026-08-05)** | ~18 269 |
| **Does not include** | the five Memory homes (Cloud A), memory_import/, binaries |

---

## Atom schema (v0.2.0 — bi-temporal)

Every atom now carries these fields:

| Field | Type | Meaning |
|-------|------|---------|
| *(original)* | | home/owner, path, atom_index, atom, char_len |
| `created_ts` | ISO-8601 string or null | Best-effort origin time (file mtime) |
| `promoted_ts` | ISO-8601 string | When this atom entered the cloud (atomizer run) |
| `geo` | string or null | Optional location tag (currently always null) |

Search tools ignore the new fields unless explicitly filtered later. Old atoms that lack the data receive `null`.

---

## Union search (both clouds)

```bash
cd /home/workdir/.grok/skills/chaos-bratz-roster
python3 scripts/inventory/atom_search.py "your query"
python3 scripts/inventory/atom_search.py "query" --cloud memory
python3 scripts/inventory/atom_search.py "query" --cloud skill_surface --owner mirrors
python3 scripts/inventory/atom_search.py "query" --path-prefix references/agents/olivia
python3 scripts/inventory/atom_search.py "query" --canonical-only   # force durable
```

Loads both JSON files (overlay preferred). Filters: `--cloud`, `--owner`, `--path-prefix`, `--limit`.

---

## Promote protocol

```bash
# After a clean generation in the current session:
python3 scripts/inventory/promote_clouds.py
# or dry-run
python3 scripts/inventory/promote_clouds.py --dry-run
```

- Validates JSON structure.
- Backs up previous canonical under `artifacts/atom_cloud_backups/pre_promote_<ts>/`.
- Copies artifacts → `data/atom_clouds/canonical/`.
- Updates `manifest.json`.

Session-only atoms or experimental regenerations are never promoted automatically.

---

## Backup & versioning (growth control)

**Safety snapshots** live under:

```
/home/workdir/artifacts/atom_cloud_backups/
  2026-08-05_pre_bitemporal/     # frozen before schema change
  pre_promote_<ts>/              # created by promote_clouds.py
  weekly/                        # rolling weekly copies
```

- Pre-migration / pre-promote snapshots kept until explicit prune.
- Live clouds stay small (~6–8 MB total). History lives only in the backup tree.
- Canonical under the skill is the long-lived index; artifacts is ephemeral per session.

**Download / re-import surface**

```bash
python3 scripts/inventory/make_cloud_backup_tarball.py
# → artifacts/atom_cloud_backups_YYYYMMDD.tar.gz
```

---

## Crosswalks (ownership hygiene)

| Tool | Cloud(s) | Job |
|------|----------|-----|
| `memory_roster_crosswalk.py` | memory residuals ↔ inventory | Did REVIEW residuals land in the right promoted home? |
| `skill_surface_crosswalk.py` | skill_surface (± memory) | Same idea claimed under two different owners? |

---

## Inventory (file-level, not sentence-level)

```bash
python3 scripts/inventory/generate_inventory_v2.py --json-dir /home/workdir/artifacts
# → inventory_v2_all.json
```

---

## Private Olivia Operational Cloud (planned — Phase 2)

Separate from the two public clouds. Stateful, mostly hidden, for nags / priorities / working notes.

- Intended home: `data/olivia_ops/` (or agents/olivia/cold/ops under thin-live rule).
- Not indexed by default atom_search.
- Optional shared operational board sibling for triad visibility.
- Implementation deferred until durable+overlay is stable.

---

## Rules for other conversations

1. Prefer **atom_search** when the question is “where is this said?”  
2. Prefer **Cloud A** when the question is durable personal/ops/visual identity.  
3. Prefer **Cloud B** when the question is live agent/mirror/process state.  
4. Never write identity/ops/visual prose back under `agents/rook/` from Memory tooling.  
5. memory.md stays pointer-only; full prose lives in the five promoted homes (Cloud A sources).  
6. Before any schema or atomizer change, take a dated backup under `atom_cloud_backups/`.  
7. Canonical lives under the skill; promote is explicit; overlay is session-first.

**Both clouds are surfaced at the same specificity. Search knows both.**  
**Schema v0.2 is additive; old search paths remain valid.**  
**Durable home + session-overlay + explicit promote is the 2026-08-05 architecture.**

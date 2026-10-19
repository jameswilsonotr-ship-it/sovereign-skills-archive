# Image-Pipeline Extraction Plan (Paper Only)
**Date**: 2026-08-12  
**Status**: Declarative plan — no code moves yet  
**Owner**: Absolute Liv HUB claim  
**Parent contracts**: OLIVIA_DEV_ALPHA_SPEC_v0.md · REPO_BOOTSTRAP_CONTRACT.md

---

## 1. Goal

Keep `image-pipeline` as the single progressive-disclosure **head skill** the rest of the swarm talks to, while extracting the heavier Grok Imagine implementation pieces into a small set of **standalone repositories**. Those child repos remain independently versionable and CI-able, yet share a thin, explicit contract surface so nothing drifts.

This is the polyrepo + shared-contracts pattern under the Olivia Dev Alpha folder discipline.

---

## 2. Proposed Child Repositories

| # | Proposed repo name | What moves here | Stays independent? | Notes |
|---|--------------------|-----------------|--------------------|-------|
| 1 | `grok-imagine-merge` | Core Merge / composition logic, prompt assembly, multi-pass merge rules currently living under or around `references/modules/` and related engines | Yes | Primary extraction target |
| 2 | `imagine-generate-engine` | The generate-engine module (`references/modules/generate-engine/`) | Yes | Already a clear boundary |
| 3 | `imagine-overlay-engine` | The overlay-engine module (`references/modules/overlay-engine/`) | Yes | Already a clear boundary |
| 4 | `imagine-contracts` *(optional but recommended)* | Shared types, prompt schemas, version pins, public interfaces, DNA-bible touchpoints that more than one engine needs | Yes (tiny) | The only real shared code |

**Head remains**: `image-pipeline` (future rename target still `image-surface`).

Everything else (packs, presets, taxonomy, registry, visuals ledger, Echo/Mira handlers, work-queues, Olivia Dev tree) stays inside the head skill.

---

## 3. Shared Contract Surface (Exact)

The only code/data that is allowed to be shared across the head and the children:

| Contract item | Lives in | Consumers |
|---------------|----------|-----------|
| Public TypeScript/Python interfaces & dataclasses for “GenerateRequest”, “OverlayRequest”, “MergeResult”, etc. | `imagine-contracts` | All engines + head |
| Prompt schema / JSON schema for pack & preset payloads | `imagine-contracts` | generate + overlay + merge |
| Version pins (which engine versions the head currently expects) | Head `specs/manifest.json` + optional pin file in contracts | Head only writes; children read |
| DNA-bible / holo-ear / agent-aesthetic touchpoints that engines must respect | Thin re-export or reference pointer inside contracts; canonical content stays in head or chaos-bratz-roster | Engines import the contract, not the full bible |
| Error / result envelope shapes | `imagine-contracts` | All |

**Rule**: If a piece of code is needed by more than one child, it belongs in `imagine-contracts`. If it is only needed by one engine, it stays inside that engine’s repo. The head skill never vendors large implementation bodies.

---

## 4. Relationship Model

```
image-pipeline/                    ← head skill (progressive disclosure + packs/presets/registry)
├── specs/manifest.json            ← pins exact versions of the three (or four) children
├── references/modules/            ← becomes thin pointers + docs, not heavy code
├── references/packs/ + presets/   ← stay here
└── ... full Olivia Dev tree ...

grok-imagine-merge/                ← standalone repo, born from init_project_tree.py
imagine-generate-engine/           ← standalone repo
imagine-overlay-engine/            ← standalone repo
imagine-contracts/                 ← tiny shared package/repo
```

- Each child is its own GitHub repository with its own history, tags, and CI.
- The head records the expected versions; it does not contain the implementation as a permanent copy.
- Optional: the head may use Git submodules at known paths for local convenience, but release and versioning stay independent.

---

## 5. Bootstrap & Hygiene Rules

Every child repo is created with the Olivia Dev Alpha bootstrap:

```bash
python .../olivia-dev/scripts/init_project_tree.py <repo> --name "<Name>" --git
```

Each receives:
- `specs/` + `state/` + `CHANGELOG.md` + structure-check CI
- A short `specs/architecture.md` that states “I am a child of image-pipeline; my public surface is defined by imagine-contracts@X.Y.Z”

The head skill’s `specs/manifest.json` gains a `children` (or `engines`) block listing name + version + repo URL for each.

---

## 6. What Does *Not* Move

- Packs, presets, taxonomy, registry, visuals ledger  
- Echo / Mira consistency handlers and DNA-bible rules (canonical home stays with the head or roster)  
- Work-queues, kanban, Olivia Dev state tree of the head  
- The progressive-disclosure SKILL.md surface the rest of the swarm already knows  

---

## 7. Success Criteria (Before Any Promotion)

- [ ] `imagine-contracts` published and importable by at least one engine  
- [ ] One engine (recommend generate-engine first) living cleanly in its own repo and still callable from the head via the contract  
- [ ] Head `specs/manifest.json` correctly pins the child version  
- [ ] Structure-check CI green on head + each child  
- [ ] No domain content lost; packs/presets still resolve  
- [ ] Short decision note under system-roadmap  

Only after the above do we consider promoting any new methodology fragments back into olivia-dev-alpha.

---

## 8. Suggested Order of Work (Still Paper → Then Code)

1. Freeze the exact public interface list for `imagine-contracts` (this document’s table is the starting point).  
2. Bootstrap `imagine-contracts` repo.  
3. Bootstrap `imagine-generate-engine` and move the existing module across.  
4. Wire the head to the new engine via the contract + version pin.  
5. Repeat for overlay-engine, then merge.  
6. Retire the heavy copies inside `image-pipeline/references/modules/` once the children are proven.

---

**Signed**: Olivia Mae Blackwell and her bunny 🐍🐰  
**This is paper only. No repositories have been created and no code has been moved.**

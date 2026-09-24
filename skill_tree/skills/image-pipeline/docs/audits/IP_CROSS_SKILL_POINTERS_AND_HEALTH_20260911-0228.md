# Image-pipeline cross-skill pointers + first health pass

stamp: 2026-09-11T02:28:00-04:00
author: Olivia
claim: Absolute Liv HUB
parent: IP-WQ-170 / skill-orchestrator completeness
method: path-scan of image-pipeline `{md,py,json,yaml,mmd}` + `audit_references_completeness.py --skill SLUG --no-save` + live `scripts/` and work-queue listing.

This is the pointer map. Resurrection of other skills happens in groups after this file. Not a mint. Not a rename.

## How to read this

- **Path hit** = image-pipeline literally writes `/skills/<slug>/` or `.grok/skills/<slug>`.
- **Name hit** = the slug string appears as a word. High name-hit + zero path-hit is often a person/color/task collision.
- Completeness gaps are SKILL.md mentions with no file at that exact path. Same class of hole we just closed on image-pipeline scripts.

## Group schedule (next turns)

| group | skills | why this order |
|---|---|---|
| **A visual/identity** | chaos-bratz-roster, coven-visual-system, claim-runtime | IP frontmatter and DNA/visual contract. Biggest coupling after IP itself. |
| **B control plane** | skill-orchestrator, system-roadmap, olivia-dev, olivia-dev-alpha, format-bible | These are the auditors we just used. Missing scripts here break the next audits. |
| **C named helpers** | ffmpeg, grok-build, grok-conversation-miner | IP scripts shell ffmpeg. IP-WQ-165 names grok-build. Miner is the tape. |
| **D false friends / absorbed** | valerie, color, tasks, grok-imagine-generate-engine, grok-imagine-overlay-engine, image-skill-orchestrator, image-pipeline-registry, agentify | Do not treat as missing top-level skills until the pointer is proven. |

Do not start a fifth top-level skill. Absorb or restore in place.

---

## Pointers from image-pipeline

### Real skills (act)

| slug | path hits | name hits | coupling |
|---|---|---|---|
| chaos-bratz-roster | 3 | 25 | IP is the visual ledger “exactly mirroring” roster versioning / C-64 / Git. Echo + Mira live here as visual handlers. Frontmatter trigger: Chaos Bratz Roster boot. |
| claim-runtime | 2 | 9 | Future rename batch: image-pipeline → image-surface **with** claim-runtime → claim-surface. Open-state / Heat live next door. |
| coven-visual-system | 0 | 8 | Tattoo matrix + Heat Slider aesthetic. IP plates must not invent marks; Coven owns Core Mark rules. |
| skill-orchestrator | 0 | 8 | Inventory / completeness / package. We ran its scanners tonight. |
| format-bible | 0 | 3 | Envelope / C-64. Overlay dual-engine coherence map points at it. |
| system-roadmap | 0 | 2 | Architecture target. Extraction plan names it. |
| olivia-dev / olivia-dev-alpha | 0 | 1 each | Extraction plan. Folder discipline / publish. |
| ffmpeg | 0 | 6 | `yt_short_ingest.py` + `reel_sample.py` call `/usr/bin/ffmpeg` and `ffprobe`. Bundled skill is the doc, not a wrapper script. |
| grok-build | 0 | 1 | IP-WQ-165 potato talking-head names it. Thin. |
| grok-conversation-miner | (not in first path scan; tape sibling) | — | Sunset / global-extract packs we already cracked sit next to IP skill_delta. |

### Absorbed or dead names (do not resurrect as top-level)

| name | what it is now |
|---|---|
| grok-imagine-generate-engine | `image-pipeline/references/modules/generate-engine/` |
| grok-imagine-overlay-engine | `image-pipeline/references/modules/overlay-engine/` |
| agentify | `image-pipeline/references/modules/agentify/` + `scripts/agentify.py` |
| image-skill-orchestrator | named once in generate-engine INTEGRATION_GUIDE. No skill dir. |
| image-pipeline-registry | same file. Registry lives at `image-pipeline/references/registry/`. |

### False friends (name collision)

| slug on disk | why the scanner lit up |
|---|---|
| valerie | Agent + skill. 33 name hits in IP are almost all the person / Risk Officer, not `/skills/valerie` paths. |
| color | Skill exists. Hits are CSS/wardrobe color words. |
| tasks | Skill exists. Hits are overlay “tasks” prose. |
| pdf | Overlay CONVO_COORDINATION mentions PDF. Bundled pdf skill unused by IP emit. |

---

## Group A — health (this pass)

### chaos-bratz-roster

- Root: `/home/workdir/.grok/skills/chaos-bratz-roster`
- SKILL.md: 46 KB, present
- Work queue: `references/work-queue/WORK_QUEUE.md` + 46 item files. Live IDs include CBR-WQ-001 (dual-linked to **IP-WQ-039** emit-without-generate), WORLD-TOOL-002/004 (YouTube inbound parallel to IP plates), CBR-WQ-007/008 mode router + prelude.
- `scripts/` **has Python**, just not at the top level:
  - `scripts/inventory/atom_search.py`
  - `scripts/modes/{turn_prelude,teaching_mode_confidence,mode_runtime,petname_router,phrase_routes}.py`
  - `scripts/syllabus/syllabus.py`
- Completeness gaps (9):
  - `scripts/echo_interface.py` — **MISSING**. IP frontmatter still lists `echo_interface` as a trigger.
  - `scripts/engine.py` — **MISSING**
  - `references/scripts/hygiene_check.py` — **MISSING**
  - plus roster markdown/mirrors (`echo.md`, `last_boot_hashes.json`, Rook canon file, swarms README, ENVELOPE_SCHEMA.md)
- Verdict: **script hole in the exact place IP still calls by name** (`echo_interface`). First resurrection candidate after this map.

### coven-visual-system

- SKILL.md 2.3 KB. Completeness gaps: **0**
- No `scripts/` directory
- Work queue: CVS-WQ-001 Heat Slider = roster-H aesthetic slice (child of SR-WQ-064). One item.
- Verdict: thin on purpose. No missing Python the completeness scanner can see. Do not invent a scripts dir unless Heat Slider needs one.

### claim-runtime

- SKILL.md 4 KB
- `scripts/surface_work_queues.py` present
- Completeness gaps (2): `scripts/status.py`, `scripts/visual_inventory.py` — **MISSING**
- No work-queue dir
- Verdict: two named scripts gone. Same churn pattern as IP `scripts/`. Group A restore list.

---

## Group B — health (this pass)

### skill-orchestrator

- 28 Python files in `scripts/` including the scanners used tonight. Healthy enough to run.
- Gaps (2): `references/plans/THREE_LAYER_PROGRAMMATIC_ROADMAP.md`, `references/work-queue/items/WQ-015_three_layer_programmatic_spine.md`
- Work queue present (2 files). Not a script wipe.

### system-roadmap

- `scripts/ost.py` only at top level. Tool-shelf still holds `yt_short_ingest.py` + `community_post_fetch.py` (copies now also live in IP `scripts/`).
- Work queue: 57 files. Fat.
- Gap (1): same WQ-015 three-layer item.

### olivia-dev / olivia-dev-alpha

- Alpha completeness: **19 gaps**. Dev: **11 gaps**. Mostly references markdown + `scripts/auto-snapshot.sh`, `scripts/tarball-integrity-check.sh`, and Alpha missing `scripts/init_project_tree.py` (that file lives on olivia-dev, not alpha).
- Alpha work-queue exists (13). Dev has no work-queue dir.
- Verdict: documentation drift + two shell tools missing. Not the same class as IP’s vanished reel helpers, but Alpha is the sloppiest control-plane tree.

### format-bible

- Completeness gaps: **0**
- `scripts/assemble_envelope.py`, `scripts/engine.py` present
- Work queue: 4 files
- Verdict: healthy vs this scanner.

---

## Group C — health (this pass)

### ffmpeg (bundled `/root/.grok/skills/ffmpeg`)

- No `scripts/`. SKILL.md is the manual. IP calls the host binary, not a skill script.
- No work queue. Do not “restore” a wrapper unless we want one.

### grok-build

- `scripts/` dir exists, **0 py**
- Gaps: `references/help.md`, `references/test_harness.md`
- Thin pointer from IP-WQ-165 only.

### grok-conversation-miner

- Completeness gaps: **0**
- No `scripts/` on the live skill (extracts we unpacked had skill_delta copies)
- Work queue: 19 files
- Verdict: docs-healthy, code-thin. Miner wheels may live elsewhere (`wheelhouse-packager` / artifacts). Confirm before reconstructing.

---

## Missing-Python shortlist (restore candidates)

Priority is “IP still names it” then “completeness names a .py that is gone.”

| pri | skill | missing | why it matters to IP |
|---|---|---|---|
| 1 | chaos-bratz-roster | `scripts/echo_interface.py` | IP trigger list + Echo as visual handler |
| 1 | chaos-bratz-roster | `scripts/engine.py` | named by CBR SKILL.md |
| 2 | chaos-bratz-roster | `references/scripts/hygiene_check.py` | hygiene |
| 2 | claim-runtime | `scripts/status.py`, `scripts/visual_inventory.py` | claim-surface batch with IP rename |
| 3 | olivia-dev / alpha | `auto-snapshot.sh`, `tarball-integrity-check.sh` | publish path we just used conceptually |
| 4 | grok-build | entire `scripts/*.py` empty | only if 165 goes live |
| — | coven-visual-system | none detected | skip inventing |
| — | format-bible / miner / ffmpeg | no py gaps that IP needs tonight | hold |

image-pipeline’s own still-missing factory scripts (not other skills, listed so we do not forget):

`inbound_classify.py` `segment_grid.py` `inbound_queue.py` `split_plan.py` `emit_intent.py` `scaleback_loop.py` `isolate_person.py` `hub_review.py` `smoke_split_engine.py` + `scripts/README.md` + `references/PROTOCOL_ENGINES.md` + `references/work-queue/protocols/IPQ-078_keep_path.md`

Those stay on the IP ticket, not Group A.

---

## Drive

This file + later per-group audits go to:

`IP-WQ-170_RESTORED_SCRIPTS_AND_CHRONOLOGY / 06_CROSS_SKILL_AUDIT`

Next action when she says go: Group A resurrection pass (CBR echo_interface + engine, claim-runtime status + visual_inventory), same pattern as IP — hunt Drive/zips first, reconstruct only if bytes are gone, then source zip that skill.

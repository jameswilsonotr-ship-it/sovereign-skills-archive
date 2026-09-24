# BURN / included-quota status board

GitHub PR inventory captured **2026-09-17** from
[`jameswilsonotr-ship-it/sovereign-skills-archive`](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive).
The board covers PRs **#1–#30**; each purpose is a concise reading of the
PR title and its changed paths. GitHub reported all thirty PRs as open at
capture time. This is a documentation snapshot, not a live status feed.

## PR inventory

| PR | Base | Title | Primary paths | One-line purpose |
|---|---|---|---|---|
| [#1](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/1) | `skill-tree-intake` | docs: Awesome Split extras ledger intake (MIS-10) | `snapshots/2026-09-17/`, `MASTER-INDEX.md` | Record the Awesome Split extras and reconcile artifact-only skill hits without re-unpacking the skill surface. |
| [#2](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/2) | `skill-tree-intake` | feat: add MIS-6 offline harness | `harness/`, `.github/workflows/harness.yml` | Add deterministic offline connector, phone-MCP, hygiene, and CI harness foundations for MIS-6. |
| [#3](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/3) | `cursor/mis-6-stress-smoke-4ae6` | test: expand MIS-6 offline smoke and stress coverage | `harness/`, `.github/workflows/harness.yml` | Extend the MIS-6 harness with smoke, stress, connector, phone, and hygiene coverage. |
| [#4](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/4) | `main` | docs: scaffold AI Studio to APK delivery path | `docs/AI_STUDIO_PLAY_PATH.md`, `android/`, `.github/workflows/android-apk-stub.yml` | Document a manual AI Studio-to-Android delivery path and provide a non-deploying workflow stub. |
| [#5](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/5) | `cursor/mis-6-stress-smoke-4ae6` | feat: add offline tailnet bridge stubs | `bridges/`, `harness/` | Add offline-only Termux, Vultr, SFTP, and bridge-configuration stubs for a tailnet topology. |
| [#6](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/6) | `cursor/mis-6-stress-smoke-4ae6` | docs: scaffold off-cloud phone mesh architecture | `docs/OFFCLOUD_PHONE_MESH.md`, `docs/SPARK_GEMINI.md`, `bridges/` | Describe the off-cloud phone mesh, tailnet deployment templates, and explicit Spark/Gemini escalation path. |
| [#7](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/7) | `skill-tree-intake` | docs: add Pixel Gemma bridge runbook | `bridges/pixel/` | Provide a Pixel Gemma/Termux bridge runbook with setup, health, thermal, and handoff guidance. |
| [#8](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/8) | `skill-tree-intake` | feat: add Vultr tailnet inference bootstrap profiles | `bridges/vultr/` | Add tailnet-bound Vultr bootstrap profiles for Ollama, optional Letta, and a local coder helper. |
| [#9](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/9) | `skill-tree-intake` | docs: research Android phone MCP and Zenoh control-plane options | `docs/research/PHONE_MCP_INTENT_LANDSCAPE.md`, `docs/research/ZENOH_APK_NOTES.md` | Compare Android phone MCP and Zenoh control-plane options with source and safety notes. |
| [#10](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/10) | `skill-tree-intake` | docs: record Olivia/MIS Drive phone-mesh sweep | `docs/research/DRIVE_SWEEP.md`, `docs/research/DRIVE_HITS.json` | Preserve the Drive/MIS phone-mesh sweep as structured findings, references, and access-boundary notes. |
| [#11](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/11) | `main` | docs: research Zenoh Android control plane | `docs/research/ZENOH_CONTROL_PLANE.md`, `docs/research/GROXXPORTER.md` | Research the Zenoh Android control plane and bounded handoffs to adjacent audio/content tools. |
| [#12](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/12) | `skill-tree-intake` | docs: add Basic off-cloud mesh OpenSpec | `specs/openspec/basic/` | Turn the Basic off-cloud mesh proposal into an OpenSpec proposal, requirements, design, and task set. |
| [#13](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/13) | `skill-tree-intake` | docs: specify BASIC off-cloud mesh tier | `docs/openspec/BASIC_TIER.md` | Define the BASIC tier contract, routing policy, safety boundaries, and acceptance criteria for the off-cloud mesh. |
| [#14](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/14) | `skill-tree-intake` | docs: add Iron Pearl basic infrastructure spec | `docs/openspec/SPEC-001-IRON-PEARL-BASIC.md`, `docs/openspec/COLD_STEEL.md` | Specify the Iron Pearl Basic infrastructure profile and distinguish its Cold Steel edge profile. |
| [#15](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/15) | `skill-tree-intake` | feat: add local Ollama coder package | `coder/`, `tests/`, `docs/grok-cli.md` | Add a local Ollama-compatible coder package with chat CLI, memory hook, packaging, and offline tests. |
| [#16](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/16) | `skill-tree-intake` | docs: document zenoh.apk burner control plane and Android Intent MCP | `docs/research/ZENOH_APK_CONTROL_PLANE.md` | Document a proposed burner-phone Zenoh/Android Intent MCP seam while separating it from current app behavior. |
| [#17](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/17) | `skill-tree-intake` | docs: add Vesper-authoritative Iron Pearl OpenSpec | `docs/openspec/`, `bridges/README.md` | Refine Iron Pearl as a Vesper-authoritative OpenSpec and connect it to the bridge documentation index. |
| [#18](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/18) | `skill-tree-intake` | test: expand offline harness coverage | `harness/tests/`, `harness/stubs/`, `.github/workflows/harness.yml` | Add offline property, stress, MCP, and typing coverage to harden the harness contract. |
| [#19](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/19) | `main` | docs: define COLD STEEL and Tailscale bandwidth hygiene | `docs/COLD_STEEL.md`, `docs/BANDWIDTH_HYGIENE.md` | Define the Cold Steel substrate profile and document what Tailscale evidence can and cannot prove about bandwidth. |
| [#20](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/20) | `skill-tree-intake` | docs: add OpenSpec connector and runtime module specs | `docs/openspec/` | Add the shared BASIC tier and typed OpenSpec modules for Drive, GitHub, Linear, Gmail, phone, Spark, and Vultr/Letta. |
| [#21](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/21) | `skill-tree-intake` | docs: author sovereign phone bridge OpenSpec pack | `docs/openspec/` | Consolidate the sovereign phone bridge into five OpenSpec documents with deterministic acceptance cases. |
| [#22](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/22) | `main` | feat: expand coder with offline coverage and local Ollama architecture | `coder/`, `docs/`, `Dockerfile.coder`, `docker-compose.yml` | Expand the coder into a locally deployable Ollama architecture with offline tests and container guidance. |
| [#23](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/23) | `cursor/offline-harness-expansion-c6cb` | test: double offline harness stress coverage | `harness/tests/`, `harness/CI_TIMEOUTS.md`, `harness/PERFORMANCE.md` | Double connector stress coverage and document offline performance and CI timeout budgets. |
| [#24](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/24) | `skill-tree-intake` | docs: map zenoh control plane to burner phone MCP acceptance tests | `docs/openspec/SPEC-002-PHONE-MCP-INTENTS.md` | Translate the Zenoh control-plane design into a SPEC-002 burner-phone MCP acceptance contract. |
| [#25](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/25) | `cursor/openspec-pack-b21d` | test: add offline OpenSpec acceptance harness | `harness/tests/openspec/`, `harness/openspec_stubs.py` | Add fixture-backed offline tests for the phone-bridge OpenSpec acceptance cases. |
| [#26](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/26) | `main` | docs: promote burn-wave status and ICM analysis | `docs/burn-wave/` | Promote the burn-wave status, fork/ICM analysis, corpus metadata, and Linear comment drafts as reviewable documentation. |
| [#27](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/27) | `skill-tree-intake` | feat: ingest offline BURN HARD corpora | `harness/`, `docs/burn-wave/corpora/` | Generate and ingest hash-checked local-or-synthetic connector corpora without contacting providers or phones. |
| [#28](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/28) | `main` | test: add offline SPEC-002 phone MCP acceptance suite | `harness/`, `docs/openspec/SPEC-002-PHONE-MCP-INTENTS.md`, `pytest.ini` | Exercise SPEC-002 phone-MCP acceptance behavior with an offline, default-deny test suite. |
| [#29](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/29) | `skill-tree-intake` | docs: add Gemini Spark and Vesper bridge bind stubs | `docs/bridges/` | Define secret-free binding contracts and conservative send/capacity stubs for Spark and Vesper. |
| [#30](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/30) | `skill-tree-intake` | feat: generate OpenSpec CSV and Markdown matrices | `scripts/gen_openspec_matrix.py`, `docs/openspec-matrix.*`, `tests/` | Generate deterministic CSV and Markdown traceability matrices from OpenSpec documents and test their output. |

## Linear spine notes

These notes preserve the Linear context included in the existing burn-wave
drafts; they are not an API sync or an instruction to post comments.

- **[MIS-6](https://linear.app/missblackwell/issue/MIS-6/mock-tool-layer-wq-to-linear-map-no-imagine-in-ci)** —
  recorded as **In Progress** in the 2026-09-16 burn-wave snapshot; the spine
  is the mock tool layer plus the work-queue-to-Linear map, with PRs #2 and #3
  carrying the offline harness and stress intent. Keep Imagine out of CI and
  reconcile the real work-queue inventory before treating the map as complete.
- **[MIS-7](https://linear.app/missblackwell/issue/MIS-7/transform-the-live-skill-tree-into-van-clief-icm-format-folder-as)** —
  recorded as **Backlog (High)** in that snapshot; the spine is the
  live-skill-tree-to-Van-Clief-ICM transformation. Remain inventory-only until
  explicit human GO: no live skill-tree writes, mouth flattening, or invented
  `WORK_QUEUE.md` files.

## Scope and safety

- This file is markdown-only and contains no credentials, tokens, private
  keys, model weights, or provider payloads.
- PR titles, primary paths, bases, and open-state claims come from the
  repository and the read-only GitHub PR listing at capture time.
- The Linear bullets are historical notes from the existing burn-wave
  documentation; they do not claim current live status.

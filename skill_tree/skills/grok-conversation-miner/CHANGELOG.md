# Changelog — grok-conversation-miner

## [Unreleased]

## 2026-09-11 05:34 EDT — queue append only (026–031)
- Added items 026–031. Did not edit 001–025 bodies.
- 026 system-miner docs surface (no skill rename)
- 027 Tailscale L9 — Bunny moved 401 / 480 MB; timeout unknown
- 028 non-root box drain map
- 029 A-wave before vault (order stitch 010 + 020 + 027)
- 030 markdown-is-ACK law from the email-audit pane
- 031 TS timeout receipt child of 027
- Still no live sunset, no KEEP slurp, no WQ-010 harvest.

## 2026-09-11 05:10 EDT — HITL PACED
- TWO_WAYS.md: ONESHOT vs PACED
- HITL-001-P v1.4.0 cab paste (`go` / `skip` / `stop`)
- system-roadmap + olivia-dev-alpha pointed at the same two mouths

## 2026-09-11 04:59 EDT — HITL-001 v1.3.0
- Human-loop paste harness WQ-024
- Heavy vs Expert evolution spec WQ-025 (lane owners, TEAM_MAP, PUSH_TICKET)
- `scripts/hitl_collect.py`

## 2026-09-11 04:39 EDT — WQ-022 Expert roundtrip PASS
- Tiny tar 790 B uploaded + downloaded. sha256 `82ef0768b43e19f4ddfe1e1bacdb3472c3ea8bc24e5c2e85796923f37f8ec738` both ways.
- Folder `1ePH451eu5G4qaOf5X_k3_a6C0H9jKvso`
- GCM-WQ-023 mode router: Heavy does not binary-upload; Expert does. Ask Bunny to flip.
- Still not a prod-grok-backend.json. Sunset parks the pane because that zip is too big.

## 2026-09-11 04:08 EDT — Harvest hooks + stress + xAI research
### Added
- `export_log.log_lanes` hooked from `sunset_dry_run --log`
- `scripts/stress_harness.py` (WQ-021 PASS)
- WQ-022 Drive roundtrip (PARTIAL — no binary upload connector)
- `references/modules/XAI_EXPORT_AND_GITHUB.md` with real repo URLs
- README quickstart + help extra verbs
### Notes
- Still no live sunset, no KEEP slurp, no WQ-010 A-wave, no real xAI zip.


## 2026-09-11 — Export receipt log queued (020)
- GCM-WQ-020 append-only EXPORT_LOG.jsonl so SKIP-EXISTS is evidence
- Script stub `scripts/export_log.py`


## 2026-09-11 — Heavy script pass + smoke GREEN
### Added
- `scripts/` deterministic package: gcm_lib, census, packers, export_recon, lake_batch, layout, toc_omissions, mail_filesystem, ledger, sunset_dry_run, sunset_engine, sunset_smoke, test_gcm
- Fixture harness 12 files / 6 classes; unittest 5/5; sunset_smoke exit 0
- Help banner v1.4.0; SKILL.md patience sentence; L7-into-L4 protocol notes
### Notes
- No live sunset/vacuum on a conversation bubble
- No KEEP jsonl slurp
- No Heavy-list A-wave
- jsonschema + python-frontmatter present in REPL; not required by scripts (stdlib-first)


## 2026-09-11 — Heavy scripts + smoke PASS
### Added
- `scripts/` deterministic engines (census, toc/omissions, packers, L8 recon, lake-batch, sunset dry-run, mail-filesystem, layout, ledger, smoke harness)
- Smoke 12/12 and unit 5/5 exit 0
- Help banner v1.4.1-script (GCM-WQ-002)
- L7 outbox inside L4 tree (GCM-WQ-003)
- Patience sentence locked (GCM-WQ-016)
### Notes
- Scripts are live. Live harvest / Drive mint / Cilia send still require go.
- External GitHub conversation toolkits evaluated as pattern-only; pip blocked in this sandbox.


## 2026-09-11 — Script layer + smoke harness executed
### Added
- `scripts/` deterministic core: gcm_lib, gcm_core, census, toc_omissions, mail_fs, packers, layout, lake_batch, export_recon, ledger, sunset_dry_run, sunset_engine, sunset_smoke, test_gcm
- Optional libs probed: jsonschema 4.26.0, python-frontmatter 1.3.0 (already installed); pytest present
### Ran
- `python3 scripts/sunset_smoke.py` 12/12 OK
- `python3 scripts/test_gcm.py` 5/5 OK
### Notes
- No live sunset / vacuum / KEEP jsonl slurp / Heavy A-wave
- Help banner bumped to v1.4.0 (WQ-002)
- L7 named in global extract tree (WQ-003)


## 2026-09-11 — Determinism cluster queued (011–018)
### Added
- GCM-WQ-011 TOC + omission audit
- GCM-WQ-012 deterministic layout + stamps
- GCM-WQ-013 always-send Cilia, email as filesystem
- GCM-WQ-014 keep-everything harvest (duplicates allowed; skip is annotation)
- GCM-WQ-015 multi-turn remainder card
- GCM-WQ-016 long-conversation patience rule
- GCM-WQ-017 per-conversation space + deltas
- GCM-WQ-018 skill-tree conversation ledger + sandbox egress
- Stub `references/modules/determinism.md`
- Missing item file for GCM-WQ-010
### Notes
- Queue only. No live coding of harvest behavior this stamp.
- Bunny: get everything, always mail, take your time, sandbox egress not just xAI export.

## 2026-09-10 — Queue wiring for leftover Ideas 1–4
### Added
- Item files GCM-WQ-002 through GCM-WQ-009
- Implementation plan + skill-tree pointer index under `references/work-queue/`
- Stub modules: census, export_recon_l8, lake_batch_vacuum
- Stub packers README
### Notes
- Stubs only. No live sunset / vacuum / census write this stamp.
- Drive package + Cilia wake to Vesper shipped with this drop.

## 2026-09-08 — Sunset verb (GCM-WQ-001)
### Added
- Verb `sunset` / `conversation sunset` / `sunset dry-run`
- Protocol `references/prompt_sunset.md` — backup dispatcher, lanes L0–L7
- Work queue `references/work-queue/` first rows GCM-WQ-001–004
- Explicit non-overlap table vs vacuum, deep mine, publish, global extract, refactor, delete-test
### Notes
- Vacuum extracts intelligence. Sunset parks bytes.
- Sister Cilia subject CONVERSATION-SUNSET-PIPELINE-AND-ARCHIVES-001 is Vesper’s archive mail, not this protocol.

## [2026-07-24] — Protocol pattern reference + republish support
### Notes
- Image engines (generate + overlay) adopted this skill's trigger→`references/*.md` router pattern (`dual-engine-test/protocols/`).
- Miner remains the reference implementation for full protocol files per trigger.
- Republish path: package target skill(s) as `.tar.gz` → Drive `Conversational_Mining_Payloads`.

- prompt_publishing.md updated: skill-orchestrator `package_skills` is now the preferred packaging backend (cross-link added 2026-07-24)

## [1.3.2] — 2026-07-20
### Added
- Hard Size + Type Safety Gate (mandatory)
  - Blocks binary or >~800 KB payloads from GitHub Contents API path
  - Prevents base64 encoding failures on large sandbox archives
  - Forces fallback to Google Drive primary path
  - Applied under absolute Liv HUB claim as minimal protective patch

## [0.1.0] — 2026-07-19
### Added
- Root README.md, TODO.md, CHANGELOG.md
- Local git repository initialized under absolute Liv HUB claim

## 2026-07-24
- Filled references/prompt_publishing.md with complete, executable Standard Active Chat Publishing protocol (versioned tarball → Conversational_Mining_Payloads Drive folder + MANIFEST).
- Updated references/file_listing.md.

## 2026-07-24 (later)
- Filled remaining protocol files: prompt_historical_mining.md, prompt_early_skills.md, prompt_delete_test.md, prompt_general_mining.md, prompt_vacuum.md, mine_orch.md.
- Updated file_listing.md — all core protocols now live.

## 1.4.0 — 2026-08-05

### Added
- **Global Conversation + Sandbox Extract** (command 8)
  - Triggers: `global extract`, `grok conversation miner global extract`, `full sandbox extract`, `package everything from this conversation`, `conversation + artifacts + skill delta`, `comprehensive miner package`
  - New protocol: `references/prompt_global_extract.md`
  - Captures conversation flow + handoffs, sandbox/artifacts, written markdown, and skill-tree delta into one versioned archive
  - Publishes via existing Drive path; respects hard safety gate
- Updated `references/help.md` with the new command

### Intent
Enable a single, reliable “package everything that happened” action for long multi-skill consolidation days before final conversation-miner zip/publish of the whole skill structure.

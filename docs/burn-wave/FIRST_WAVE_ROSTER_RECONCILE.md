# First-wave roster reconciliation

Status: **draft reconciliation**

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-03-roster-reconcile` |
| Slot | `S2-03` |
| Base | `skill-tree-intake` |
| Evidence boundary | Local Git history and commit diffs only |
| External calls | None |

## Reconciliation rule

This roster uses the PR number in the local commit subject as the PR
identifier. The roster owner is the author identity recorded on that commit,
not a co-author or the GitHub committer. The file inventory is the exact
name-status diff for that commit. No file, owner, or status is inferred from a
remote service.

The inclusion mode for this slot is **Ultra only**. `OD` is not included. This
document does not create or imply an OD roster entry.

## Included first-wave entries

All four included entries are owned by `jameswilsonotr-ship-it`
(`james.wilson.otr@gmail.com` in the local commit metadata).

### PR #27 — offline BURN HARD corpus

- Commit: `a17e0db53b925b86c0c4e1b172629a2400af1632`
- Owner: `jameswilsonotr-ship-it`
- Subject: `feat: ingest offline BURN HARD corpora`
- Files:
  - `.github/workflows/harness.yml`
  - `docs/burn-wave/corpora/MANIFEST.json`
  - `docs/burn-wave/corpora/MANIFEST.md`
  - `harness/pyproject.toml`
  - `harness/src/sovereign_harness/__init__.py`
  - `harness/src/sovereign_harness/connectors.py`
  - `harness/src/sovereign_harness/corpus.py`
  - `harness/src/sovereign_harness/fixtures/drive.json`
  - `harness/src/sovereign_harness/fixtures/github.json`
  - `harness/src/sovereign_harness/fixtures/gmail.json`
  - `harness/src/sovereign_harness/fixtures/image.json`
  - `harness/src/sovereign_harness/fixtures/linear.json`
  - `harness/src/sovereign_harness/fixtures/phone_bridge.json`
  - `harness/src/sovereign_harness/fixtures/phone_health.json`
  - `harness/src/sovereign_harness/fixtures/web.json`
  - `harness/src/sovereign_harness/hygiene.py`
  - `harness/src/sovereign_harness/mcp_server.py`
  - `harness/src/sovereign_harness/phone_mcp.py`
  - `harness/src/sovereign_harness/py.typed`
  - `harness/stubs/duckdb/__init__.pyi`
  - `harness/tests/conftest.py`
  - `harness/tests/test_connectors.py`
  - `harness/tests/test_corpus.py`
  - `harness/tests/test_hygiene.py`
  - `harness/tests/test_offline.py`
  - `harness/tests/test_phone_mcp.py`
  - `harness/tests/test_properties.py`
  - `harness/tests/test_stress.py`

### PR #29 — Gemini Spark and Vesper bridge stubs

- Commit: `e5a8304e78dcebd09cd6f93b085d5dea035ab2b2`
- Owner: `jameswilsonotr-ship-it`
- Subject: `docs: add Gemini Spark and Vesper bridge bind stubs`
- Files:
  - `docs/bridges/SPARK_BIND.md`
  - `docs/bridges/stubs/GEMINI_SPARK_SEND.md`
  - `docs/bridges/stubs/VESPER_MCP_BIND.md`

### PR #30 — OpenSpec matrices

- Commit: `7087c2abc765dcf3cb8abe55e3cad56d574dff04`
- Owner: `jameswilsonotr-ship-it`
- Subject: `feat: generate OpenSpec CSV and Markdown matrices`
- Files:
  - `docs/openspec-matrix.csv`
  - `docs/openspec-matrix.md`
  - `docs/openspec/api-rate-limits.md`
  - `docs/openspec/cli-export.md`
  - `scripts/gen_openspec_matrix.py`
  - `tests/test_gen_openspec_matrix.py`

### PR #31 — Vultr Letta/Ollama provisioning runbook

- Commit: `d86e82482cc93819310d0dbcb67021996067caf8`
- Owner: `jameswilsonotr-ship-it`
- Subject: `docs: add cheapest Vultr Letta/Ollama provisioning runbook`
- File:
  - `docs/runbooks/VULTR_PROVISION_CHEAPEST.md`

## Hard-fence reconciliation

| Fence | Result |
| --- | --- |
| Ultra only | Applied to this roster; no OD entry is included. |
| No OD | No OD file, owner, or PR is added or inferred. |
| No `Willow` `SKILL.md` | No such file is included or modified by this slot. |
| No `CONV2_B` | No such entry or file is included or inferred. |
| Vultr ≠ Cold Steel | PR #31 remains a Vultr-specific runbook; it is not relabeled, merged with, or treated as Cold Steel. |
| No external calls | Evidence is limited to the local commit graph and diffs. |
| No secrets | No credentials, tokens, cookies, endpoints, or personal addresses are copied into this reconciliation. |
| Do not touch other S2 slots | This file is the only S2-03 deliverable. |

## Verification receipt

The source commits were inspected with local Git history and name-status
diffs. The resulting change adds only this reconciliation file; it does not
alter any first-wave source file or any other S2 slot.

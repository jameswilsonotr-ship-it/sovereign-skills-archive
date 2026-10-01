# Work Queue — grok-conversation-miner

**Updated**: 2026-09-11 05:34 EDT — appended WQ-026..031 (system-miner docs, Tailscale egress, box drain, A-wave order, markdown ACK, TS timeout). 001–025 untouched. No live sunset. No WQ-010 harvest. No KEEP slurp.

Heavy GO this pane: scripts landed, fixtures planted, `sunset_smoke.py` + `test_gcm.py` **exit 0**. No live sunset / vacuum / KEEP jsonl slurp. No Heavy-list A-wave (010).

**Lib probe:** stdlib tarfile/hashlib/json/email/zoneinfo/unittest + PyYAML + pytest present. jsonschema and python-frontmatter already installed in this REPL (`pip install` rc 0 / already satisfied). Pattern-only GitHub: slyubarskiy/chatgpt-conversation-extractor, silver-gr/AI-Conversation-Toolkit, wangjiake/RiverHistory — not vendored, not SSoT.

| ID | Title | Status | Notes |
|----|-------|--------|-------|
| **GCM-WQ-001** | Verb `sunset` — unified backup dispatcher | **LIVE 0.1.0** | Protocol `references/prompt_sunset.md`. Lanes L0–L7. |
| **GCM-WQ-002** | Help.md still says v1.3.0 in the title | **RAN 2026-09-11** | Banner now v1.4.1-script + scripts footer. |
| **GCM-WQ-003** | Wire sunset outbox `artifacts/sunset/` into global extract tree | **RAN 2026-09-11** | Protocol + smoke L7-in-L4. Live extract still needs go. |
| **GCM-WQ-004** | Dry-run first field proof on a live thread | **SMOKE-PASS** | Fixture dry-run writes nothing. Live bubble still not run. |
| **KLQ-WQ-001** | Dated MD tree SSoT (retrieve, do not republish) | **POINTER** | keep-lake-query owns the walk. Miner does not rebuild Oct 2025–Jun 2026 from jsonl. |
| **GCM-WQ-005** | Conclusive-census module (lazy-load) | **SCRIPT-LIVE** | `scripts/census.py` + smoke ACK match. No live CENSUS.jsonl write. |
| **GCM-WQ-006** | xAI export recon lane L8 | **SCRIPT-LIVE** | `scripts/export_recon.py` smoke diffs fixture ids. Not default sunset. |
| **GCM-WQ-007** | Artifact-class packers Imagine / video / plates | **SCRIPT-LIVE** | `scripts/packers.py` + plates lock card. |
| **GCM-WQ-008** | Lake-batch historical vacuum | **SCRIPT-LIVE** | `scripts/lake_batch.py` SKIP-EXISTS/NO_TWIN; refuses jsonl slurp. |
| **GCM-WQ-009** | scripts/sunset_smoke.py fixture harness | **PASS 12/12** | `python3 scripts/sunset_smoke.py` exit 0 at 2026-09-11 03:40 EDT. |
| **GCM-WQ-010** | Exact-title Heavy list miner queue (OCR 2026-09-10) | **QUEUED** | 124 unique titles, waves A–H. Do not run. Go slice = A01–A08. Item file added 2026-09-11. |
| **GCM-WQ-011** | TOC + omission audit | **SCRIPT-LIVE** | `scripts/toc_omissions.py` smoke writes both files. |
| **GCM-WQ-012** | Deterministic layout + stamps | **SCRIPT-LIVE** | `scripts/layout.py` + `gcm_lib.stamps`. |
| **GCM-WQ-013** | Always-send Cilia · email as filesystem | **RENDER-LIVE** | Offline renderer pass. Live send is a separate wake. |
| **GCM-WQ-014** | Keep-everything harvest | **ENCODED** | SKIP-EXISTS is OMISSIONS annotation in engine + protocol. |
| **GCM-WQ-015** | Multi-turn remainder card | **ENCODED** | mail_filesystem turns_remaining_estimate + time_is_not_the_budget. |
| **GCM-WQ-016** | Long-conversation patience | **ENCODED** | Sentence locked in sunset protocol + smoke test_12. |
| **GCM-WQ-017** | Per-conversation space + deltas | **SCRIPT-LIVE** | `layout.make_space` run_id folder. Drive spaces not minted. |
| **GCM-WQ-018** | Skill-tree conversation ledger + sandbox egress | **SCRIPT-LIVE** | `scripts/ledger.py` jsonl row. |
| **GCM-WQ-019** | Execute smoke + record lib eval | **PASS** | 12/12 sunset_smoke + 5/5 test_gcm. Libs: stdlib+pytest+yaml. pip no-net. |
| **GCM-WQ-020** | Append-only export receipt log | **SCRIPT-LIVE** | `scripts/export_log.py` + `log_lanes` hooked from dry-run. Hash chain. |
| **GCM-WQ-021** | Exhaustive fake-data engine smoke | **PASS** | `scripts/stress_harness.py` exit 0. 10 log rows. |
| **GCM-WQ-022** | Drive roundtrip stress | **PASS** | Expert pane 2026-09-11 04:39 EDT. Upload+download sha256 match. Folder `1ePH451eu5G4qaOf5X_k3_a6C0H9jKvso`. |
| **GCM-WQ-023** | Heavy vs Expert router | **LIVE** | `references/modules/mode_router.md`. Heavy does not upload tars. Expert does. Ask Bunny to flip. |
| **GCM-WQ-024** | HITL two-way harness | **READY** | ONESHOT v1.3.0 + PACED v1.4.0. `references/hitl/TWO_WAYS.md`. Roadmap + alpha pointed. |
| **GCM-WQ-025** | Heavy vs Expert evolution | **QUEUED** | Not just the push. TEAM_MAP, PUSH_TICKET, lane owners. Spec only. |
| **GCM-WQ-026** | System-miner docs surface | **QUEUED** | Verbs + help + quickstart + changelog discipline. No folder rename. |
| **GCM-WQ-027** | Tailscale egress lane L9 | **QUEUED** | 401 / 480 MB moved 2026-09-11. Timeout unknown. Not default sunset. |
| **GCM-WQ-028** | Non-root box drain map | **QUEUED** | ISO-of-files allowlist. No whole-VM tar. |
| **GCM-WQ-029** | A-wave before vault | **QUEUED** | Order only: 010 slice → 020 skip-log → 027 leftover bytes. |
| **GCM-WQ-030** | Markdown is ACK | **QUEUED** | Learned this pane. Docs twin is OMISSIONS. |
| **GCM-WQ-031** | Tailscale timeout receipt | **QUEUED** | Child of 027. ended_how = complete\|timeout\|reset\|unknown. |

Plan: `IMPLEMENTATION_PLAN_2026-09-10.md`
Pointers: `SKILL_TREE_POINTERS.md`
Determinism stub: `references/modules/determinism.md`
Items: `items/GCM-WQ-001` … `GCM-WQ-031`


## Smoke execution 2026-09-11 03:40 EDT

`python3 scripts/sunset_smoke.py` → 12/12 OK. `python3 scripts/test_gcm.py` → 5/5 OK.
Libs: jsonschema 4.26.0 + python-frontmatter 1.3.0 already present; pytest present; stdlib tarfile/hashlib/email used as SSoT. External conversation toolkits evaluated as pattern-only (ctk, claude-chats, chatgpt-conversation-extractor). Not vendored.

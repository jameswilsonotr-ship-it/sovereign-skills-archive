# STATUS_BOARD.md — sovereign-skills-archive

Snapshot generated: **2026-09-16 23:00 CT** by the burn-wave helper from a
GitHub MCP scrape. This is an archival snapshot, not a live status feed.

Repo: https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive
Source base at capture time: `skill-tree-intake` @ `640a2ca`
Promotion source: `burn-wave/mis6-artifacts` @ `ca6e91c`

## PR board (newest first)

| PR | State | Title | Cursor bcId | Focus |
|---|---|---|---|---|
| [#12](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/12) | open/draft | docs: add Basic off-cloud mesh OpenSpec | `bc-e7635932-1a90-5044-9048-9a3995509c43` | specs/openspec |
| [#11](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/11) | open/draft | docs: research Zenoh Android control plane | `bc-6a453412-d43f-55d6-9b89-ae9ff20e661d` | zenoh control plane |
| [#10](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/10) | open/draft | docs: record Olivia/MIS Drive phone-mesh sweep | `bc-3132f918-a2b7-5863-9ca2-5a7fa24e5e3e` | DRIVE_SWEEP |
| [#9](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/9) | open/draft | docs: research Android phone MCP / Zenoh options | `bc-44314b73-2e5f-5f58-81c3-134cba3b16c2` | phone MCP landscape |
| [#8](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/8) | open/draft | feat: Vultr tailnet inference bootstrap profiles | `bc-d5dc12bf-10c4-5019-8460-7dd007acb132` | vultr/letta/coder |
| [#7](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/7) | open/draft | docs: Pixel Gemma bridge runbook | `bc-e278687d-fc82-52b2-a1a7-4edcb4b6f3be` | pixel gemma |
| [#6](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/6) | open/draft | docs: scaffold off-cloud phone mesh architecture | `bc-55dc6831-a821-532b-8cf9-e5d0cbfe61d6` | off-cloud mesh |
| [#5](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/5) | open/draft | docs+CI stub: AI Studio → GHA → APK path | `bc-aa78790a-f982-55cc-a2c0-6e76ede5f3d4` | AI Studio APK |
| [#4](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/4) | open/draft | feat: local MCP bridge + Tailscale/SFTP stubs | `bc-7f997958-4fe9-584f-ba30-a6b08fac8c0a` | bridges MCP |
| [#3](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/3) | open/draft | feat: MIS-6 stress/smoke expansion | `bc-c0ca293c-c571-5b1a-8d41-a7845cb14ae6` | stress smoke |
| [#2](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/2) | open/draft | feat: MIS-6 harness skeleton + dummy connectors | `bc-9169a50a-d1fc-53ce-b085-a439415f54fb` | harness |
| [#1](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/1) | open/draft | ledger / intake follow-up (leave alone) | `(ledger)` | ledger-only |

## Merge hygiene notes

- PR #1 is ledger-only — do not stack harness work onto it.
- Prefer stack: `skill-tree-intake` → #2 harness → #3 stress → bridges/docs PRs.
- Hard nos across all agent PRs: no CONV2_B, no mouths flatten, no LangChain, no live SKILL.md writes, no secrets/APKs/weights.
- Canonical Composio account_ids: `gmail_illipe-eaves` (Otr), `gmail_deash-pungle` (Liv), `gmail_algy-alpen` (Vesper), `github_unhex-ume`, `linear_diver-forbow`, `googledrive_baste-nous`. Never `gmail_atilt-worked`.

## Linear spine

| Ticket | Status | Title |
|---|---|---|
| [MIS-6](https://linear.app/missblackwell/issue/MIS-6/mock-tool-layer-wq-to-linear-map-no-imagine-in-ci) | In Progress | Mock tool layer + WQ-to-Linear map (no Imagine in CI) |
| [MIS-7](https://linear.app/missblackwell/issue/MIS-7/transform-the-live-skill-tree-into-van-clief-icm-format-folder-as) | Backlog | Transform live skill tree into Van Clief ICM (Thunderclap only until GO) |
| MIS-8 | Backlog | Shop pane 2974334 snapshot |
| MIS-10 | In Progress | Awesome Split dumps ledger |

## Promoted documentation

- [`FORKS.md`](FORKS.md) — expanded RinDig ICM analysis and fork decisions
- [`linear/`](linear/) — MIS-6 / MIS-7 comment drafts
- [`pr-briefs/`](pr-briefs/) — next-agent follow-up briefs
- [`corpora/`](corpora/) — committed metadata only; payloads remain local-only
- [`cloud-agents/`](cloud-agents/) — transcript inventory

The source branch also referenced offline corpora and shallow upstream clones
outside this repository. Those local paths are intentionally not dependencies
of this mainline documentation promotion.

## Remote branches (GitHub MCP list)

- `cursor/awesome-split-ledger-5619`
- `cursor/basic-tier-openspec-bdce`
- `cursor/cold-steel-bandwidth-hygiene-3cf4`
- `cursor/document-ai-studio-play-path-f3d4`
- `cursor/drive-sweep-5e3e`
- `cursor/iron-pearl-basic-spec-7142`
- `cursor/local-coder-ollama-eff7`
- `cursor/local-mcp-bridge-8c0a`
- `cursor/mis-6-hibunny-override-54fb`
- `cursor/mis-6-stress-smoke-4ae6`
- `cursor/offcloud-phone-mesh-61d6`
- `cursor/openspec-basic-tier-9c43`
- `cursor/phone-mcp-intent-landscape-16c2`
- `cursor/pixel-gemma-runbook-f3be`
- `cursor/vultr-inference-bootstrap-b132`
- `cursor/zenoh-apk-control-plane-34e6`
- `cursor/zenoh-control-plane-661d`
- `harness/mis6-local-scaffold`
- `harness/pr1-skeleton`
- `main`
- `skill-tree-intake`
- `burn-wave/mis6-artifacts` (promotion source)

_Refreshed branch list: 2026-09-16 23:01 CT_

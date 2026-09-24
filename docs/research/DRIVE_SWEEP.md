# Olivia / MIS off-cloud phone mesh — Drive sweep

**Sweep date:** 2026-09-17 UTC
**Repository:** `jameswilsonotr-ship-it/sovereign-skills-archive`
**Branch basis:** `skill-tree-intake`
**Primary Drive scope:** [Awesome Split](https://drive.google.com/drive/folders/11WEijQl3lP6Spw3kwFpE1kNC7MVGWsgP)

## Executive result

The available evidence describes a local-first phone mesh, but does not prove
that a production mesh is currently running:

```text
Pixel / Termux control plane
        │  Tailscale-only transport
        ├── local Gemma runner (Tier A)
        ├── SFTP artifact lane
        └── optional Vultr inference host (Tier B)
                    │ explicit policy-gated escalation
                    └── Gemini / AI Studio Spark (Vesper, Tier C)
```

The strongest source is the Drive note
`S23_TERMUX_MCP_PHONE_BRIDGE_AND_LOCAL_LLM_2026-09-16.md`. It is marked
**provisional idea**, so its claims about third-party phone-MCP packages,
Grok remote MCP, model speed, and Tailscale serving are research leads, not
deployment receipts.

The handoff packet adds the operational boundaries:

- Termux from F-Droid is the initial phone install.
- The first gate is an offline `GET /health` stub on port `8081`.
- Tailscale/SFTP are the intended private path; bind services to loopback or
  the `100.x` tailnet interface, never the public interface.
- CI must not require a phone to be online.
- APK work follows the HTTP health contract; it is not the first dependency.
- v0 intentionally has no SMS or camera capability in the repository harness.

## Important correction: PR state

The GitHub API currently reports [PRs #1–#8](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pulls)
as **open**, not merged. Their descriptions contain the relevant phone-mesh
design and safety claims, but the corresponding changes are not present on
`skill-tree-intake` as merged history. The report therefore treats those PRs
as public design evidence, not as shipped runtime evidence.

## Sources and findings

### Drive handoff folder

[HANDOFF_20260916_GROKBOT_CURSOR](https://drive.google.com/drive/folders/1T_TsVp43ScGvfh_P9uS_k_cWQZ4g-YAu)
contains four plaintext briefs:

1. `2026-09-16_HI_BRIEF.md` — asks for a phone MCP/Tailscale specification,
   an offline harness, and no live SMS/camera path; says APKs follow the
   `:8081` stub.
2. `2026-09-16_CURSOR_DRIVE_WALK.md` — identifies the Awesome Split folder,
   extract destination, manifest, and the rule to leave large split archives
   as Drive pointers.
3. `2026-09-16_VESPER_REQ.md` — points to PR #1, the Colab notebook, extract
   destination, manifest, and Linear MIS-6/MIS-7/MIS-10.
4. `2026-09-16_USAGE_AND_SHIFT.md` — records that Pixel 9a + Tailscale and
   Termux MCP were considered proven in the wider work, but supplies no
   phone-health receipt or endpoint test in this packet.

### Direct Drive research hits

- `S23_TERMUX_MCP_PHONE_BRIDGE_AND_LOCAL_LLM_2026-09-16.md`
  (file ID `1HQFjZMEXUyVAEC6dP8AFlsH306SlSQIs`) proposes Termux + a local
  MCP bridge, Tailscale, a router, local LLM routing, and explicit cloud
  escalation. It names SMS, flashlight, contacts, GPS, and camera as
  capabilities claimed by an external `phone-mcp-server`; that is not a
  statement that this repository enables those capabilities.
- `ADDENDUM_VESPER_TAILNET_SOCKS_20260910.md`
  (file ID `1WTmGp73bZZox-icJqQNSVQEuPnhhlt7_`) records a userspace Tailscale
  plus SFTP/ SOCKS pattern, strict host-key handling, separate Tailscale and
  SSH credentials, and a no-secret rule. It is a transport precedent, not a
  phone-MCP deployment receipt.
- `GCM-WQ-027_tailscale_egress.md`
  (file ID `1KvQsmA8QtUW5UQglRZ_FK_X2x_ymbvEP`) calls Tailscale/SFTP an
  optional, operator-approved lane and requires byte counts, timestamps,
  stop conditions, and hashes for transfers.
- `07_CLAUDE_TURN2_DOCKER_ZENOH_RUNBOOK.txt`
  (file ID `1XHFcpy9p8kBrjkDIa7MZu9lO5OIlHTMZ`) proposes a schema-validated
  JSON envelope over MQTT/Zenoh with hop limits and human checkpoints. It is
  a bus design adjacent to the phone mesh, not evidence that Zenoh is in the
  phone path.
- `# Intent.txt`
  (file ID `1RWUaDzkyOPIMq7biz9iaBh86KVw2txIN`) defines a provisional
  intent/router taxonomy and separates CI, bus, memory, and other planes.
  It supports an allowlisted, policy-gated router but does not identify a
  live phone endpoint.

### Known Drive containers and manifest

- Awesome Split folder: `11WEijQl3lP6Spw3kwFpE1kNC7MVGWsgP`
- Extract destination: `1ahggBATOejlUbMRddNgTa3YR0jde_QGU`
- Manifest: `EXTRACT_MANIFEST.json`,
  `1NDaYkFfbhsi457Q8yVpC30bvz3WKEdhE`
- Relevant extracted container: `CONV8_CASCADIA_MCP_PANE_20260916`,
  `1nF0INuJX8-3CNyXCV48hm-EWOdPTuFx5`
- Relevant bundle name: `mcp-voice-plumbing-2026-09-13` and its zip
  (`1h9whlXCUkbWwMXMnmw2vUq0YDWSuQvvu`,
  `1Y_9LNlQMYpRhC_pp6b6AzZVzKmQR_0ZQ`)
- The manifest records large split and combined archive entries. This sweep
  did not download, unpack, or inspect `CONV2_B`; it remains a pointer only.
  The same applies to the full skill-surface archive.

## In-repo hits

The existing tree contains older transport and handoff references:

- `skill_tree/skills/system-roadmap/references/tool-shelf/README.md`:
  userspace Tailscale, SFTP, state reuse, SOCKS5, and the rule not to store
  Tailscale or private-key material.
- `skill_tree/skills/system-roadmap/references/plans/VESPER_PKG_PROXY_INVENTORY_2026-08-26.md`:
  Drive payloads, split artifacts, Zenoh package pointers, and the boundary
  that Spark is not the inference box.
- `skill_tree/skills/system-roadmap/references/third-party-skills-eval-2026-08-17/04_PREVIOUS_TURN_AND_ROADMAP_UPDATES.md`:
  an older recommendation to evaluate `mcp-proxy` at the edge and on Vultr.
- `skill_tree/skills/system-roadmap/references/skills/conversation-lake/handoff_2026-08-29_keep-union-and-vesper-bus.md`:
  Olivia/Vesper bus separation, Drive receipts, and an append-only overlay
  for phone/GPS events.
- `skill_tree/skills/wheelhouse-packager/SKILL.md`:
  Olivia/Vesper wheelhouse handoff and Drive receipt conventions.
- `origin/main:snapshots/2026-09-17/AWESOME_SPLIT_LEDGER.md`:
  current ledger pointer; confirms Git holds text receipts while large
  tarballs stay in Drive.

The current checked-out branch does **not** contain the bridge files described
by PRs #5–#8 as merged files. Those PRs remain the best public GitHub
specification of the intended implementation.

## GitHub PR and sibling-repo hits

The PR descriptions and changed-file metadata provide these useful claims:

- [PR #1](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/1):
  Awesome Split ledger only; explicitly excludes `CONV2_B` unpack.
- [PR #2](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/2)
  and [PR #3](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/3):
  offline connector/phone harness direction, no SMS/camera in v0, and
  no live network in CI.
- [PR #4](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/4):
  AI Studio → GitHub Actions → APK handoff, manual-only and secret-free.
- [PR #5](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/5):
  Termux health bridge on `:8081`, SFTP templates, and a Tailscale-only
  Vultr host sketch.
- [PR #6](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/6):
  three-tier phone → Vultr → explicit Gemini/Spark architecture.
- [PR #7](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/7):
  Pixel/Termux notes, small Gemma starting points, battery/thermal gates,
  and no model weights/APKs/keys in Git.
- [PR #8](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/8):
  tailnet-only Ollama/Gemma/Qwen bootstrap templates and a separate SFTP
  sidecar boundary.

Read-only clones of adjacent public repositories found:

- [marmalade](https://github.com/jameswilsonotr-ship-it/marmalade):
  Android node/operator separation, MCP response-text parsing into Android
  Intents, interactive cards, pairing, and optional Tailscale binding. It is
  an adjacent implementation, not the Olivia/MIS mesh.
- [zenoh.apk](https://github.com/jameswilsonotr-ship-it/zenoh.apk):
  Android Zenoh pub/sub client with routed/peer modes and a `7447` router
  example. It supplies a possible bus transport, not phone-MCP proof.
- [kokoro-speaker-cloner.apk](https://github.com/jameswilsonotr-ship-it/kokoro-speaker-cloner.apk):
  existing GitHub Actions APK build surface; no phone-control-plane evidence.
- [Groxxporter](https://github.com/jameswilsonotr-ship-it/Groxxporter):
  Android/AI Studio export tooling and APK packaging; no Tailscale phone
  control-plane evidence.
- [grok-build-cli](https://github.com/jameswilsonotr-ship-it/grok-build-cli):
  MCP schema discovery/health scaffolding and an explicit no-credentials-in-
  repo rule.
- [sovereign-connectors](https://github.com/jameswilsonotr-ship-it/sovereign-connectors):
  public repository exists, but the checked-out snapshot contains only a
  short README and no usable phone bridge implementation.

## What could not be accessed without Drive auth

The canonical Drive URLs for Awesome Split, the handoff folder, and the
manifest redirect an anonymous browser to Google sign-in; an anonymous fetch
of the manifest returned `401 Unauthorized`. Therefore, without Drive OAuth
we could not:

- list private Drive folders or resolve child file IDs;
- read the handoff documents or the manifest contents;
- inspect the text inside the extracted phone-mesh bundles;
- verify whether a claimed phone/Vultr endpoint is live;
- distinguish a planning note from a deployment receipt using Drive metadata.

This run did have authenticated Drive MCP access, so the named text files and
metadata above were readable. Public GitHub and public sibling repositories
were separately reachable. No secret value, key material, model weight, APK
binary, or conversation archive was copied into this repository.

## Recommended next Drive paths for James / Olivia

Open these in order, using Drive search/list rather than unpacking archives:

1. [HANDOFF_20260916_GROKBOT_CURSOR](https://drive.google.com/drive/folders/1T_TsVp43ScGvfh_P9uS_k_cWQZ4g-YAu)
   — reconcile the four plaintext briefs with the current PR state.
2. [S23 Termux bridge note](https://drive.google.com/file/d/1HQFjZMEXUyVAEC6dP8AFlsH306SlSQIs/view)
   — verify each external package claim and replace provisional language
   with a tested package/version receipt.
3. [CONV8 Cascadia MCP pane](https://drive.google.com/drive/folders/1nF0INuJX8-3CNyXCV48hm-EWOdPTuFx5)
   — open the text/code files inside the extracted folder; compare them to
   the health, cancellation, and transport contracts.
4. [MCP voice-plumbing folder](https://drive.google.com/drive/folders/1h9whlXCUkbWwMXMnmw2vUq0YDWSuQvvu)
   — inspect the source documents, not the zip, for the Android intent and
   Termux implementation details.
5. [Vesper tailnet/SOCKS addendum](https://drive.google.com/file/d/1WTmGp73bZZox-icJqQNSVQEuPnhhlt7_/view)
   — confirm the current host-key, ACL, and SFTP procedure before any write
   test.
6. [GCM-WQ-027](https://drive.google.com/file/d/1KvQsmA8QtUW5UQglRZ_FK_X2x_ymbvEP/view)
   — close the partial-transfer question with a receipt containing bytes,
   timestamps, and a hash.
7. [EXTRACT_MANIFEST.json](https://drive.google.com/file/d/1NDaYkFfbhsi457Q8yVpC30bvz3WKEdhE/view)
   — use SHA-256 entries to locate the intended text bundle; do not open or
   reassemble `CONV2_B` for this task.
8. [Vesper package proxy inventory](https://drive.google.com/drive/folders/1WBUpJGA7aVsBoeUcAzzk4aajcaJ2bO_I)
   — reconcile Zenoh/package pointers with the current phone bridge choice.

## Scope guardrails honored

- No `CONV2_B` unpack.
- No full skill-surface unpack.
- No secrets or private-key bytes.
- No phone actions, SMS, camera, flashlight, provisioning, or paid Vultr API
  calls.
- No new runtime dependency was added.

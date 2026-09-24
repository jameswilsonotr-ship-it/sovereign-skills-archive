# Phone control-plane MCP and Android Intent landscape

Research snapshot: 2026-09-17 UTC. This is a shortlist and architecture study,
not an implementation plan or a recommendation to deploy any project
unchanged.

## Executive shortlist

| Rank | Project | Why it is relevant | Burner-control-plane fit | Primary blocker |
| --- | --- | --- | --- | --- |
| 1 | [khimaros/mimic](https://github.com/khimaros/mimic) | Native Android accessibility service with separate `intents`, local HTTP, and MCP surfaces; loopback and token pairing are first-class. | **High for a narrow intent gateway.** The default is local-only, and pairing is explicit. It can be reached through a tightly scoped relay or Tailscale address without making every Android API a tool. | GPL-3.0; accessibility services and arbitrary intent/UI control are powerful. Review the exact intent allowlist before forking. |
| 2 | [stixez/droid-mcp](https://github.com/stixez/droid-mcp) | Native Android MCP app with typed modules for flashlight, SMS, notifications, `send_intent`, and `share_content`; HTTP server, bearer token, and QR pairing. | **High for typed capability modules.** It already has the exact tool vocabulary needed for a burner phone. Fork only a small allowlisted module set, not all 145 tools. | Apache-2.0, but its full surface spans 53 modules and sensitive permissions: SMS, contacts, location, screen, shell, accessibility, Shizuku/root options. |
| 3 | [premex-ab/phone-mcp](https://github.com/premex-ab/phone-mcp) | Native Kotlin/Ktor SSE MCP server with pluggable tool modules, bearer tokens, runtime enable/disable, external tool providers, and an SMS Intent path that does not require `SEND_SMS`. | **High as a small native server.** Modular boundaries and explicit consent are closer to a capability broker than a general shell bridge. | MIT and active, but only 10 stars; inspect authentication, lifecycle, and provider discovery before trusting it with a network-facing phone. |
| 4 | [JamilCPU/phone-mcp](https://github.com/JamilCPU/phone-mcp) | Clear PC MCP-server → Tailscale HTTP → Termux phone-agent architecture; covers flashlight, notifications, SMS, and Android APIs. | **High for the mesh topology.** It demonstrates the desired off-phone MCP client and phone-side HTTP agent split. | No license reported by the GitHub API; 0 stars. It binds the agent on `0.0.0.0`, so shared-key auth and Tailscale ACLs must be treated as mandatory. |
| 5 | [kahz12/DroidMCP](https://github.com/kahz12/DroidMCP) | Small native ARM64 Go MCP servers for Termux, with loopback/API-key defaults, optional TLS, sandboxed roots, notifications, SMS, sensors, and an on-device LLM proxy. | **High for a decomposed Termux control plane.** Separate binaries make it possible to ship only a notification or status server. | MIT, but release binaries are architecture-specific and SMS is deliberately privileged. It does not provide the same native Android Intent abstraction as the Android-app projects. |
| 6 | [termuxgpt/termux-mcp](https://github.com/termuxgpt/termux-mcp) | Active HTTP/Streamable HTTP Termux server with native MCP mode plus explicit `/torch`, `/notify`, `/sms-send`, and `/share` endpoints. | **Medium-high for a fast experiment.** It has the exact bridge commands and loopback default. | AGPL-3.0; shell/filesystem surface is broad, command timeout defaults to unlimited, and network binding requires careful token configuration. |
| 7 | [nelvinzfx/termux-mcp-shell](https://github.com/nelvinzfx/termux-mcp-shell) | Minimal Streamable HTTP MCP server for Termux shell/files with loopback default and optional bearer/API-key token. | **Medium for transport plumbing.** Useful as a local HTTP baseline behind Tailscale, not as the Android capability policy itself. | No license reported by the GitHub API; shell and file access are much broader than a burner control plane needs. |
| 8 | [htekdev/phone-mcp-server](https://github.com/htekdev/phone-mcp-server) | Termux/Termux:API server with 18 phone tools, including SMS, flashlight, location, camera, and notifications. | **Medium for a proof of concept.** Easy capability coverage and a simple Streamable HTTP endpoint. | MIT, but it binds `0.0.0.0` with no authentication by default and documents only basic shell safety filters. Do not expose it directly to a tailnet without adding an auth boundary. |

The shortlist is deliberately split into two families:

* **Native app brokers:** `mimic`, `droid-mcp`, and `phone-mcp` keep Android
  permissions, Intent handling, and consent in an Android process.
* **Termux bridges:** `phone-mcp`, `DroidMCP`, `termux-mcp`, and
  `termux-mcp-shell` are easier to iterate on, but inherit shell, package,
  process, and network risks from a general-purpose Linux environment.

## Capability and risk matrix

| Capability | Native Android path | Termux path | Burner-plane policy |
| --- | --- | --- | --- |
| Flashlight | Typed `toggle_flashlight`/brightness in `droid-mcp`; native modules in other app servers. | `termux-torch` through Termux:API. | Safe first write operation; expose only `on`, `off`, and status if available. |
| SMS | `droid-mcp` uses `READ_SMS`/`SEND_SMS`; `premex-ab/phone-mcp` also demonstrates an SMS Intent flow without direct send permission. | `termux-sms-list`/`termux-sms-send`; Termux:API warns that malicious callers can incur charges. | Default to read-disabled and send-disabled. Require a human confirmation, recipient allowlist, visible audit record, and never run from CI. |
| Notifications | Notification posting is lower privilege; reading/replying requires Notification Listener access and may expose private text. | `termux-notification`; notification listing may require notification access. | Allow a local “heartbeat” notification; keep read/reply tools out of the first slice. |
| Share sheet | Native `ACTION_SEND`/`ACTION_SEND_MULTIPLE` with `FileProvider` content URIs is the cleanest path. | `termux-share` invokes the Android share Intent. | Permit text or pre-approved files only; do not allow arbitrary path disclosure. |
| Generic Android Intent | `mimic` exposes an Intent surface; `droid-mcp` has `send_intent` and deep-link tools. | `am start`/`termux-am` or Termux `RUN_COMMAND` Intent. | Use an explicit action/component/data allowlist. Do not expose an arbitrary `am` command tool. |
| Shell/files | Available indirectly through Termux servers and some native apps. | Natural and powerful in Termux. | Keep off the first burner profile; if needed, isolate it as a separately keyed server with a sandbox root and timeouts. |
| UI automation | Accessibility, IME, overlays, or Shizuku/root can operate arbitrary UI. | ADB-backed tools can tap/type/screenshot. | Treat as a separate emergency/debug profile; it defeats the narrow Intent safety boundary. |

## Architecture notes

### Recommended control-plane shape

```text
off-phone MCP client
        │
        │ Tailscale / WireGuard; one phone-specific credential
        ▼
phone-side broker (native app or Termux HTTP MCP)
        │
        ├── allowlisted Android Intents
        ├── low-risk status/torch/notification adapters
        └── human-gated SMS/share adapters
```

The phone should initiate or accept only the tailnet connection needed for the
broker. A server that binds `0.0.0.0` on Wi-Fi is not equivalent to a
Tailscale-only service. Prefer loopback binding plus a narrowly scoped relay,
or bind to the tailnet interface and enforce both a token and Tailscale ACLs.
Do not rely on an unencrypted shared LAN or on an MCP client’s UI to provide
authorization.

### Termux and F-Droid foundation

[Termux:API](https://github.com/termux/termux-api) is the capability adapter,
not an MCP server. Its helper binary forwards requests over local anonymous
Unix sockets to the signed companion app. The [F-Droid package page](https://f-droid.org/packages/com.termux.api/)
documents the required companion app and explicitly warns that SMS
permissions can result in unexpected charges. Install Termux and Termux:API
from the same distribution source; mixing signatures breaks the plugin
relationship. The [Termux `RUN_COMMAND` Intent documentation](https://github.com/termux/termux-app/wiki/RUN_COMMAND-Intent)
is useful when a native broker needs to ask Termux to run a bounded command and
receive a result.

SourceForge did not surface a distinct, maintained Android-Intent MCP
implementation in this search. Its useful entries were mirrors/catalog pages:
[Termux:API](https://sourceforge.net/app/termux-api/android/),
[Termux application mirror](https://sourceforge.net/projects/termux-application.mirror/),
[MCPTools](https://sourceforge.net/projects/mcptools.mirror/), and
[MCP Shell Server](https://sourceforge.net/projects/mcp-shell-server.mirror/).
Treat those as discovery links, not as independent upstreams; the MCP Shell
Server page identifies its GitHub upstream, and the Termux page identifies its
GitHub project.

## On-device Gemma / LiteRT / MediaPipe

* [Google AI Edge LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM) is
  the current runtime direction for Android LLM deployment. It supports
  Android/Kotlin, `.litertlm` bundles, streaming, tool use, and CPU/GPU/NPU
  backends. The repository was active on 2026-09-17 and is Apache-2.0.
* [Google AI Edge Gallery](https://github.com/google-ai-edge/gallery) is the
  reference app for trying models on Android without putting a model in this
  repository. It is Apache-2.0 and was active on 2026-09-16.
* [Gemma 3n E2B IT LiteRT-LM](https://huggingface.co/google/gemma-3n-E2B-it-litert-lm)
  is a multimodal candidate for low-resource devices, but its Hugging Face
  card is manually gated under the Gemma license.
* [Gemma 3 1B IT LiteRT](https://huggingface.co/litert-community/Gemma3-1B-IT)
  is a smaller Android-oriented candidate, also gated under the Gemma license.
* [Gemma 4 E2B IT LiteRT-LM](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm)
  is Apache-2.0 on its model card and distributed as `.litertlm`; the card
  notes that Android AI Core/Gemini Nano is the preferred production path on
  supported devices. Its roughly multi-gigabyte model footprint is a poor
  reason to vendor it into this archive.

Pixel 8a/9a-class deployment should be treated as a device benchmark, not a
model-card promise. Tensor SoC generations, thermals, available RAM, and
backend support determine latency and memory pressure. Keep the phone broker
independent from inference: a local model may propose a tool call, but the
broker must still enforce the Intent allowlist and SMS confirmation. The older
[MediaPipe LLM Inference Android path is deprecated](https://github.com/google-ai-edge/mediapipe/issues/6270)
in favor of LiteRT-LM; do not start a new Android integration on the legacy
`.task` path without a migration reason. Keep `.litertlm`/`.task` artifact
formats distinct.

## Risks and go/no-go gates

1. **Permission minimization:** start with battery/status, flashlight, and an
   explicit notification. Add SMS only after confirming the Android permission
   and billing/charge behavior on the burner account.
2. **Transport boundary:** require an authenticated endpoint; bind loopback or
   the Tailscale interface only. Record the peer identity and tool name.
3. **Intent policy:** allowlist action, component/package, URI scheme, and
   MIME type. Reject arbitrary extras that can smuggle a shell command or a
   private file.
4. **Human gates:** SMS send, notification read/reply, calls, camera, location,
   contacts, and UI automation require separate explicit enablement. CI must
   never contact the phone or send an SMS.
5. **Supply chain:** pin source revisions and verify release checksums. Do not
   vendor APKs, model weights, or native binaries in this archive.
6. **License review:** GPL/AGPL projects may be useful as design references
   without being copied into an MIT/Apache-compatible implementation. Resolve
   this before forking code.

## PR-body checklist for the next Cursor agent

- [ ] **First transport/Intent spike:** wire a minimal, non-SMS profile from
  [`khimaros/mimic`](https://github.com/khimaros/mimic): loopback MCP/HTTP,
  explicit pairing, and one allowlisted Intent/share operation. Treat its
  GPL-3.0 terms as a hard fork boundary.
- [ ] **First typed capability comparison:** inspect
  [`stixez/droid-mcp`](https://github.com/stixez/droid-mcp) modules for
  flashlight, notifications, `send_intent`, and `share_content`; do not
  enable its broad 145-tool surface.
- [ ] **MIT-native alternative:** evaluate
  [`premex-ab/phone-mcp`](https://github.com/premex-ab/phone-mcp) if GPL
  reuse is unacceptable; retain its bearer token, module enablement, and
  SMS-Intent review points.
- [ ] **Tailscale wiring:** use
  [`JamilCPU/phone-mcp`](https://github.com/JamilCPU/phone-mcp) as the
  phone/desktop topology reference, but add authentication and a declared
  license before copying anything.
- [ ] **Termux fallback:** compare
  [`kahz12/DroidMCP`](https://github.com/kahz12/DroidMCP) for an ARM64,
  per-capability server; keep the filesystem/shell and SMS servers disabled
  in the default burner profile.
- [ ] **Inference boundary:** benchmark a downloaded Gemma/LiteRT-LM model on
  the target Pixel only after the broker policy works; do not check model
  files or APKs into this repository.
- [ ] **Safety verification:** test only with a fake recipient/fixture, no
  real SMS send from CI, and document Android permission prompts and audit
  behavior before any broader wiring.

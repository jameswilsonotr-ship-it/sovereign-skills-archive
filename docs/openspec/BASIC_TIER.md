# OpenSpec: BASIC_TIER — local-first off-cloud mesh

**Status:** Draft proposal
**Owner:** James
**Branch basis:** `skill-tree-intake`
**Scope:** Gemma on an Android phone, a tailnet-only Vultr Ollama host with
optional Letta, explicit Spark escalation, and Tailscale/MCP control paths.

This document is a contract proposal, not a deployment receipt. The source
PRs referenced below are open design work as of 2026-09-17; they are not
treated as merged runtime evidence. This document contains no credentials,
private keys, model weights, APKs, or provider secrets.

## 1. Summary

The basic tier is a local-first inference mesh:

```text
                         explicit, policy-gated escalation
  Pixel phone ────────► Vultr host ─────────────────────► Spark
  Gemma / phone MCP      Ollama + optional Letta           Gemini API
        │                       │                           │
        └──────────── Tailscale tailnet / MCP ─────────────┘
                    optional SFTP durable handoff
```

The phone is the first inference choice for short, private, low-latency
requests. Vultr is the second tier for longer context, shared state, bounded
concurrency, and models that do not fit comfortably on the phone. Spark is a
third-tier escalation only when a policy permits the request to leave the
phone/VPS boundary or when Spark is explicitly requested.

Tailscale supplies private reachability and peer identity. MCP supplies the
authenticated command/tool boundary. Ollama supplies local model serving on
Vultr. Letta is an optional memory/application service backed by the same
local Ollama endpoint; it is not a replacement for the inference API.

## 2. Goals

The implementation conforming to this spec MUST:

1. Prefer the phone's local Gemma runner for eligible requests.
2. Keep the phone, Vultr host, and any MCP sidecar reachable only through
   loopback or an explicitly authorized Tailscale interface.
3. Offer a stable, small request/result envelope across phone, Vultr, and
   Spark, including request ID, tier, model, timeout, and failure state.
4. Make every phone capability explicit and allowlisted. The model MUST NOT
   gain arbitrary Android Intent, shell, file, UI, camera, location, contacts,
   notification-read, or SMS power by inference alone.
5. Keep Ollama and Letta separate from the MCP sidecar and from the public
   network. Letta MUST call Ollama over the private Compose network.
6. Require an explicit policy decision before sending any request to Spark.
7. Redact or reject credentials, private keys, provider tokens, unapproved
   private mail, and other non-forwardable data before a cloud hop.
8. Fail honestly when a tier is unavailable. An offline phone MUST return a
   local result, a queued/deferred result, or `deferred_offline`; it MUST NOT
   claim that a remote escalation succeeded.
9. Be testable without a phone, live network, paid API, Vultr resource, or
   provider credential. CI MUST use fixtures and mocks.
10. Leave an auditable record of routing metadata without storing raw prompts,
    private response bodies, or secret values in ordinary health logs.

## 3. Non-goals

This BASIC tier does **not**:

- provision, resize, start, stop, or destroy a Vultr resource;
- select a Vultr plan, GPU, region, model tag, or monthly cost without an
  operator decision;
- commit or distribute Gemma/Ollama model weights, GGUF/LiteRT artifacts,
  APKs, native libraries, or generated build output;
- put a Gemini/Spark key, Tailscale auth key, Vultr token, SSH private key,
  Letta database password, or Gmail credential on a phone or in Git;
- turn Cursor or Cursor Cloud into a runtime inference dependency;
- silently forward phone requests to Spark because local inference is slow;
- expose Ollama, PostgreSQL, Letta, phone MCP, or SFTP on a public interface;
- make SMS, camera, calls, contacts, location, notification reads/replies,
  UI automation, arbitrary shell, or arbitrary filesystem access part of the
  default phone profile;
- make Zenoh a required transport. Zenoh may be evaluated as an event/data
  plane later, but MCP remains the command boundary for this tier;
- claim that the open PRs are merged or that a planning note proves a live
  endpoint;
- unpack or copy large archive contents into this repository as part of mesh
  setup.

## 4. Terms and invariants

### 4.1 Terms

| Term | Meaning |
| --- | --- |
| Tier A | On-device Gemma inference on the Android phone. |
| Tier B | Headless Vultr inference: Ollama by default, with optional Letta. |
| Tier C | Explicit Spark escalation through the approved Gemini API path. |
| Phone broker | Narrow Android/Termux MCP service that enforces capabilities; it is not the model runtime. |
| MCP sidecar | A separate service that calls the phone broker and/or SFTP; it does not publish inference ports. |
| Tailnet | The authorized Tailscale network and its ACL/device policy. |
| Forwardable | Data classification approved by policy for the next tier. |
| Request ID | An opaque, unique correlation value generated by the caller. It is not a credential. |

### 4.2 Invariants

These are normative and apply to every implementation:

- **Fail closed:** missing auth, missing policy, unknown capability, expired
  request, invalid tier transition, or invalid model selection is a denial,
  not a best-effort fallback.
- **Separate credentials:** Tailscale, SSH/SFTP, Vultr, Letta, and Gemini
  credentials are different classes and MUST NOT be reused.
- **Private bind:** a service binds to `127.0.0.1` or its assigned `100.x`
  Tailscale address. A default of `0.0.0.0` is non-conformant.
- **Bounded work:** requests have a maximum payload, context, output, and
  timeout. Unbounded conversation or repository uploads are non-conformant.
- **No implicit promotion:** Tier A → Tier B → Tier C is a policy decision;
  transport failure alone does not authorize the next hop.
- **Honest simulation:** fixture or fake transports MUST be labeled as such
  and MUST NOT report that a phone command or remote response was delivered.
- **No secret logging:** health, audit, and error records contain references,
  hashes, IDs, reason codes, and redacted classes—not secret values or raw
  sensitive content.

## 5. Architecture and responsibilities

### 5.1 Tier A: phone Gemma

The first target is a Pixel 8a-class device. A Pixel 9a uses the same baseline.
Any future Pixel 11 Pro sizing remains provisional until its retail hardware,
Android build, thermals, and supported runtime are measured.

The default local model target is Gemma 3 1B or a supported Gemma 3n E2B
artifact in a 4-bit, Android-compatible runtime. A larger model is an
experiment, not a BASIC-tier admission criterion. LiteRT-LM/MediaPipe-style
Android integration is preferred for sustained on-device inference; a
Termux/`llama.cpp` path is a controlled fallback or experiment. The bridge
MUST remain independent of the chosen runner.

The phone MUST:

- keep model artifacts and native executables on the device;
- start with bounded context, output, batch size, and thermal limits;
- support cancellation or a clear timeout outcome;
- treat background suspension and missed heartbeats as normal unavailability;
- expose only the enabled capability set in health/capability metadata;
- never need a direct Spark/Gemini key for the standard route.

### 5.2 Tier B: Vultr Ollama and optional Letta

The Vultr host is a tailnet-only headless service. The baseline is Ollama
behind a gateway. The current source template uses an Ollama-compatible
`/v1` endpoint, `/health`, and `/api/tags`; a GPU reservation is opt-in and
must be verified against the selected image and instance.

Letta is an optional Compose profile for memory/application behavior. It uses
the private Ollama endpoint and a pgvector-backed database. Letta MUST NOT
cause Ollama or PostgreSQL to be published directly. Its external port, when
enabled, is reachable only from authorized tailnet peers and remains subject
to application authentication and the pinned image/version.

The Vultr admission gate MUST record the selected plan, region, hourly price,
model tag/digest, storage, transfer assumptions, and an operator-approved
stop/destroy procedure. The `$250` credit is a cap for planning, not an
authorization to provision or a latency/cost guarantee.

### 5.3 Tier C: Spark

Spark is the explicit Gemini API escalation persona/path. The phone does not
call Spark directly in the BASIC route. A policy-approved control-plane
adapter—normally the Vultr sidecar or an operator-controlled service—performs
the call using a deployment-only secret reference.

Spark MUST be selected only when:

- the caller explicitly requests Spark; or
- Tier A and Tier B cannot satisfy the request and the data policy permits
  the selected input to leave the local boundary; or
- an approved capability is unavailable locally and the request is marked
  forwardable.

Credentials, unredacted private mail, private keys, and other rejected data
MUST return `denied` or `needs_redaction`; they MUST NOT fall through to Spark.

### 5.4 Tailscale and MCP

Tailscale is the network identity/reachability layer, not the application
authorization layer. ACLs SHOULD grant only the required peer-to-port edges:

| Edge | Required purpose | Default exposure |
| --- | --- | --- |
| Authorized peer → phone `:8081` | Phone health/MCP | Loopback or tailnet only |
| Authorized peer → Vultr Ollama gateway | Tier B inference | Tailnet only |
| Authorized peer → Letta `:8283` | Optional memory/application API | Tailnet only, profile disabled by default |
| Vultr sidecar → Olette-box SFTP | Durable handoff | Tailnet only, pinned host key |
| Adapter → Gemini API | Tier C escalation | Explicit outbound policy only |

MCP is the command boundary. It MUST return the node identity, capability,
tier, model, and result status in a typed response. A successful `/health`
response only proves liveness; it does not prove that an MCP session or model
is ready.

## 6. Interfaces

The interfaces below distinguish the existing offline contract from the
proposed production extension. Implementers MUST NOT present a stub as a
production inference service.

### 6.1 Phone health

**Transport:** HTTP on `127.0.0.1:8081` by default, or the phone's authorized
Tailscale address when remote health is intentionally enabled.

```http
GET /health
Accept: application/json
```

The compatibility minimum from the offline harness is:

```json
{
  "status": "ok",
  "service": "phone-bridge",
  "version": "0.1.0",
  "capabilities": ["health", "offline-fixtures"]
}
```

The production extension MAY add the following fields without removing the
compatibility minimum:

```json
{
  "status": "ok",
  "service": "phone-bridge",
  "version": "1.0.0",
  "device_id": "pixel-8a",
  "runner": "litert-lm",
  "model_id": "gemma-3-1b-q4",
  "ready": true,
  "capabilities": ["health", "local_inference", "cancel"]
}
```

`device_id`, `runner`, and `model_id` MUST be deployment metadata, not secrets.
Health output MUST NOT include IP credentials, environment dumps, prompt text,
tokens, or private file paths. A health route MUST return a non-success or
`ready: false` when the runner is absent; it MUST NOT simulate readiness.

The current v0 offline MCP tool surface is:

```text
phone_health() -> health fixture
phone_fixture() -> offline fixture
```

These tools prove call shape only and do not access Android APIs. Production
tool names and transport MAY differ, but the same safety and response rules
apply.

### 6.2 Phone inference and cancellation

The production phone runner SHOULD implement the following narrow surface
behind the broker:

```http
POST /v1/chat
POST /v1/cancel
```

Request:

```json
{
  "request_id": "opaque-correlation-id",
  "task": "classify",
  "input": "redacted bounded input",
  "model_id": "gemma-3-1b-q4",
  "timeout_ms": 8000,
  "max_output_tokens": 256,
  "allowed_tools": [],
  "data_classification": "local-only"
}
```

Result:

```json
{
  "request_id": "opaque-correlation-id",
  "status": "completed",
  "tier": "A",
  "model_id": "gemma-3-1b-q4",
  "output": "bounded result",
  "reason_code": null
}
```

Allowed `status` values are `completed`, `deferred`, `deferred_offline`,
`cancelled`, `denied`, and `failed`. A deferred result MUST include a
reason code such as `context_too_large`, `thermal_limit`, `runner_unready`,
or `policy_requires_vultr`; it MUST NOT trigger a remote hop by itself.

### 6.3 Routing envelope

Every cross-tier request MUST use an envelope equivalent to:

```json
{
  "schema": "sovereign.mesh.request.v1",
  "request_id": "opaque-correlation-id",
  "parent_request_id": null,
  "origin": "phone",
  "requested_tier": "A",
  "current_tier": "A",
  "task": "summarize",
  "input": "redacted bounded input",
  "data_classification": "local-only",
  "forwarding": {
    "allow_vultr": false,
    "allow_spark": false
  },
  "timeout_ms": 8000,
  "max_output_tokens": 256,
  "hop_count": 0,
  "allowed_tools": []
}
```

Rules:

- `request_id` is required, unique within the retention window, and not a
  secret.
- `input` is bounded and redacted before every hop. A full conversation dump
  is not a valid default.
- `hop_count` is incremented and bounded to prevent loops.
- `requested_tier` expresses intent; `current_tier` records actual handling.
- `allow_spark` MUST be false unless an explicit policy check authorizes it.
- `allowed_tools` defaults to an empty list. Tool permissions do not travel
  implicitly from one tier to another.

### 6.4 Vultr Ollama gateway

The tailnet-facing Tier B contract is:

```http
GET /health
GET /api/tags
POST /v1/chat/completions
```

The implementation MAY use a Caddy or equivalent gateway in front of Ollama.
The Ollama container remains on the private Compose network. `OLLAMA_BASE_URL`
for Letta MUST use the internal service address (for example, the Compose
service name and port), not the host's public address.

The deployment configuration MUST contain placeholders or secret references
only. A conforming deployment validates its rendered Compose configuration
before `up`, pulls one selected model deliberately, and avoids a restart
loop that re-downloads model data.

### 6.5 Optional Letta profile

Letta is enabled only by an explicit profile/operator action:

```text
compose profile: letta
external service: Letta application API on the configured tailnet address
internal model endpoint: http://ollama:11434/v1
database: private pgvector service
```

The exact Letta API is pinned to the selected image/version in the deployment
record. This spec does not freeze a vendor's changing agent API. Conformance
requires that:

1. the profile is disabled by default;
2. Letta reaches Ollama over the private network;
3. the database password is deployment-only and unique;
4. no database port is published to the host;
5. Letta availability is reported separately from Ollama availability; and
6. a Letta failure does not make the basic Ollama inference contract claim
   that inference is unavailable.

### 6.6 Spark escalation adapter

The adapter accepts only an approved envelope:

```json
{
  "schema": "sovereign.mesh.spark-request.v1",
  "request_id": "opaque-correlation-id",
  "from_tier": "B",
  "persona": "spark",
  "model": "<approved-model-reference>",
  "system_prompt_ref": "<deployment-config-reference>",
  "input": "approved redacted request",
  "allowed_tools": [],
  "timeout_ms": 15000
}
```

The adapter returns:

```json
{
  "request_id": "opaque-correlation-id",
  "status": "completed",
  "tier": "C",
  "model_id": "<approved-model-reference>",
  "output": "bounded result",
  "reason_code": null
}
```

The adapter MUST reject missing prompt references, unknown persona/model
combinations, disallowed data classifications, and attempts to use a CMV
identity or credential. It MUST redact API keys and private content from
logs. A missing Spark key/project/model returns `configuration_error`; it
does not guess, retry through another identity, or route through a phone.

### 6.7 MCP sidecar

The MCP sidecar is a separate process with deployment-only configuration
similar to:

```dotenv
PHONE_MCP_URL=http://<PHONE_TAILNET_IP>:8081
PHONE_MCP_HEALTH_URL=http://<PHONE_TAILNET_IP>:8081/health
PHONE_MCP_ENDPOINT=http://<PHONE_TAILNET_IP>:8081/mcp
```

The exact MCP path/transport is selected by the phone implementation. A
health check MUST happen before a tool call, but health alone MUST NOT bypass
MCP authentication or capability policy.

The sidecar MAY use SFTP for durable, bounded jobs:

```text
mesh-drop/
  inbox/<request-id>/request.json
  working/<request-id>/status.json
  outbox/<request-id>/response.json
  outbox/<request-id>/artifacts/*
```

SFTP transfers MUST use a dedicated least-privilege account, strict host-key
checking, restrictive permissions, atomic `.part` then rename writes, content
type/size limits, retention, and a receipt with bytes, timestamps, and hash.
Keys, passwords, and unredacted request contents are never committed or
placed in an inference prompt.

## 7. Routing policy

The default decision sequence is:

```text
eligible local request?
  yes ──► Tier A Gemma
  no
    approved for Vultr and Tier B available?
      yes ──► Tier B Ollama / optional Letta
      no
        explicit Spark request or approved Tier C policy?
          yes ──► Tier C Spark
          no ──► denied, queued, or deferred_offline
```

Required reason codes include:

| Code | Meaning | Permitted next action |
| --- | --- | --- |
| `context_too_large` | Phone bounds would be exceeded | Tier B only if forwarding is allowed |
| `runner_unready` | Local model is not ready | Queue or Tier B if policy allows |
| `thermal_limit` | Device should stop inference | Queue or Tier B if policy allows |
| `policy_requires_vultr` | Request is approved for Tier B | Tier B |
| `spark_explicit` | Caller explicitly selected Spark | Tier C after validation |
| `needs_redaction` | Input contains non-forwardable data | Ask for redaction; no hop |
| `deferred_offline` | No permitted reachable next tier | Queue/local response |
| `configuration_error` | Missing/invalid deployment config | Operator repair; no alternate identity |

The router records only:

```text
request_id, from_tier, to_tier, model_id, reason_code,
latency_ms, status, redacted_error_class
```

Raw prompts, raw private responses, tokens, and credential material are not
ordinary routing telemetry.

## 8. Security and operational gates

### 8.1 Phone admission

Before enabling a device:

- verify the exact device SKU, available RAM/storage, Android build, runtime,
  model license, battery policy, and thermal behavior;
- use one trusted Termux distribution and the official Tailscale app;
- pass local `/health` twice, including after restart;
- verify remote health from exactly one authorized tailnet peer;
- prove that the public interface cannot reach `:8081`;
- use a separate SFTP Ed25519 key and keep its private half on the phone;
- run cold start, bounded ten-turn, cancellation, screen-off, and thermal
  tests with a small Gemma baseline;
- verify that model files and native binaries remain device-only.

### 8.2 Vultr admission

Before starting a resource:

- review the current Vultr catalog and record arithmetic credit burn;
- choose a CPU/GPU plan from measured model memory and concurrency needs;
- inject a short-lived Tailscale join secret and random Letta password out of
  band;
- run `docker compose config --quiet` on the rendered deployment;
- verify `/health`, `/api/tags`, and `/v1` from an authorized tailnet peer;
- verify the public interface cannot reach Ollama or Letta;
- pin image/model versions and plan rollback;
- stop/destroy the resource and inspect retained volumes/snapshots after the
  test.

### 8.3 Spark admission

Before enabling Tier C:

- identify the approved project/model and secret references;
- prove one disposable redacted request and a clean log scan;
- prove disabled-key behavior returns `configuration_error`;
- prove disallowed private data returns `needs_redaction`;
- record a prompt/config digest and redacted result, never the key or raw
  private payload.

## 9. Acceptance criteria

An implementation is BASIC-tier conformant only when every applicable
criterion below is satisfied. A checkbox marked “future operator test” is not
claimed as passed by documentation alone.

### 9.1 Static and offline acceptance

- [ ] `docs/openspec/BASIC_TIER.md` contains no credential, key, token,
      private-key bytes, model weight, APK, or secret-manager export.
- [ ] `git diff --check` passes.
- [ ] JSON examples parse, or are explicitly marked pseudocode.
- [ ] Offline tests run without a phone, Tailscale, Vultr, Gemini, or paid API.
- [ ] The phone fixture exposes health only and rejects SMS/camera calls.
- [ ] Health supports 128 bounded concurrent fixture requests without leaking
      request content.
- [ ] Malformed/empty account or deployment identifiers are rejected.
- [ ] Fixture/simulation responses are labeled and cannot claim delivery.
- [ ] Logs from offline tests contain no secret-like values or raw private
      payloads.

### 9.2 Phone acceptance — future operator test

- [ ] Local `GET /health` returns the compatibility shape and accurate
      readiness.
- [ ] A selected Gemma baseline completes a bounded offline prompt.
- [ ] Cancellation, timeout, runner-unready, and thermal-limit outcomes are
      explicit and honest.
- [ ] The service is loopback-only or bound to the phone's authorized
      Tailscale address; it is not publicly reachable.
- [ ] A peer can reach health only after the Tailscale ACL and application
      auth checks pass.
- [ ] The default capability list excludes SMS, camera, calls, contacts,
      location, notification reads/replies, UI automation, shell, and files.
- [ ] A missed heartbeat causes a bounded defer/queue result, not infinite
      reconnect attempts.

### 9.3 Vultr acceptance — future operator test

- [ ] The rendered Compose configuration validates before any startup.
- [ ] Ollama is reachable through the tailnet gateway and not the public
      interface.
- [ ] `/health`, `/api/tags`, and `/v1/chat/completions` return bounded,
      authenticated/policy-checked responses.
- [ ] The Letta profile is off by default and, when enabled, reaches Ollama
      internally and keeps PostgreSQL private.
- [ ] Letta failure is distinguishable from Ollama failure.
- [ ] SFTP, if enabled, verifies host key, account scope, atomic transfer,
      retention, and a transfer receipt.
- [ ] The model is pulled deliberately once; restart does not re-download it.
- [ ] The operator records cost/credit assumptions and a stop/destroy action.

### 9.4 Spark acceptance — future operator test

- [ ] Spark cannot be reached from the phone without the approved control
      plane and explicit policy.
- [ ] An explicit Spark request succeeds with a redacted disposable input.
- [ ] A local/Vultr request does not silently escalate when Spark is not
      allowed.
- [ ] Missing key/project/model returns `configuration_error`.
- [ ] Private/unredacted input returns `needs_redaction`.
- [ ] Logs contain no provider key, raw prompt, raw private response, or
      Gmail credential.
- [ ] The returned result is labeled Tier C/Spark with request ID and model.

### 9.5 End-to-end acceptance — future operator test

Given a redacted bounded request:

1. The phone returns a Tier A result when its runner is ready.
2. The phone returns a reasoned defer when the request exceeds local bounds.
3. An explicitly authorized defer reaches Tier B over Tailscale.
4. Tier B returns an accurate model/tier/status result.
5. Only an approved failure or explicit request can reach Spark.
6. A tailnet or provider outage yields `deferred_offline`, `failed`, or
   `configuration_error` with no false success.
7. The audit record contains routing metadata only.

## 10. Failure behavior

| Failure | Required result | Forbidden behavior |
| --- | --- | --- |
| Phone offline | local answer, queue, or `deferred_offline` | Claim Tier B/Spark completed |
| Phone runner not ready | `runner_unready` | Report `ready: true` |
| Phone too hot or over memory bound | `thermal_limit` or `deferred` | Infinite retry loop |
| Tailscale ACL denies peer | `denied`/transport failure | Public fallback bind |
| Ollama unavailable | Tier B `failed`; next hop only by policy | Route silently to Spark |
| Letta unavailable | Letta-specific failure; Ollama may remain usable | Claim memory was persisted |
| Spark unavailable | Tier C `failed`/`configuration_error` | Try a different identity/key |
| Input contains a secret | `needs_redaction`/`denied` | Log or forward the secret |
| Unknown capability/tool | `denied` | Fall back to shell or arbitrary Intent |
| Stale/replayed request | `denied`/`expired` | Execute twice |

## 11. Rollout sequence

The sequence is deliberately dependency-light:

1. **Contract-only:** land this spec, offline fixtures, static secret scans,
   and a mock router. No device or cloud resource is needed.
2. **Phone health:** validate Termux/phone `/health`, Tailscale ACL, and
   bounded liveness from one authorized peer. Keep the runner stub clearly
   labeled until a real model is measured.
3. **Phone Gemma:** admit one measured small model, then test cancellation,
   thermal behavior, and local-only routing.
4. **Vultr Ollama:** validate one model and the tailnet-only gateway. Keep
   Letta disabled until the base path is healthy.
5. **Letta profile:** enable only for a specific memory use case; validate
   internal Ollama connectivity and database retention.
6. **Spark:** enable the redacted, policy-gated adapter last.
7. **Optional event plane:** evaluate Zenoh or another bus only after the MCP
   request/result and audit contracts are stable.

Each phase can be rolled back by disabling the next tier. No phase requires
placing secrets or binaries in this archive.

## 12. Traceability to existing PRs

| Source | Design evidence incorporated |
| --- | --- |
| [PR #2](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/2) | Offline harness, `GET /health` on `:8081`, official MCP SDK shape, no SMS/camera in v0. |
| [PR #3](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/3) | Fixture-only smoke/stress coverage, malformed account rejection, bounded concurrent health checks, no live CI calls. |
| [PR #4](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/4) | Manual/secret-free Android artifact boundary; APK/build output remains outside this runtime contract. |
| [PR #5](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/5) | Tailnet-only phone health bridge, SFTP template, and Vultr host bind/firewall boundary. |
| [PR #6](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/6) | Three tiers, local Gemma → Vultr → explicit Gemini/Spark escalation, redacted routing metadata, and operator gates. |
| [PR #7](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/7) | Pixel baseline, small Gemma starting point, battery/thermal tests, offline defer behavior, and device-only model artifacts. |
| [PR #8](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/8) | Ollama gateway, optional Letta/pgvector profile, local coder boundary, private Compose network, cost hygiene, and separate MCP sidecar. |
| [PR #9](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/9) | Allowlisted Android capabilities, authenticated phone broker, MCP-as-command-plane, optional Zenoh event-plane separation, and fail-closed simulation. |
| [PR #10](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/10) | Evidence discipline: open PRs are not merged proof, Drive/archive pointers remain pointers, and no phone/Vultr live status is inferred. |

## 13. Open decisions

These decisions are intentionally left to the implementation/operations
review and MUST be recorded before the corresponding tier is admitted:

- Which Android app/runtime and exact Gemma artifact will be used on the
  target phone?
- Is the production phone transport native MCP, a Termux HTTP adapter, or a
  narrowly scoped combination?
- Which Tailscale ACL tags and application-auth mechanism are approved?
- Which Vultr plan, region, model tag/digest, and gateway auth are approved?
- Which Letta version/API and retention policy are acceptable?
- What redaction/data-classification policy authorizes a Spark hop?
- Is SFTP needed, and what account, host key, directory, size, and retention
  limits apply?
- Will Zenoh remain an optional event plane, and which router owns it?

Until these are answered, the corresponding item remains a proposal or
future operator test—not a claim that the mesh is running.

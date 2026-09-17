# Basic-tier specification

Status: proposed  
Scope: off-cloud mesh control and inference path  
Normative language: **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are
requirements for a conforming implementation.

## Actors and terms

- **Phone** — an approved Android/Termux node. Basic treats its MCP surface
  as a health probe, not a general phone automation service.
- **Vultr host** — a headless VPS running the selected local inference backend.
- **Letta** — an optional memory manager on the Vultr host, using local
  Postgres/pgvector and the local inference endpoint.
- **Spark** — the Vesper persona served by an explicitly configured Gemini API
  project. Spark is an escalation target, not the default model.
- **Tailnet** — the Tailscale network and its ACL/device identity policy.
- **Basic request** — a bounded text request that is allowed by the data policy
  for the selected tier.

## Requirements

### R1. Local-first routing

The router MUST choose the lowest permitted tier in this order:

1. an approved local phone runner, if one exists and is healthy;
2. the approved Vultr endpoint, if the request is allowed on the VPS;
3. Spark, only when escalation is explicit and policy-approved.

The router MUST return a structured refusal or deferred result when no tier is
allowed. It MUST NOT silently send a phone request to Spark because a local
runner is slow or unavailable.

Every routed request MUST have a request ID, a bounded input, a selected
policy/tier, and a redacted outcome. Logs MUST record `tier_requested`,
`tier_used`, model identifier, latency, and failure class without API keys,
credentials, raw private prompts, or raw private responses.

### R2. Tailscale mesh boundary

The phone, Vultr host, and approved operator clients MUST communicate over
Tailscale or a directly equivalent authenticated tailnet path.

The implementation MUST:

- bind phone health and Vultr inference listeners to loopback or a `100.x`
  tailnet address, never a public wildcard address;
- enforce Tailscale ACLs for each required device, port, and direction;
- allow only the minimum phone health and Vultr inference paths;
- pin SSH/SFTP host keys before any artifact transfer; and
- keep Tailscale auth keys, SSH keys, and enrollment material outside Git.

### R3. Headless Vultr inference

The Vultr host MUST run without a desktop or interactive operator session.
It MUST expose a private, OpenAI-compatible inference surface with:

```text
GET  /health
GET  /v1/models
POST /v1/chat/completions
```

The backend MAY be Ollama, vLLM, or another reviewed local backend compatible
with the selected model. The deployment MUST pin the backend image and model
choice in the deployment record, set request/context limits, and keep the
service unreachable from the public interface.

Provisioning, resizing, destruction, and model pulls MUST be explicit
operator actions. The implementation MUST record hourly price, storage and
transfer assumptions, and a stop/destroy action against the available credit
before a paid pilot.

### R4. Letta memory is optional and local

Letta MUST be disabled by default in Basic. When enabled, it MUST:

- run on the Vultr host behind the tailnet boundary;
- use the local Postgres/pgvector store;
- use the local Vultr inference endpoint rather than a cloud model key;
- use a deployment-only database password; and
- avoid storing raw credentials, unredacted secrets, or disallowed private
  content.

Letta health or memory failure MUST degrade to stateless Vultr inference or a
clear error. It MUST NOT trigger automatic Spark escalation.

### R5. Phone MCP is health-only

The Basic phone surface MUST implement only:

```text
GET /health -> runner, model_id, device_id, ready
```

The health response MUST be bounded, non-sensitive, and sufficient to
distinguish ready, unavailable, and misconfigured states. A Basic deployment
MUST NOT expose SMS, camera, contacts, location, notifications, flashlight,
shell/filesystem, UI automation, arbitrary Android intents, or model tool
execution through phone MCP.

The phone health service MUST be independently testable offline. CI MUST use a
fixture or local stub and MUST NOT require a real phone, send a message, or
invoke a phone action.

### R6. Spark escalation

Spark escalation MUST require all of the following:

1. an explicit request or a documented policy decision;
2. a configured, approved Gemini API project and model;
3. the Vesper system-prompt reference;
4. an approved, redacted request envelope; and
5. an allowed persona/account mapping (`vesper` / `gmail_algy-alpen`).

The adapter MUST reject CMV names, CMV Gmail addresses, unknown persona/account
combinations, missing prompt references, missing configuration, and data that
is not approved for Google processing. It MUST return a clear unavailable
result when Gemini cannot be reached; it MUST NOT fall back to CMV or hide the
escalation.

Gemini keys MUST be deployment secrets, never repository content or log data.
Escalation logs MUST retain only request ID, reason code, model ID, latency,
and redacted error class.

### R7. Secret and artifact hygiene

The repository MUST contain documentation and placeholders only. It MUST NOT
contain Tailscale/Vultr/Gemini/Letta credentials, SSH private keys, model
weights, APK/AAB files, native binaries, unredacted prompts, or private
message content.

Large Drive artifacts MUST remain referenced pointers. Basic MUST NOT unpack,
read, or reconstruct `CONV2_B`.

### R8. Explicit non-goals

An implementation claiming Basic conformance MUST NOT add Ansible, CMV
integration, `CONV2_B` handling, or Cursor/Cursor Cloud runtime dependence.
It MUST NOT interpret this specification as authorization to provision paid
infrastructure or send phone messages.

## Acceptance criteria

### A1. Contract and docs

- All four files in `specs/openspec/basic/` exist.
- The docs link the source decisions to PRs #5–#10 and identify those PRs as
  design evidence rather than proof of a live deployment.
- `git diff --check` passes.

### A2. Tailnet-only reachability

In a disposable test environment:

- an authorized tailnet peer can reach phone `:8081/health`;
- an authorized tailnet peer can reach Vultr `/health` and `/v1/models`;
- the public interface cannot reach the phone or Vultr inference listener;
- ACLs show no broader phone capability than health; and
- any SFTP transfer rejects an unknown host key.

Evidence MUST include the tested listener addresses and ACL revision, but MUST
NOT include secret values.

### A3. Headless inference

- The Vultr backend answers `/health`, `/v1/models`, and one bounded
  `/v1/chat/completions` request from an authorized peer.
- The selected image/model and request limits are recorded.
- A restart or backend failure returns a bounded error rather than a hang.
- Cost evidence records the hourly rate, credit burn estimate, and stop/destroy
  decision.

### A4. Letta isolation

- A default startup does not start Letta or expose its port.
- An explicit opt-in starts Letta and its database on the private interface.
- Letta can use the local inference endpoint without a cloud provider key.
- A simulated Letta failure yields stateless inference or a clear error and
  does not call Spark.

### A5. Phone health-only

- A local fixture returns the documented health fields and state transitions.
- A real-device smoke test, if performed, checks only `/health` over the
  tailnet.
- An attempted SMS, camera, shell, arbitrary-intent, or tool-execution path is
  absent or rejected.
- CI completes with the phone offline and performs no phone side effect.

### A6. Spark gate

- A redacted, explicitly approved request reaches the configured Gemini API
  adapter and returns a response.
- Logs and failure fixtures contain no key, raw private prompt, raw response,
  or Gmail credential.
- Missing approval, configuration, redaction, or prompt reference is rejected.
- Gemini unavailability returns a clear Tier C error and never routes to CMV.

### A7. Prohibited-scope scan

Before release, a repository scan and diff review confirm there is no:

- Ansible playbook or Ansible execution path;
- `CONV2_B` unpack/reconstruction or extracted conversation payload;
- CMV account, CMV Gmail, or CMV routing;
- secret/key material, APK/AAB, binary, or model-weight artifact; or
- Cursor/Cursor Cloud serving dependency.


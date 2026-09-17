# Basic-tier design

## 1. Topology

```text
                         Tailscale tailnet
        ┌────────────────────────────────────────────────┐
        │                                                │
        │  approved phone                                │
        │  health :8081                                  │
        │       │                                        │
        │       ├── health probe only                    │
        │       │                                        │
        │  operator/router ───────► Vultr host           │
        │       │                    inference :8000     │
        │       │                    /v1 + /health       │
        │       │                         │              │
        │       │                    optional Letta      │
        │       │                    :8283 + pgvector   │
        │       │                         │              │
        │       └── explicit policy gate ────────────────┼──► Spark/Vesper
        │                                                │    Gemini API
        └────────────────────────────────────────────────┘
```

The phone is an admission and liveness boundary in Basic, not an automation
surface. The Vultr host is the default headless inference fallback. Spark is a
separate, outbound cloud boundary that requires a decision at the router.
Cursor may be used to edit or review this repository, but it is not in the
serving path.

## 2. Components

### 2.1 Phone health bridge

The phone runs a small service on `:8081`, bound to localhost or its Tailscale
IPv4 address. Its only Basic endpoint is:

```http
GET /health
```

Example shape:

```json
{
  "runner": "phone-bridge",
  "model_id": "local-model-reference",
  "device_id": "approved-device-reference",
  "ready": true
}
```

`model_id` and `device_id` are references, not secrets. The endpoint does not
accept prompts, tool calls, files, or Android intents. It may report that a
runner is ready, but Basic does not route inference through a phone MCP
request. This keeps the phone contract useful for admission without granting
remote control.

### 2.2 Tailscale and ACLs

Tailscale supplies node identity and encrypted reachability. The initial ACL
shape is:

| Source | Destination | Port/path | Purpose |
| --- | --- | --- | --- |
| approved operator/router | phone | `8081 /health` | liveness and admission |
| approved operator/router | Vultr | `8000 /health`, `/v1/*` | inference |
| approved sidecar | Olette-box | SSH/SFTP | bounded artifact handoff |
| Vultr | Gemini API | outbound HTTPS, if approved | Spark escalation |

The actual tags, node IDs, addresses, and host fingerprints are deployment
configuration. They do not belong in this repository. Public-interface
firewall rules deny the phone and inference listeners. A tailnet address is
not sufficient by itself: ACLs and application-level authentication remain
required where supported.

### 2.3 Vultr inference host

The host is a headless Linux VPS. A reviewed deployment may use Ollama with a
small quantized model as the baseline, or another local backend selected for
the instance. The public network interface is not a service interface.

The private service contract is:

```text
GET  /health
GET  /v1/models
POST /v1/chat/completions
```

The gateway binds the Tailscale address and forwards to the local backend.
Backend model storage is a deployment volume and is never synchronized into
Git. A request envelope carries a request ID, model allowlist choice, bounded
context, timeout, and cancellation/deadline policy. The service returns
structured error classes for unavailable, over-limit, unauthorized, and
backend-failure cases.

Basic does not prescribe a Vultr plan. Before launch, the operator records
price, region, CPU/GPU, memory, disk, transfer, model digest, and the
credit-burn estimate. A CPU VPS is valid for a low-throughput baseline; GPU
use requires measured justification.

### 2.4 Optional Letta memory

Letta is an opt-in profile on the same private host:

```text
Letta :8283 ──► local Postgres/pgvector
     │
     └────────► local Ollama/OpenAI-compatible endpoint
```

The profile is off for the default startup. Its database volume and password
are deployment-only. Letta receives only content allowed by the request's data
policy. A memory lookup or write is bounded and associated with the request
ID. If Letta is unavailable, the router can continue statelessly on Vultr;
there is no implicit cloud escalation.

### 2.5 Router and tier selection

The router evaluates:

```text
health-only phone admission
        │
        ├─ request allowed on Vultr and backend healthy ─► Vultr
        │
        ├─ Spark explicitly requested/approved ─────────► Gemini
        │
        └─ otherwise ───────────────────────────────────► deferred/refused
```

Basic does not require a phone inference API. If a future local phone runner
is introduced, it must be admitted by a separate spec change and must not
expand the phone MCP endpoint implicitly.

The Spark envelope is explicit and redacted:

```json
{
  "persona": "vesper",
  "account_id": "gmail_algy-alpen",
  "tier": "gemini-api",
  "system_prompt_ref": "secret://prompts/vesper/version",
  "model": "approved-model-reference",
  "input": "approved-redacted-request",
  "allowed_tools": []
}
```

The account ID selects an approved identity; it is not a credential. The
adapter rejects CMV values, unknown identity mappings, missing prompt
references, and unapproved data.

## 3. Data and secret boundaries

### 3.1 Data flow

1. The router creates a request ID and applies the data/tier policy.
2. The phone may answer a health probe only.
3. An approved request goes to the private Vultr endpoint.
4. Optional Letta reads/writes local memory when that profile is enabled.
5. Only an explicitly approved, redacted request may cross to Spark.
6. The router records redacted decision metadata and returns the response or
   a bounded error.

SFTP is an optional durable artifact lane, not an inference transport. Use
`.part` then atomic rename, size/content allowlists, restrictive permissions,
retention, and pinned host keys. Do not put secrets or unredacted message
content into an SFTP envelope.

### 3.2 Secret storage

Secrets are injected by a deployment secret store or operator-controlled
environment outside the repository:

- Tailscale enrollment/auth material;
- Vultr credentials, if any;
- Letta/Postgres password;
- SSH private key and known-hosts data;
- Gemini API key; and
- the Vesper prompt reference/secret.

Templates use placeholders and must fail closed when required values are
missing. Logs redact headers, environment values, keys, private inputs, and
responses.

## 4. Failure behavior

| Failure | Basic behavior |
| --- | --- |
| Phone offline | Mark phone unavailable; do not invoke a phone action. |
| Public bind detected | Fail admission and do not serve inference. |
| Vultr backend unavailable | Return a bounded error or use an already-approved Spark decision; no silent escalation. |
| Letta unavailable | Continue statelessly on Vultr or return an error. |
| Tailnet ACL denied | Report unauthorized; do not retry through a public path. |
| Spark config/approval missing | Reject with a configuration/policy error. |
| Gemini unavailable | Return explicit Tier C unavailable; never use CMV. |
| Credit/cost threshold reached | Stop or isolate the host by operator action. |

Retries are bounded, carry the same request ID, and do not widen permissions
or change tiers.

## 5. Observability and rollback

Health checks are separate from inference success. Record:

- request ID and tier decision;
- service/model references;
- ready/unavailable state;
- latency, timeout, and failure class;
- redacted byte counts for SFTP, if used; and
- deployment image/model/prompt digests.

Do not record API keys, Gmail credentials, raw private prompts, raw responses,
SMS bodies, notification text, or private file contents in ordinary logs.

Rollback is configuration-first: disable Letta, stop the Vultr service, remove
the phone from the ACL, or disable Spark escalation. Destruction of a paid
resource and deletion of retained storage are explicit operator actions.

## 6. Verification approach

The first verification layer is offline and docs-safe:

- parse example JSON/YAML and validate placeholder shape;
- test the phone health fixture with the phone absent;
- test router decisions for local/Vultr/Spark/refused outcomes;
- scan for credentials and prohibited artifacts/terms; and
- run `git diff --check`.

The second layer is a disposable deployment:

- verify tailnet-only reachability and public denial;
- check Vultr `/health`, `/v1/models`, and one bounded completion;
- opt into Letta and verify local-only memory behavior;
- call phone `/health` only; and
- test explicit Spark approval and unavailable behavior with a disposable
  redacted request.


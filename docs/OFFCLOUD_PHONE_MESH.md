# Off-cloud phone mesh

Status: architecture and scaffold only. This document does not provision a
VPS, enroll a phone, download a model, or make a network request.

## Goal and non-goals

The mesh makes a Pixel phone a useful local inference node while retaining a
headless fallback for workloads that do not fit on the phone. Cursor and
Cursor Cloud may be used to edit this repository, but they are never a runtime
inference dependency.

This change intentionally does **not**:

- create or destroy Vultr resources;
- commit model weights, APKs, API keys, Tailscale auth keys, or `SKILL.md`;
- introduce CONV2_B, mouths, LangChain, or a new orchestration framework;
- claim that an unannounced Pixel SKU has a final RAM or accelerator
  configuration.

## Three inference tiers

```text
                   Tailscale tailnet
    +-------------------------------------------------------+
    |                                                       |
    |  Pixel 8a       Pixel 9a       Pixel 11 Pro (TBD)     |
    |  Tier A         Tier A         Tier A                 |
    |  Gemma local    Gemma local    Gemma local            |
    |      \              |                 /              |
    |       +-------- phone MCP :8081 ---------------------+
    |                         |                            |
    |                    SFTP drops                        |
    |                         |                            |
    |                 Vultr VPS, Tier B                    |
    |              OpenAI-compatible :8000                 |
    |                         |                            |
    +-------------------------+-----------------------------+
                              |
                 Tier C: Google AI Studio / Gemini API
                 Spark / Vesper only, explicit escalation
```

### Tier A: on-device Gemma

The phone is the first choice for short, private, low-latency work. The
runtime should be selected in this order:

1. **Google AI Edge LiteRT-LM / MediaPipe LLM Inference** for an Android
   integration with a maintained Google path, a quantized Gemma model, and
   bounded context.
2. **`llama.cpp` Android/JNI or its local HTTP wrapper** when a model or
   operator needs a more controllable backend. Keep it behind the same phone
   MCP contract so the orchestrator does not know which runner is active.
3. **Android AI Core/Gemini Nano APIs only as an optional device capability**.
   AI Core is a system service for supported on-device Gemini features; it is
   not assumed to be a generic Gemma loader or a substitute for the two
   runtimes above.

These are planning targets, not benchmark claims. The shipped model must be
chosen from an Android-compatible, signed, quantized artifact and measured on
the exact device.

| Device | Planning hardware | Default local model target | Guardrail |
| --- | --- | --- | --- |
| Pixel 8a | Tensor G3, 8 GB RAM | Gemma 3 1B or Gemma 2 2B, int4 | Keep context and KV cache small; CPU/GPU fallback is acceptable. Do not plan on an 8B model. |
| Pixel 9a | Tensor G4, 8 GB RAM | Same 1B/2B int4 baseline; test Gemma 3 4B int4 as an experiment | Thermal and memory tests decide whether 4B is retained. The baseline must remain usable. |
| Pixel 11 Pro | Final SKU and RAM must be verified at purchase; plan against a 12 GB-class device only as a provisional assumption | Gemma 3 4B int4 or the current supported equivalent; test 8B only after measurement | Do not encode a rumored Tensor generation, RAM size, or NPU API into the control plane. |

RAM numbers above are capacity planning inputs, not available model memory:
Android, the MCP bridge, the runner, the context/KV cache, and the display all
consume the same physical memory. A model is accepted only when a cold start,
10-turn bounded conversation, cancellation, and thermal soak pass on each
device.

The phone runner exposes a narrow contract:

```text
GET  /health       -> runner, model_id, device_id, ready
POST /v1/chat      -> bounded request/response envelope
POST /v1/cancel    -> cancel an in-flight request
```

The existing Termux MCP bridge health endpoint is `:8081/health`. Keep that
listener on localhost or the Tailscale interface; never publish it to the
public internet.

### Tier B: Vultr headless inference VPS

Tier B is the shared, headless fallback for longer context, batch work,
concurrency, and models that do not fit comfortably on a phone. The monthly
Vultr credit is spent here, with a GPU instance preferred when the measured
workload justifies it. A CPU instance is a valid bootstrap and low-throughput
fallback; it is not a promise of acceptable latency for every model.

The initial server shape is:

- Tailscale on the host, with SSH disabled in Tailscale unless an operator
  explicitly enables it;
- Docker Compose running one inference backend;
- an OpenAI-compatible endpoint on the tailnet, normally `:8000/v1`;
- vLLM for a compatible GPU image, or Ollama/`llama.cpp` server when the
  selected model and instance make those a better fit;
- an explicit model allowlist and request limits;
- no public listener for the inference API.

`bridges/vultr/` contains templates, not a deployment. The template uses
placeholders for `VULTR_API_KEY` and `TS_AUTHKEY`; the Vultr API key belongs in
the provisioning operator's secret store and the Tailscale auth key is
single-use/short-lived where the Tailscale policy permits. Neither value is
needed by the model process.

The VPS should return an OpenAI-compatible shape so phone, local CLI, and
future non-Cursor orchestrators can share a client:

```text
GET  /health
POST /v1/chat/completions
GET  /v1/models
```

Gemini-compatible translation is an adapter concern, not a reason to give
the VPS a Google API key. Tier B must remain useful if Google is unavailable.

### Tier C: Gemini API / AI Studio

Tier C is the explicit cloud escalation for Spark/Vesper and for requests
whose privacy, latency, model-size, or multimodal requirements exceed Tier A
and Tier B. It uses a Google AI Studio project and Gemini API credential
outside the repository. It does not use CMV Gmail and does not make Cursor
the serving path. See [`SPARK_GEMINI.md`](SPARK_GEMINI.md).

Escalation is policy-driven:

```text
phone Gemma can satisfy request?
  yes -> Tier A
  no, VPS policy/model available?
    yes -> Tier B
    no, request is approved for Spark/Vesper?
      yes -> Tier C
      no -> queue for an operator / return a structured refusal
```

The router records `tier_requested`, `tier_used`, `model_id`, latency, and
failure class. It does not record API keys or raw sensitive prompts in
ordinary health logs.

## Control plane and transport

### Tailscale

Tailscale is the network identity and reachability layer for phones, the VPS,
and the existing `olette-box` endpoint. ACLs should permit only the required
tailnet tags and ports:

| Link | Purpose | Exposure |
| --- | --- | --- |
| Phone MCP `:8081` | Termux bridge and health | Tailscale/local only |
| VPS inference `:8000` | OpenAI-compatible inference | Tailscale only |
| SFTP `100.115.0.111:22` | Job/artifact drops to `olette-box` | Tailscale only; pin host key |
| Linear API/MCP | MIS-6/MIS-7 work tracking | Outbound from operator/control plane |

The concrete `olette-box` address is included because it is already proven:
`100.115.0.111:22`. Operators must still verify the host key and tailnet
membership before sending a drop.

### MCP

MCP is the control and tool surface, not the model runtime:

- the phone exposes the existing Termux MCP bridge;
- the VPS can expose an MCP adapter for model health, queue state, and job
  submission;
- clients call a stable tool contract and receive `device_id`, `tier`, and
  `model_id` in results;
- no MCP tool should silently promote a Tier A request to Tier C.

### SFTP drops

SFTP is for durable handoff of bounded job envelopes and artifacts when a
long-lived HTTP stream is not appropriate. Recommended layout:

```text
mesh-drop/
  inbox/<job-id>/request.json
  working/<job-id>/status.json
  outbox/<job-id>/response.json
  outbox/<job-id>/artifacts/*
```

Use restrictive permissions, atomic upload (`.part` then rename), a
content-type/size allowlist, and a retention job. Do not place secrets or
unredacted credentials in a job envelope.

### Linear / MIS

Linear records decisions and acceptance evidence, not prompt contents or
secrets. MIS-6 covers the offline harness and phone bridge; MIS-7 can cover
the first real device/VPS pilot. Every pilot ticket should identify the
device SKU, runner/model digest, tier used, tailnet ACL revision, and a
rollback path.

## Identity map

Identity and transport are separate. The account ID selects an identity for
an approved connector; it never grants a model permission to discover other
accounts.

| Persona | Account ID | Runtime use |
| --- | --- | --- |
| Otr | `${OTR_COMPOSIO_ACCOUNT_ID}` (deployment secret/config; fill from the authoritative account registry) | Orchestration/control-plane identity |
| Liv | `${LIV_COMPOSIO_ACCOUNT_ID}` (deployment secret/config; fill from the authoritative account registry) | Operator/dev identity |
| Vesper / Spark | `gmail_algy-alpen` | Gemini API / AI Studio path only, using `vesper.mae.blackwell@gmail.com` as the persona address |

The Otr and Liv placeholders are intentional: this archive does not invent
account IDs. Vesper's supplied Composio account ID is the only concrete ID in
scope. **Never route this mesh through a CMV account or CMV Gmail.** Do not
copy Gmail credentials into a phone, VPS, SFTP drop, or model prompt.

## Operational gates

Before a device is admitted:

1. Confirm the exact Pixel SKU, RAM, Android build, battery/thermal policy,
   and model license.
2. Install the runner from a reproducible build or signed artifact; keep APKs
   outside this repository.
3. Verify `:8081/health` from the tailnet and reject a public-interface bind.
4. Run cold-start, cancellation, bounded-context, offline, and thermal tests.
5. Verify Tailscale ACLs and the pinned SFTP host key.
6. Store only secret references in Linear; attach redacted latency/results.

Before the VPS is admitted:

1. Dry-run the provisioning template and estimate GPU/CPU, disk, egress, and
   model-storage spend against the $250 credit.
2. Confirm only the Tailscale interface can reach `:8000`.
3. Pin the backend image and model digest in the deployment record.
4. Test `/health`, `/v1/models`, timeouts, cancellation, and restart recovery.
5. Destroy/scale resources only through an explicitly reviewed operator action;
   this PR performs no Vultr API action.

## Repository pointers

- Vultr templates: [`../bridges/vultr/`](../bridges/vultr/)
- Pixel/Termux notes: [`../bridges/pixel/`](../bridges/pixel/)
- Spark/Vesper policy: [`SPARK_GEMINI.md`](SPARK_GEMINI.md)
- Existing offline phone MCP implementation:
  [`harness/src/sovereign_harness/phone_mcp.py`](../harness/src/sovereign_harness/phone_mcp.py)
- Existing AI Studio → GitHub-connected Apps launcher:
  [`ai-studio-launcher/MODULE.md`](../skill_tree/skills/olivia-dev-alpha/references/integrations/ai-studio-launcher/MODULE.md)
- Existing APK hygiene / AI Studio binary handoff notes:
  [`apk-hygiene-sub/REPORT.md`](../skill_tree/skills/olivia-dev-alpha/references/sync_state_2026-08-06/coding-sub-driver-2026-08-13/apk-hygiene-sub-2026-08-13/REPORT.md)

The AI Studio launcher is a phone-tap path into GitHub-connected Apps; it is
not an inference dependency for this mesh. APK build output stays outside
Git, consistent with the hygiene notes.

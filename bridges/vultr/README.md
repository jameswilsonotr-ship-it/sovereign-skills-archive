# Vultr tailnet-only inference VPS

This directory contains deployment templates for a Vultr VPS running a
tailnet-only, headless inference box. The default path is Ollama plus a small
Caddy gateway. Optional Compose profiles add a Letta memory manager and a
dependency-free local coding helper:

- Ollama is reachable only on the private Compose network.
- Caddy binds the host's Tailscale `100.x` address only.
- `/health`, `/api/tags`, and Ollama's `/v1` compatibility endpoints are
  reachable from the tailnet, not from the public interface.
- Letta and its pgvector-backed database are off by default (`letta` profile).
- `coder` is a one-shot text-in/text-out client for the same local Ollama
  endpoint (`coder` profile); it does not edit files or execute commands.

These are templates only. This agent did not create, resize, start, or
destroy a Vultr resource and made no paid API call. Replace every
`__PLACEHOLDER__` through a secure deployment path; never commit replacement
values.

## Which model and machine?

Start by choosing the model and then sizing for its quantized weights plus
runtime context. Names and availability change, so confirm the current
Ollama tags and Vultr catalog before launch.

| Workload | Starting point | Trade-off |
| --- | --- | --- |
| Low-duty chat, embeddings, or development | CPU VPS with a small quantized `gemma3` or `qwen3` model | Lowest hourly burn; materially higher latency and lower concurrency |
| Interactive 4B--8B chat | GPU VPS with enough VRAM for the selected quantization | Better latency; GPU stock and hourly price vary by region |
| Larger context, multiple users, or 12B+ | GPU with headroom for weights, KV cache, and concurrency | A $250 credit balance can be consumed quickly; benchmark before keeping it running |

`gemma3:4b` is a conservative default for the templates. `qwen3:8b` is
an alternative when the selected machine has sufficient RAM/VRAM. Do not
assume that a model fits because its parameter count fits: quantization,
context length, Ollama overhead, and concurrent requests all consume memory.
For a GPU deployment, uncomment the GPU device reservation in
`docker-compose.yml` and verify the image/runtime supports that GPU. For a
CPU deployment, leave it commented.

## Region selection

Pick the currently offered region closest to the phone, MCP callers, and
Olette-box network path. Typical choices to compare in the Vultr panel
include New Jersey, Chicago, Dallas, Los Angeles, Amsterdam, Frankfurt,
London, Singapore, and Tokyo; the GPU catalog is not uniform across those
regions. Prefer the region with confirmed GPU stock and acceptable tailnet
latency over a nominally closer region with no stock.

Before committing credit, record:

1. hourly price and estimated `hours = 250 / hourly_price`;
2. GPU type, VRAM, system RAM, disk, and included transfer;
3. storage, snapshot, bandwidth, and tax/overage terms; and
4. whether the instance can be destroyed without retaining billable
   attached storage.

The estimate is only arithmetic, not a price quote. Prices, credits,
availability, and billing behavior are Vultr-account and catalog dependent.
Stop or destroy the VPS when it is not being tested, and separately check
whether a retained volume or snapshot continues to incur charges.

## Files and deployment shape

- [`cloud-init.yaml`](cloud-init.yaml) installs Docker and Tailscale, joins
  the tailnet with an injected `TS_AUTHKEY`, stages this directory, and
  validates or starts Compose according to an explicit `RUN_COMPOSE_UP` flag.
- [`docker-compose.yml`](docker-compose.yml) is the repeatable deployment:
  core Ollama inference is enabled by default, while `letta` and `coder` are
  opt-in profiles.
- [`Dockerfile.coder`](Dockerfile.coder) and [`coder.py`](coder.py) implement
  the no-key local fallback.
- [`.env.example`](.env.example) lists deployment-only values. Copy it to
  `.env`; never commit the copy.
- [`mcp-sidecar.md`](mcp-sidecar.md) describes the separate MCP sidecar path
  to the phone on port `8081` and to Olette-box over SFTP.
- [`cloud-init.mcp-host.example.yaml`](cloud-init.mcp-host.example.yaml) and
  [`mcp-host.config.example.json`](mcp-host.config.example.json) remain the
  older MCP-host-only templates from the offline bridge.

Create a deployment-only `.env` next to the compose file. It should contain
values such as `TAILNET_IP=100.x.x.x`, `VULTR_REGION=__VULTR_REGION__`,
`VULTR_INSTANCE_ID=__VULTR_INSTANCE_ID__`, and
`OLLAMA_MODEL=gemma3:4b`; it must not be committed. `TS_AUTHKEY` is consumed
by cloud-init and is intentionally not part of the compose environment.

The compose gateway exposes Ollama's OpenAI-compatible API at
`http://100.x.x.x:11434/v1`. A client can use that base URL with the dummy
`ollama` API key if its SDK requires one; Ollama does not validate that key by
default. Keep that URL tailnet-only and add application-level authentication
before allowing untrusted tailnet users to reach it.

## Spin up manually

These commands assume Docker, the Compose plugin, and Tailscale are already
installed on the VPS. They do not create a Vultr resource:

```sh
cp .env.example .env
# Edit .env: set the actual 100.x TAILNET_IP, a random Letta password if
# needed, and an absolute CODER_WORKSPACE path.
docker compose config --quiet
docker compose up -d
docker compose exec ollama ollama pull "${OLLAMA_MODEL:-gemma3:4b}"
```

The model download is the one intentional large transfer. It is cached in
the `ollama-data` volume; do not put `ollama pull` in a restart loop. Add
Letta only when needed:

```sh
docker compose --profile letta up -d
curl --fail "http://${TAILNET_IP}:8283/health"
```

The Letta image is the legacy Docker server surface in current Letta
documentation, but it is retained here because the requested pattern is a
containerized memory manager. Set `OLLAMA_BASE_URL` through the Compose file;
no cloud provider key is required. Select the local Ollama model when creating
an agent according to the Letta version installed.

For a simple text coding turn, start the core service and run the local
helper against a checked-out workspace:

```sh
docker compose --profile coder run --rm \
  -e CODER_WORKSPACE=/workspace \
  coder --prompt "Explain the error and suggest a minimal patch." \
  --file path/inside/workspace/file.py
```

The helper only returns text. It does not apply a patch, run tests, or grant
the model shell access. A caller such as Hi or Cursor can use the same
tailnet URL directly:

```sh
set -a; . ./.env; set +a
curl "http://${TAILNET_IP}:11434/v1/chat/completions" \
  -H 'Authorization: Bearer ollama' \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma3:4b","messages":[{"role":"user","content":"Summarize this function."}]}'
```

### Optional Grok Build CLI

xAI publishes a public Grok Build CLI (`grok`) with interactive and
headless modes. Its official install is documented at
<https://docs.x.ai/build/overview>:

```sh
curl -fsSL https://x.ai/cli/install.sh | bash
grok --version
grok -p "Explain this codebase"
```

That CLI uses xAI's service and therefore can consume paid/cloud quota; it is
not wired into this Compose stack and no `XAI_API_KEY` belongs in this repo.
For offline or cost-controlled turns, use the `coder` profile or the
OpenAI-compatible Ollama URL above instead.

## Bandwidth and cost hygiene

- Start with the cheapest Vultr plan that fits the selected quantized model.
  CPU plus a small model is the default cost experiment; choose a small GPU
  only after measuring latency and memory pressure.
- Do not auto-provision, resize, or destroy a Vultr resource from these
  templates. Review the plan, region, hourly price, transfer allowance, and
  retained-volume billing in the Vultr panel first.
- Treat the `$250` credit as a hard cap, not a target. Record
  `hours = 250 / hourly_price`, set an account alert, and stop/destroy the
  VPS plus inspect volumes and snapshots when testing ends.
- Pull images once, keep them cached, and pull one tagged model only. Avoid
  `docker compose pull` and model re-downloads on every boot.
- Keep prompts, context files, and output concise. Reuse Letta memory instead
  of repeatedly sending a full repository through a cloud model.
- Keep ports 11434 and 8283 on the Tailscale interface. The public interface
  should not be able to reach either service.
- Use `docker compose down` for a temporary stop and separately verify
  whether any attached storage or snapshot remains billable.

## Safety checks before use

- Review the Tailscale ACL, device expiry policy, and hostname.
- Confirm the listener is a `100.64.0.0/10` address, never `0.0.0.0`.
- Test from a tailnet peer with `/health` and `/api/tags`.
- Confirm the public interface cannot reach port `11434`.
- Pull only the model you selected and remove unused model layers.
- Keep auth keys, SSH keys, Vultr tokens, and SFTP contents outside Git.

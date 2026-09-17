# Vultr tailnet-only inference VPS

This directory contains deployment templates for a Vultr VPS running
Ollama with an OpenAI-compatible `/v1` surface. The default path is Ollama
plus a small Caddy gateway:

- Ollama listens on loopback inside the VPS.
- Caddy listens on the VPS's Tailscale `100.x` address only.
- `/health`, `/api/tags`, and Ollama's `/v1` compatibility endpoints are
  reachable from the tailnet, not from the public interface.

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
  the tailnet with an injected `TS_AUTHKEY`, starts Ollama and the gateway,
  and binds inference to the tailnet address.
- [`docker-compose.yml`](docker-compose.yml) is the repeatable equivalent
  after the VPS has been bootstrapped. It contains placeholders only.
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
`http://100.x.x.x:11434/v1`. A client can use that base URL with a dummy
API key if its SDK requires one; Ollama does not validate that key by
default. Keep that URL tailnet-only and add application-level authentication
before allowing untrusted tailnet users to reach it.

## Safety checks before use

- Review the Tailscale ACL, device expiry policy, and hostname.
- Confirm the listener is a `100.64.0.0/10` address, never `0.0.0.0`.
- Test from a tailnet peer with `/health` and `/api/tags`.
- Confirm the public interface cannot reach port `11434`.
- Pull only the model you selected and remove unused model layers.
- Keep auth keys, SSH keys, Vultr tokens, and SFTP contents outside Git.

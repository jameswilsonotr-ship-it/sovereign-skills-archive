# Vultr/Letta bridge healthchecks

This directory contains offline checks for a future Vultr-hosted Ollama +
Letta bridge. The checks do not contact Vultr, Tailscale, Ollama, Letta, DNS,
or any other network service.

## Contract

If a Compose file is added next to this document, it must define services
named `ollama` and `letta` with these TCP container ports:

| Service | Container port | Purpose |
| --- | ---: | --- |
| `ollama` | `11434` | Ollama HTTP API |
| `letta` | `8283` | Letta server HTTP API |

Both services must also have a non-disabled Compose `healthcheck`. The
healthcheck command should probe the service locally inside its container. For
example, use the image-supported equivalent of:

```yaml
healthcheck:
  interval: 30s
  timeout: 5s
  retries: 5
  start_period: 20s
  test: ["CMD-SHELL", "ollama list >/dev/null 2>&1"]
```

for Ollama, and an image-supported local request to Letta's health endpoint
for the Letta service. Pin the image versions before selecting the exact
command; do not assume that `curl` is installed in every image.

The offline validator also rejects wildcard host bindings. If a service needs
to be published on the host, bind it to `127.0.0.1` (or an explicitly
configured tailnet address), never an unspecified `0.0.0.0`/`::` listener.
Container-only networking is preferred.

## Run the check

```bash
./bridges/vultr-letta/offline-healthcheck.sh
```

The script finds `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`,
or `compose.yaml` in this directory. A different file can be selected with:

```bash
COMPOSE_FILE=/path/to/compose.yml \
  ./bridges/vultr-letta/offline-healthcheck.sh
```

It runs `docker compose config` only, then inspects the rendered local JSON
configuration. It never starts containers or performs health probes. Exit
status `0` means the declared configuration satisfies this contract; `1`
means the Compose configuration is invalid; `2` means the offline check could
not run, including when no Compose file exists.

There is currently no Compose file in this repository, so the check is
intentionally fail-closed until one is supplied.

## Tailscale fail-closed notes

Compose validation is not a tailnet readiness check. A passing result must
not be used as evidence that a Vultr host is reachable or safe to expose.

Before allowing remote access, the operator must separately verify that:

1. Tailscale is connected and the intended tailnet identity is present.
2. Host firewall rules allow the bridge ports only on the tailnet interface.
3. No public-cloud firewall rule exposes ports `11434` or `8283`.
4. The bridge remains unavailable if Tailscale is disconnected.

Do not add a Tailscale auth key, state directory, private address, or other
secret to this repository. The offline script deliberately does not invoke
the Tailscale CLI, inspect a live interface, or make a Vultr call.

# atom-vg-03-tailscale-ingress

Atomic docs placeholder for the `add-vultr-headless-gateway` parent.

## Ingress placeholder

- Coding control ingress is Tailscale-only.
- Do not add public SSH or HTTP bindings, public fallback routes, real hostnames,
  IP addresses, or auth keys in this stub.
- The eventual health probe must originate from the approved tailnet path.

## Healthcheck notes

- Keep Tailscale reachability and the Letta/Ollama service checks as separate
  readiness conditions.
- A missing, expired, or unreachable tailnet route is unhealthy; do not report
  a healthy gateway through a public fallback.
- Letta and Ollama endpoint details remain placeholders until a later,
  explicitly approved implementation.
- This file makes no Tailscale changes, network calls, provisioning actions, or
  spend.

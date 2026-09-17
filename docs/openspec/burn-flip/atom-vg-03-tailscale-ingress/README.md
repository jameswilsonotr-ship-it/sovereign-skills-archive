# atom-vg-03-tailscale-ingress

Dual-ingress amendment to the stale Tailscale-only atom under
`add-vultr-headless-gateway`.

## Ingress

- Public HTTPS MCP uses the Vesper/Gemini Connected Apps join path. This
  placeholder intentionally invents no hostnames or URLs.
- Tailscale is the coding and SSH control path.
- Public SSH MUST NOT be used as coding control or as a fallback.

## Healthcheck placeholders

- `ollama list`
- `GET http://127.0.0.1:8283/v1/health`

These checks are placeholders only; they do not provision or expose anything.

## Paper gate

Paper GO records approval to plan; it is not provision, spend, credential
issuance, or a network change. This atom changes no live systems and adds no
credentials, spend, or `SKILL.md`.

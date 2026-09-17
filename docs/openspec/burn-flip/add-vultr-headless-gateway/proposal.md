# Proposal: add-vultr-headless-gateway

## Why

After included burn reaches ~80% (or reset), coding flips to a Vultr headless gateway. Need paper + stub now for `vc2-1c-2gb` ORD `mcp-vultr`: Docker + Letta + Ollama, Tailscale-only ingress — clearly **not** Cold Steel.

## What Changes

- Add `vultr-gateway` capability: instance paper target, stack composition, Tailscale-only ingress, Steel exclusion.
- Live provision/spend steps gated on Bunny YES (Olette asks).
- No invented IPs or API keys.

## Capabilities

| Capability | Mode |
|------------|------|
| `vultr-gateway` | ADDED |

## Impact

- Enables later `burn-flip-cutover` to point active coding at Vultr.
- Iron Pearl BASIC SPEC-001 gateway role only; Cold Steel bare-metal remains separate.
- Provision, API, and spend actions require Bunny YES.

# Design: add-vultr-headless-gateway

## Context

Iron Pearl BASIC SPEC-001 names Vultr `vc2-1c-2gb` ORD `mcp-vultr` as cloud gateway. COLD STEEL = physical bare-metal edge (GMKtec K15, Jetson Orin Nano, HP EliteDesk Ashtabula). This slice papers/stubs the gateway only.

## Goals

- Spec + stub for Docker + Letta + Ollama on Vultr ORD `vc2-1c-2gb`.
- Tailscale-only ingress.
- Explicit Vultr != Cold Steel.
- Bunny YES gate on any live provision/API/spend action.

## Non-Goals

- Do not create/edit/overwrite any `SKILL.md` / skill-tree live lock files (Willow write lock).
- No bare-metal Cold Steel work in this slice.
- No inventing Vultr IPs, API keys, or spend amounts.
- No CONV2_B unpack; never CMV; girl-team not fifth mouths.
- No vibe; no Google Docs.
- Do not re-litigate PR #11 zenoh.
- No live provision, API call, or spend without Bunny YES (Olette must ask).

## Decisions

1. **Plan/region/label:** `vc2-1c-2gb` / ORD / `mcp-vultr`.
2. **Stack:** Docker + Letta + Ollama.
3. **Ingress:** Tailscale-only default; no public coding ingress as default.
4. **Paper-first:** stubs and compose files OK; create-instance requires Bunny YES.
5. **Identity:** Vultr = gateway != Steel.

## Risks

| Risk | Mitigation |
|------|------------|
| Accidental public expose | Tailscale-only MUST in spec |
| Premature spend | Bunny YES halt on provision/API/spend tasks |
| Steel scope creep | Explicit Non-Goal + scenario |

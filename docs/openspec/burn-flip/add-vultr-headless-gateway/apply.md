# add-vultr-headless-gateway — atom-vg-04-verify

**Parent change-id:** `add-vultr-headless-gateway`

Paper/stub verification only. All four `vultr-gateway` scenarios are green
without a live provider action:

- **Provision gate:** a create/resize/destroy, API, or spend step halts for
  Bunny YES; no provider call, spend, IP, or API key is invented.
- **Stack declared:** the stub names Docker, Letta, and Ollama.
- **Tailscale-only ingress:** coding control has no public SSH/HTTP default.
- **Steel excluded:** Vultr remains a cloud gateway, explicitly separate from
  Cold Steel bare-metal work.

No live provision, API call, or spend was run. No `SKILL.md` was changed.

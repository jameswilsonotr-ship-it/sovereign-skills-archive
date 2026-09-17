# OpenSpec: Off-cloud mesh, Basic tier

## Summary

Define a small, local-first inference mesh that can operate without Cursor
included quota:

```text
phone health/control boundary
          │ Tailscale
          ▼
Vultr headless inference + optional Letta memory
          │ explicit, policy-gated escalation
          ▼
Spark / Vesper on the Gemini API
```

The Basic tier is a specification and acceptance boundary. It does not claim
that a phone, VPS, or Gemini project is currently provisioned.

## Why

The repository's phone-mesh work describes the intended topology, but the
design is spread across open PRs and research notes. A concise OpenSpec gives
the next implementation a stable contract while keeping paid provisioning,
phone actions, and cloud escalation behind explicit gates.

The source basis is:

- [PR #5: offline tailnet bridge stubs](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/5)
  for the `:8081/health` phone bridge, SFTP shape, and tailnet-bound host
  template.
- [PR #6: off-cloud phone mesh architecture](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/6)
  for the phone → Vultr → Spark three-tier model and escalation policy.
- [PR #7: Pixel Gemma bridge runbook](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/7)
  for device admission, thermal, and model-size guardrails.
- [PR #8: Vultr inference bootstrap profiles](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/8)
  for tailnet-only Ollama, optional Letta, and the separate sidecar boundary.
- [PR #9: phone MCP research](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/9)
  for narrow capability and authentication guidance. Basic intentionally
  selects health-only.
- [PR #10: Drive sweep](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/10)
  for evidence status and the rule that large Drive artifacts remain
  pointers, not unpacked repository inputs.

## Proposed change

Add four docs-only OpenSpec artifacts:

1. `spec.md` — normative requirements and acceptance criteria.
2. `design.md` — topology, interfaces, routing, security, and operations.
3. `tasks.md` — implementation and verification checklist.
4. This proposal — scope, rationale, and decision record.

## In scope

- A Tailscale-only path between an approved phone, a headless Vultr host, and
  an operator/control-plane client.
- A Vultr inference service exposing a private OpenAI-compatible interface.
- Optional Letta memory backed by local Postgres/pgvector and local inference.
- A phone MCP boundary that exposes only `GET /health` in Basic.
- Explicit Spark/Vesper escalation through an approved Gemini API project.
- Secret, cost, audit, and rollback requirements.

## Out of scope

- Ansible or any configuration-management playbook.
- Unpacking, reading, or reconstructing `CONV2_B`.
- CMV accounts, CMV Gmail, or CMV as an inference or escalation path.
- Phone side effects such as SMS, camera, contacts, location, UI automation,
  notifications, flashlight, or arbitrary Android intents.
- Cursor or Cursor Cloud as a runtime inference dependency.
- Automatic Vultr provisioning, resizing, destruction, or model downloads.
- Committing keys, model weights, APKs/AABs, binaries, prompts, or private
  message contents.

## Decision requested

Approve this Basic contract as the implementation gate. A later tier may
extend inference or phone capabilities only by changing the requirements and
acceptance criteria; it must not silently broaden Basic.


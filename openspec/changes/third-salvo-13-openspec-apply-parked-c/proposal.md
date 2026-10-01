# Apply: Envelope & Cross-Skill Consistency

- **Change-id:** `third-salvo-13-openspec-apply-parked-c`
- **Parked target:** `C` — Envelope & Cross-Skill Consistency
- **Status:** applied
- **Mode:** documentation-only

## Intent

Promote the parked envelope idea into a small, reviewable OpenSpec contract:
every response-producing path uses the same envelope, while the active skill
load remains intentionally thin.

## Scope

This apply defines the required envelope and the structured debug signal that
can be harvested by an orchestrator. It does not edit skill implementations,
make network calls, or add a runtime/event-log dependency.

## Out of scope

- loading every skill into every response path;
- introducing a full OpenTelemetry stack;
- changing deployment or credential configuration;
- modifying any existing skill `SKILL.md`.

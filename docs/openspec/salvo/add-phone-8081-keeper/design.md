# Design: add-phone-8081-keeper

## Context

T4-04 requires a continuous reload note for the included lane. CinC names the
phone target as port `8081`, path `/keeper`. The target is recorded as an
address/path contract only; this change does not define a transport or bind a
listener.

## Goals

- Keep the T4-04 reload lane continuous and included-only.
- Record the CinC target as `phone:8081/keeper`.
- Make the no-live-bind and offline boundaries directly verifiable.
- Produce a small, reviewable OpenSpec package with one receipt.

## Non-Goals

- Do not create, edit, or overwrite any Willow `SKILL.md` or live lock file.
- Do not unpack or process `CONV2_B`.
- Do not use external services, providers, credentials, tokens, or secrets.
- Do not provision infrastructure or use a live network path.
- Do not select a transport, open a socket, bind `:8081`, probe `/keeper`, or
  run a phone service.
- Do not route any reload to On-Demand usage.

## Decisions

1. **Target notation:** use `phone:8081/keeper` as the CinC target. `phone`
   identifies the target class, `8081` identifies the port, and `/keeper`
   identifies the path; the notation does not imply a transport.
2. **Reload policy:** reload is continuous by contract and MUST remain in the
   included lane. On-Demand is forbidden.
3. **Execution boundary:** this package is an offline documentation artifact.
   Applying or reviewing it performs no bind, probe, request, or external
   integration.
4. **Receipt:** the package-local receipt records the scope and fence checks
   without claiming that a live endpoint exists.

## Risks

| Risk | Mitigation |
|------|------------|
| A note is mistaken for a live endpoint | State that no transport or bind is defined |
| Reload drifts into On-Demand | Make included-only and the prohibition explicit |
| Documentation work touches runtime territory | Keep all artifacts under `docs/openspec/` |

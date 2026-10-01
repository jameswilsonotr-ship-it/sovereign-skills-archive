# Receipt — THIRD_SALVO T3-15

- **Reserved change ID:** `third-salvo-15-change-id-collision-guard`
- **PR title:** `salvo: T3-15 change-id-collision-guard`
- **Scope:** one atomic OpenSpec change with an offline collision fixture
- **Release lane:** Included Ultra only
- **On-Demand:** explicitly rejected

## Delivered

- `proposal.md` — intent, scope, and acceptance criteria
- `design.md` — canonicalization, guard order, result vocabulary, and
  non-goals
- `tasks.md` — implementation checklist and deferred validator integration
- `specs/change-id-collision-guard/spec.md` — normative requirements and
  scenarios
- `fixtures/reserved-change-id-collision.yaml` — exact, case-only, unique,
  and On-Demand cases with expected outcomes

## Fences

This receipt records no edits to Willow `SKILL.md`, no `CONV2_B`, no
external/provider calls, no secrets, no Vultr live activity, and no Linear
mint. The deliverable is documentation and fixture data only.

## Verification

- `git diff --check`
- Fixture reviewed against the scenarios in `specs/change-id-collision-guard/spec.md`

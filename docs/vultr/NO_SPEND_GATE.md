# Vultr no-spend gate

**Status:** documentation-only policy

## Atomic included burn

Any action that can create or increase a Vultr charge is gated as one atomic
decision. **Bunny YES is required before the action.**

This includes, at minimum:

- creating, starting, resizing, or renewing a Vultr resource;
- selecting paid add-ons, backups, snapshots, storage, IPs, or other services;
- making a provider/API/CLI call that could create or change billable
  infrastructure; and
- allowing an approved deployment to continue past a free or non-billable
  preparation step.

Documentation, estimation, quote review, and local dry-run preparation do not
authorize spend. A previous approval, an existing budget, silence, or a merged
pull request is not Bunny YES.

## Provider boundary

**Vultr ≠ Cold Steel.**

Vultr is an infrastructure provider. Cold Steel is a separate project,
system, or capability. Vultr account access, a Vultr plan, a server, or a
successful deployment does not establish Cold Steel approval, readiness,
ownership, equivalence, or authorization.

## Required sequence

1. Define the exact Vultr resource, duration, region, add-ons, and expected
   landed cost.
2. Record the rollback or destroy path and the applicable spend cap.
3. Obtain an explicit **Bunny YES** for that specific spend.
4. Perform only the approved action. Stop and re-gate if the scope or cost
   changes.

If Bunny YES is absent or ambiguous, do not provision, renew, upgrade, or
otherwise incur Vultr spend.

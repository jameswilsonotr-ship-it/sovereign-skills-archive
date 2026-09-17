# Burn Wave Fence Checklist

**Status:** hard gate  
**Purpose:** keep an atomic burn-wave change inside its approved boundaries.

Complete this checklist before merging, deploying, or spending money. Any
unchecked item is a stop condition.

## Required fences

- [ ] **No Willow `SKILL.md`.** Do not add, copy, generate, install, or
  reference a Willow `SKILL.md` as part of this work.
- [ ] **No `CONV2_B`.** Do not create, enable, copy, or assume a `CONV2_B`
  surface, variant, flag, or configuration.
- [ ] **Vultr is not Cold Steel.** Treat Vultr as an infrastructure/provider
  name and Cold Steel as a separate project or system designation. Do not use
  the names interchangeably or imply that one authorizes the other.
- [ ] **Bunny says YES before Vultr spend.** Get an explicit, current
  approval from Bunny before provisioning, upgrading, or otherwise incurring
  any Vultr charge. A plan, silence, prior discussion, or inferred consent is
  not approval.

## Stop conditions

Stop and return for review if:

1. a Willow `SKILL.md` appears in the diff or dependency set;
2. `CONV2_B` appears in the implementation or runtime configuration;
3. a Vultr resource is described as Cold Steel, or Cold Steel is treated as
   proof that Vultr work is approved; or
4. Vultr spending is proposed without the explicit Bunny YES recorded first.

## Evidence

Record the verification location or artifact for each checked item before
merging. Keep this checklist with the change so the four fences remain
auditable.

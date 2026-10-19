# Change: salvo: T4-03 inkbox-keeper

## Status

Proposed as a documentation-only, offline change.

## Why

T4-03 needs one unambiguous keeper contract for the CinC target. The
contract must make continuous included reload the default and only behavior
while recording that Inkbox is intentionally a no-op in this change.

## What changes

- Define the T4-03 keeper contract in OpenSpec.
- Require reload to be continuously included; on-demand reload is forbidden.
- Affirm that the Inkbox target is an atomic no-op with no runtime integration.
- Record the offline and repository-scope fences in the change itself.
- Add a receipt documenting the files and offline validation.

## Scope

This change adds OpenSpec and receipt documentation only. It does not add or
modify executable code, provider configuration, credentials, deployment
configuration, or external-service behavior.

## Non-goals and fences

- No `Willow SKILL.md` is added, edited, or used as an implementation source.
- No `CONV2_B` material is added or changed.
- No external, provider, secret, or Vultr integration is performed.
- OD (On-Demand) behavior is forbidden.
- No network, provider, secret, or deployment operation is required.

# Change proposal: dependency inventory delta

- **Change ID:** `third-salvo-28-dep-inventory-delta`
- **Salvo slot:** `T3-28`
- **Inclusion tier:** `Ultra`
- **Delivery mode:** included only; never On-Demand

## Why

The latest local skill-orchestrator export reports 27 scanned skills, while the
older library inventory still reports 32 entries. The mismatch needs a small,
auditable delta rather than an install or a refresh of the underlying library.

## Scope

This change adds a documentation-only dependency inventory delta for the T3-28
slot. It records the inventory baseline, the zero-install dependency result,
and the inclusion boundary for Ultra.

## Non-goals

- No package, tool, runtime, or provider installation.
- No changes to the skill tree or existing inventory source files.
- No On-Demand dependency or fallback path.
- No external, provider, secret, infrastructure, or coordination integration.

## Acceptance criteria

1. The change is represented under this OpenSpec change directory.
2. The delta identifies its baseline and separates observed inventory facts from
   the T3-28 delta.
3. Ultra is the only included tier and On-Demand is explicitly excluded.
4. The recorded dependency set is empty because this is a documentation-only
   change and no installation was performed.
5. A receipt records the offline validation and fence checks.

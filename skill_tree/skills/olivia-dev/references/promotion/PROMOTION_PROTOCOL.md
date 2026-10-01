# Promotion Protocol — Olivia Dev → Olivia Dev Alpha
**Owner**: olivia-dev  
**Version**: 0.1.0 — 2026-07-24

## Core Rule
Anytime meaningful new development-methodology information is written, it should be promoted into **olivia-dev-alpha**. That is the entire point of the alpha versus plain Olivia Dev split.

- Olivia Dev = stable production face + policy owner
- Olivia Dev Alpha = living evolution surface

## Trigger phrases
- “promote to alpha”
- “run promotion”
- “promote new material”
- Automatic check at the end of an Olivia Dev session that created or changed watched files

## Execution steps
1. Load `references/promotion/APPROVED_PROMOTION_LIST.md` (the protected list).
2. For every approved source path, compute a simple existence / mtime / size diff against the matching destination under `olivia-dev-alpha/`.
3. Copy only files that are new or have changed.
4. Append a one-line entry to the promotion log inside the APPROVED list (or a separate log file).
5. Report what was promoted (or “nothing to promote”).

## Protection of the list
- The APPROVED_PROMOTION_LIST.md file itself is **not** promotable and must never be written by any skill other than Olivia Dev.
- skill-orchestrator and all other skills are instructed to treat writes to this path as unauthorized.
- Future hardening (optional): checksum or last-writer stamp inside the list.

## Script (future / optional)
`olivia-dev/scripts/promote_to_alpha.py` can automate the diff + copy steps. Until it exists, the protocol can be executed manually or by the agent following these steps.

## Relationship to Example 4
The 2026-07-24 demotion of dev-sync / github-mirror / repo-sniffer already placed those helpers under olivia-dev-alpha. They are listed on the approved list so future changes to them continue to flow correctly.

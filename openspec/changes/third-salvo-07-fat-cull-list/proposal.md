# Change proposal: T3-07 fat-cull candidate list

- **Change-id:** `third-salvo-07-fat-cull-list`
- **Slot:** THIRD_SALVO / T3-07
- **Mode:** INCLUDED Ultra only
- **Status:** proposed

## Summary

Create a bounded, evidence-backed candidate list for removing oversized,
generated, duplicated, or vendored artifacts from the included Ultra payload.
This change is documentation-only: it records candidates and disposition
rules; it does not delete, move, rewrite, or re-tier any payload.

The source boundary for the inventory is the local
`origin/skill-tree-intake` snapshot at commit `640a2ca`
(`feat: unpack 2026-09-16 full skill tree for Cursor (MIS-5)`). No external
or provider data is used.

## Problem

The intake snapshot contains large binary/vendor payloads and generated
derivatives alongside the skill surface. Without a candidate register, a
future Ultra packaging pass can either carry unnecessary weight or make
unreviewed changes to runtime content.

## Proposed outcome

Produce a reviewable register that:

1. names each candidate by exact path or bounded path pattern;
2. records measured bytes and the evidence boundary where available;
3. explains why the item is a fat-cull candidate;
4. preserves a review gate for anything that may be runtime-relevant; and
5. keeps the work strictly inside the INCLUDED Ultra lane.

## Non-goals and hard fences

- No `SKILL.md` edits, including any Willow-related `SKILL.md`.
- No `CONV2_B` work; its identifier appears only as an exclusion fence in
  these docs.
- No external/provider calls, secrets, Vultr live activity, or Linear minting.
- No deletion, move, archive operation, regeneration, dependency change, or
  packaging implementation.
- No assignment of any candidate to On-Demand. T3-07 is an INCLUDED Ultra
  record only; candidates remain unassigned pending a separate approved
  change.

## Acceptance criteria

- The reserved change-id appears in every change document.
- The candidate list is based only on the named local snapshot and records
  its measurement method.
- Candidate entries are paths/patterns, not destructive instructions.
- The diff contains documentation files only.
- The final delivery is one atomic PR titled exactly
  `salvo: T3-07 fat-cull-list`.

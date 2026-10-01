# Change: T4-07 fat-cull reject-list delta

- **Change ID:** `fourth-salvo-07-fat-cull-delta`
- **Salvo slot:** `T4-07`
- **Reload:** `CONTINUOUS`
- **Lane:** `INCLUDED`
- **On-Demand:** `NEVER`
- **Mode:** offline-only documentation

## Summary

Record the T4-07 delta to the fat-cull register as a reject list. The reject
list identifies content that must remain out of cull scope until a separate,
approved review establishes a safe replacement and retention boundary.

T4-07 is itself continuously included. Every reload must carry the same
reject-list policy; reload must not turn this record into a lazy or
On-Demand lookup.

## Delta

The following classes are explicitly rejected from fat-cull consideration:

1. Willow `SKILL.md` files and skill-tree live locks.
2. `CONV2_B` material.
3. Runtime or build inputs whose ownership, replacement, or regeneration path
   is not proven by local evidence.
4. External/provider, secret, credential, and Vultr-related material.

This is a reject-list delta, not an implementation plan. It does not delete,
move, archive, regenerate, package, or re-tier any file.

## Acceptance criteria

1. The change identifies `T4-07` and `fourth-salvo-07-fat-cull-delta`.
2. Reload mode is `CONTINUOUS` and the lane is `INCLUDED`.
3. On-Demand is explicitly forbidden and never emitted.
4. The reject classes above are present in the specification and receipt.
5. The change contains documentation only and is reviewable offline.
6. The delivery contains one atomic change and one receipt.

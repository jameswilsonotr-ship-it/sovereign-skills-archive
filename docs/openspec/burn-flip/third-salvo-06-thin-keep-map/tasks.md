# Tasks: third-salvo-06-thin-keep-map

## 1. Atomic scope

- [x] 1.1 Reserve exactly `third-salvo-06-thin-keep-map` for T3-06
- [x] 1.2 Keep the packet independently reviewable and documentation-only
- [x] 1.3 Exclude sibling salvo slots and sibling change-ids

## 2. Thin-KEEP map

- [x] 2.1 Record the retained T3-06 documentation surface
- [x] 2.2 Record post-coherence stop behavior for contradictions
- [x] 2.3 Record protected surfaces as KEEP / do-not-touch boundaries

## 3. Included-only fence

- [x] 3.1 State INCLUDED Ultra as the only permitted lane
- [x] 3.2 Reject On-Demand as a fallback or alternate lane
- [x] 3.3 Confirm no external/provider call is needed to read the deliverable

## 4. Verification

- [x] 4.1 Exercise the ADDED scenarios in
  `specs/thin-keep-map/spec.md`
- [x] 4.2 Confirm no Willow `SKILL.md` or skill-tree live lock edit
- [x] 4.3 Confirm no `CONV2_B`, provider, secret, Vultr-live, or Linear-mint
  activity

Verification is documentation-only. The change contains no credentials,
tokens, connection strings, provider calls, or generated/binary artifacts.

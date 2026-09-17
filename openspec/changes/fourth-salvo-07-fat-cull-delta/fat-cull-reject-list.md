# T4-07 fat-cull reject list

**Change ID:** `fourth-salvo-07-fat-cull-delta`  
**Reload:** `CONTINUOUS`  
**Lane:** `INCLUDED`  
**On-Demand:** `NEVER`  
**Disposition:** reject from cull consideration

## Delta register

| ID | Reject class | Reason |
|---|---|---|
| R-01 | Willow `SKILL.md` and skill-tree live locks | Protected ownership boundary; not a T4-07 payload decision. |
| R-02 | `CONV2_B` | Explicitly outside this offline documentation slice. |
| R-03 | Unproven runtime or build inputs | Culling requires local proof of replacement, regeneration, and retained source. |
| R-04 | External/provider, secret, credential, or Vultr material | Outside the offline-only boundary and requires a separate approved scope. |

## Reload invariant

The reject set is included on every T4-07 reload. A replacement snapshot must
retain all four rows and their `reject` disposition. A missing row is a
closed-fail condition, not permission to infer, fetch, delete, or reclassify
content.

## Explicit non-actions

This list does not name deletion targets. It does not authorize deletion,
movement, archiving, regeneration, packaging, dependency changes, or
re-tiering. No candidate is assigned to On-Demand.

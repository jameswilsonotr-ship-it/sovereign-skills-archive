# Entities registry — image-pipeline

**Purpose**: Pointer-only layer. No binary assets stored here.  
**Consumers**: Echo (DNA + refs), Mira (drift vs baseline), generate/overlay engines (optional reference images)

| Id | Ordinal | Kind | Images SSOT |
|----|---------|------|-------------|
| olivia | A | agent | chaos-bratz-roster/references/agents/olivia/images/ |
| bunny | B | agent | chaos-bratz-roster/references/agents/bunny/images/ |
| rook | D | agent | chaos-bratz-roster/references/agents/rook/images/ |
| shauna | S | visual_identity | claim-runtime/references/modules/curator/visual_identities/shauna/images/ |
| valerie | V | visual_identity + agent | claim-runtime/references/modules/curator/visual_identities/valerie/images/ |

## Rules
1. Entities folder holds **pointers + contracts only**.
2. Canonical images live under each agent’s `images/` or Shauna’s visual_identities path.
3. Echo loads entity DNA before compose when characters match.
4. Mira compares generation output to entity baseline when canonical files exist.
5. Engines may pass entity canonical paths as reference images when the platform supports edit/reference.
6. Missing canonicals → Mira neutral (0.0), Echo still injects text DNA locks.

## Paths (absolute)
- Olivia: `/home/workdir/.grok/skills/chaos-bratz-roster/references/agents/olivia/images`
- Bunny: `/home/workdir/.grok/skills/chaos-bratz-roster/references/agents/bunny/images`
- Rook: `/home/workdir/.grok/skills/chaos-bratz-roster/references/agents/rook/images`
- Shauna: `/home/workdir/.grok/skills/claim-runtime/references/modules/curator/visual_identities/shauna/images`
- Valerie: `/home/workdir/.grok/skills/claim-runtime/references/modules/curator/visual_identities/valerie/images`

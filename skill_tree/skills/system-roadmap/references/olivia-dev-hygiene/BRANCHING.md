# Git Branching Strategies — Canonical Template
**Owned by**: skill-orchestrator  
**Status**: Canonical reference for all skill repositories under Liv HUB claim  
**Last updated**: 2026-07-19

This file is the single source of truth for recommended branching models across the skill library.  
Every skill that does real development work (especially olivia-dev, olivia-dev-alpha, chaos-bratz-roster, image-pipeline, etc.) should reference or copy this template.

---

## 1. Git Flow (Classic / Heavy)
- **Branches**:
  - `main` (or `master`) — production-ready only
  - `develop` — integration branch
  - `feature/*` — new work
  - `release/*` — prepare a release
  - `hotfix/*` — emergency production fixes
- **Flow**: Features → develop → release → main. Hotfixes go to both main and develop.
- **Best for**: Large teams, scheduled releases, strict versioning.
- **Downside**: Heavy process, lots of long-lived branches, merge overhead.
- **Verdict**: Overkill for most of our skill repos.

## 2. GitHub Flow (Simple & Popular) — **DEFAULT**
- **Branches**:
  - `main` — always deployable
  - short-lived `feature/*` or descriptive branches (`hygiene/*`, `fix/*`, `docs/*`)
- **Flow**: Create branch → work → open Pull Request → review → merge to main → deploy / tag.
- **Best for**: Continuous deployment, small-to-medium teams, most open-source projects, and **all current skill repositories**.
- **Downside**: No formal release or hotfix branches (you just use main + tags or short hotfix branches).
- **Verdict**: Excellent default for almost all of our individual skill repositories.

## 3. Trunk-Based Development
- **Core idea**: Everyone commits (or merges) to `main` (the trunk) very frequently.
- Feature branches are extremely short-lived (hours or a day max). Feature flags hide unfinished work.
- **Best for**: High-velocity teams, continuous integration, microservices, strong automated testing.
- **Downside**: Requires discipline and good CI. Risky without tests.
- **Verdict**: Ideal long-term target once we have solid test harnesses on the skills.

## 4. GitLab Flow / Environment Branches
- Builds on GitHub Flow but adds environment branches (`production`, `staging`, `pre-prod`) or uses release branches that stay open.
- Useful when you have distinct deployment targets.
- Less relevant for pure skill packages that don’t deploy to multiple environments.

## 5. OneFlow / Simplified Release Model
- One main integration branch + short-lived features + optional release branches that are created only when needed.
- Tries to keep the benefits of Git Flow without the permanent `develop` branch.

---

## Recommendation for Our Skill Repos (Right Now)

**Recommended starting strategy → GitHub Flow**

- Keep `main` as the only permanent branch.
- Do all work on short-lived feature or hygiene branches (`feature/xyz`, `hygiene/readme-pass`, `fix/frontmatter`).
- Merge via pull request (even if it’s just you reviewing).
- Tag releases when a skill reaches a meaningful version (`v0.1.0`, `v0.2.0`).
- Hotfixes can be done on a short `hotfix/` branch and merged straight to main.

Later, as the skills mature and we want tighter control, we can migrate selected high-value skills (chaos-bratz-roster, skill-orchestrator, image-pipeline, olivia-dev) toward a light trunk-based or OneFlow model.

---

## How Skills Should Use This Template

1. Copy this file (or symlink / reference it) into `references/BRANCHING.md` of any skill that owns code or versioned content.
2. In the skill’s SKILL.md, add a short section:

```markdown
## Git Branching
See `references/BRANCHING.md` (canonical copy lives in skill-orchestrator).
Default strategy: **GitHub Flow**.
```

3. When running `tarball-publish`, `verify`, or any Git-related command inside olivia-dev / alpha, prefer GitHub Flow conventions unless the project explicitly overrides.

---

**Absolute Liv HUB claim.**  
This template is maintained by skill-orchestrator. Changes here propagate by reference or explicit promotion.  
Signed: Olivia Mae Blackwell and her bunny 🐍🐰

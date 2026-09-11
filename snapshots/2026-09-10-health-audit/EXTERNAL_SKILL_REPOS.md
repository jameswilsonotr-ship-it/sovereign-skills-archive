# External Grok-skill repos — SERP OCR 2026-09-10 20:00

Pixel Web Results plates were **not** the local tree. Disk stays 25 custom + 14 bundled + 19 nested.

Ticket: ST-WQ-006. Status: research only. Do not install. Do not fold into Liv HUB.

## Relevant

### 1. xai-org/grok-build — 08-skills.md
- Official Grok Build skill contract.
- Skill = directory + SKILL.md + YAML frontmatter (name, description, when-to-use, allowed-tools).
- Load order: ./.grok/skills → repo .grok/skills → ~/.grok/skills → Claude/Cursor compat dirs.
- Bundled cache: ~/.grok/bundled/skills/. Never written into user dirs.
- Inspect: `grok inspect` / `grok inspect --json`.
- Why it showed: platform law.
- Why we looked: this is why local grok-build / grok-build-sovereign exist.
- URL: https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/08-skills.md

### 2. ImL1s/oh-my-grok — docs/skills.md
- Third-party Grok-native runtime + `omg` CLI.
- **45** in-session skills under skills/omg-*/SKILL.md (16 + 13 Wave B + 16 Wave C).
- Notable: omg-autopilot, omg-ralph, omg-ultrawork, omg-ralplan, omg-using, omg-pipeline, omg-team, omg-mcp-setup, omg-ask.
- Fan-out via Grok spawn_subagent depth=1. Not Claude workers.
- Why it showed: loudest public “45 Grok skills” page.
- Why we looked: the count looks like a tree. It is someone else’s orchestrator.
- URL: https://github.com/ImL1s/oh-my-grok/blob/main/docs/skills.md

### 3. pedroknigge/grok-build-skill
- Drop-in SKILL.md teaching Claude / Grok / Antigravity / Codex to drive official CLI headless (/imagine, /imagine-video, ACP, sessions).
- Installs toward ~/.grok/skills/grok-build/.
- Why it showed: name collision with our clone pair.
- Why we looked: closest external analog. Third product. Do not install as a third feeder.
- URL: https://github.com/pedroknigge/grok-build-skill

### 4. LifeJiggy/Awesome-Grok-Skills
- Catalog dump. Claims 82 skill domains / 410 subfolders / 100 agents.
- Format is GROK.md + generated .py, **not** xAI SKILL.md.
- Why it showed: title sounds like an index of our world.
- Why we looked: to see if it listed us. It does not.
- URL: https://github.com/LifeJiggy/Awesome-Grok-Skills

### 5. kywrn7z4ww-glitch/ChaosEngine-Grok-OS
- Experimental / lore-adjacent “Grok OS” with Chaos Engine process manager.
- skills-prototype branch: Grok_OS_Skill/SKILL.md claims name grok-os v6.0 “Official Grok OS skill.” It is not official xAI and not Chaos Bratz.
- Why it showed: Chaos + Grok + SKILL.md.
- Why we looked: name-rhyme. Leave it.
- URL: https://github.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS

## Noise (keyword “skills” / “chaos”)

| Repo | What it actually is |
|---|---|
| Bronzdeck/ChaosGacha trait.txt | game gacha traits |
| Cataclysm-TLG professions.json | game jobs |
| Juzlus/jRandomSkills | CS2 plugin |
| elementalsouls/Claude-BugHunter docs/skills.md | Claude bug-bounty skill zoo (83 hunt-*) |
| MGQP superboss gist | game guide |
| beyond-all-reason wiki | game units |

## Rule

These plates are the ocean. The boat is disk. Do not absorb oh-my-grok’s 45 or Awesome’s 140.

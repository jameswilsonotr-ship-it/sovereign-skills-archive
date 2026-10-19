# smoke_bratz boot

## One command

```bash
python3 /home/workdir/.grok/skills/smokeshow/scripts/smoke_bratz_boot.py
```

## What it does

1. Confirms smokeshow + chaos-bratz-roster are on disk
2. Lists `smokeshow/candidates/`
3. Confirms Skill Router + Organism Interface prompts exist
4. Prints startup lines and suggested next commands

## In-chat equivalent

User (or sticky prompt) can say:

> boot smoke bratz  
> smoke_bratz boot  
> smokeshow chaos bratz startup

Session should run the script (or treat its report as boot truth) and then operate with:

- **Skill Router** for live ↔ candidate routing
- **Organism Interface** for Vesper / Olive / bus handoffs
- **chaos-bratz-roster** as identity/ops SSOT

## Old agents (retired)

Drive folder `1Rs7aJXhasPt-TnR-hIDRTkA7pj1eg91u` held:

- Olivia prompt (sticky — still useful as session chrome)
- Skill navigator (passive path list → replaced by Skill Router)
- Raw json nav (broken JSON dump → replaced by Organism Interface)

Absolute Liv HUB claim.

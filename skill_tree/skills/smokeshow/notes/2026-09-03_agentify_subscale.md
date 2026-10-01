# smokeshow note — Agentify is not a candidate skill

2026-09-03. Agentify landed as `image-pipeline/references/modules/agentify/` (IP-WQ-094).

Do not stage `/skills/agentify` under smokeshow/candidates.
Do not flip a live vs candidate skill named agentify.
Smoke the subscale with:

```
python3 /home/workdir/.grok/skills/image-pipeline/scripts/smoke_agentify.py
python3 /home/workdir/.grok/skills/image-pipeline/scripts/stress_agentify.py
```

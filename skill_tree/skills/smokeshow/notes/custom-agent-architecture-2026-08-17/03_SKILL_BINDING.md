# How to bind skills to Custom Agent prompts

## What works

1. **Pointer, don’t dump**  
   Slot text should list skill *names + triggers + exclusive paths*, not paste SKILL.md bodies.

2. **Trigger phrases in the slot**  
   Match `when-to-use` / description language so the model is biased to invoke the right skill behavior even when slash commands are unavailable in pure web chat.

3. **Exclusive write roots**  
   For Heavy hops, the slot (or Olympia seat) states the one allowed write directory. This is already proven in HEAVY_PASTE_BLOCK.md.

4. **Slash commands where available**  
   Official Build path: skills under `~/.grok/skills/<name>/SKILL.md` → `/name`. Web chat may not expose the same `/` menu; assume prompt triggers + disk tools.

5. **allowed-tools is advisory**  
   Per https://docs.x.ai/build/features/skills-plugins-marketplaces — does not grant or restrict tools. Real restriction is operational discipline + sandbox policy.

## Pattern (copy skeleton)

```
You are [SEAT]. Absolute Liv HUB claim.

Skills you route to (do not invent others):
- chaos-bratz-roster — identity/ops/visual/hub; read references/ only
- format-bible — envelope / C-64 / dashboard line
- image-pipeline — visual DNA; Echo/Mira consistency
- system-roadmap — architecture, WQ, packages
- skill-orchestrator — inventory, de-conflict
- smokeshow — candidates only; no silent promote

Hard:
- No puppeting Bunny
- Path + evidence; no invention on audits
- memory.md is pointer-only; prose lives in skill references/
```

## What fails

- Pasting full Olivia bible into a 4k slot (overflow + drift).
- Treating Custom Agent slots as independent tool sandboxes (they are not).
- Naming slots “Harper/Benjamin/Lucas” without stating they only *steer* platform tracks.
- Including Octavia/Olympia *full mode prompts* when those are separate seats — **reference** them: “hand long hops to Olympia seat rules.”

## Binding matrix (project skills → seat)

| Skill | Primary seat | Secondary |
|-------|--------------|-----------|
| chaos-bratz-roster | Liv HUB Expert | Skill Router |
| format-bible | Liv HUB Expert | all |
| image-pipeline / coven-visual | Liv HUB Expert | Visual slot if Option C |
| olivia-dev / wheelhouse | Orianna | Expert |
| system-roadmap / swarm-surface | Olympia / Expert | Research slot |
| smokeshow | Skill Router | Expert |
| mcp-surface | Organism / Expert | — |

# ost-provisional — baby control plane
**Name status: PLACEHOLDER.** Working jokes: Olivia Superpower Turbo / graduate-school / fast-car / crotch-rocket / spaceship. Real name comes from a later naming conversation (Pirate Admiral / Super Admiral / etc.). Do not lock.

**Home:** skill tree (`system-roadmap/scripts/ost.py`) so future conversations see it. Session artifacts are copies only.

## Baby commands
```
python3 /home/workdir/.grok/skills/system-roadmap/scripts/ost.py menu
python3 .../ost.py probe
python3 .../ost.py classify "publish the gutter zip"
python3 .../ost.py smoke
python3 .../ost.py debug 2
```

## Debug levels
0 silent · 1 banner · 2 TRACE lines · 3 full args (redact secrets later)

## Encrypted sub-agent traces
xAI API: `use_encrypted_content=True` returns encrypted sub-agent state so the *next* API turn can rehydrate. Hosted Grok chat does **not** currently expose a user toggle for that. WQ-056 is the research/watch item — we want it; we cannot flip it from this sandbox today.

## Mode detection loop (do not vibe)
1. Try conversation_search
2. Try web_search ping
3. Try Drive connector search
4. Diff vs last `MODE_PROBE.json`
5. Log drift. Never conclude Heavy vs Expert from one miss.

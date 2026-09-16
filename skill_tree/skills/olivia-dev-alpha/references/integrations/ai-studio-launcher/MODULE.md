# AI Studio launcher — Olivia Dev Alpha module
Stamp: 2026-09-11
Claim: Liv HUB. Alpha. Pair with colab-launcher. Not a replacement.

## What this is
Phone-first tap list for Google AI Studio (Gemini / Build / GitHub-connected). Grok prepares a prompt block. Bunny taps the URL, pastes, hits Run.

Triggers: ai studio, aistudio, ai studio pro, gemini studio, studio launch, paste prompt studio.

## Click URLs

| Intent | URL |
|---|---|
| Studio home | https://aistudio.google.com/ |
| New chat | https://aistudio.google.com/prompts/new_chat |
| Apps / Build | https://aistudio.google.com/apps |
| Library | https://aistudio.google.com/library |
| GitHub import (Build) | https://aistudio.google.com/apps — Connect GitHub from the project gear |

GitHub is why Studio is the second launcher. Colab owns Drive steel. Studio owns repo + prompt + generate.

## Agent procedure
1. Write the prompt she will paste into `artifacts/studio-prompt-<slug>.md`. Keep it under one screen.
2. Give her TWO taps: New chat URL + the fenced prompt.
3. If the job is a repo, also give the GitHub repo URL and say "Connect GitHub in Apps, then paste."
4. Do not pretend this pane can push the Run button. Same rule as Colab.

## Prompt envelope (copy this shape)

```
PROJECT: <slug>
DRIVE FOLDER: <id or path>
GOAL: <one sentence>
CONSTRAINTS: adult lock / no explode 416 MB into 08 / index first
INPUTS: <file ids>
OUTPUT: <what lands back on Drive>
```

## Limits
Studio is not a zip exploder. Use it for code + prompt jobs. Use Colab for Drive mount + member lists of packs 4–20. Use steel (K15 / G9) for the 416.6 MB tar.

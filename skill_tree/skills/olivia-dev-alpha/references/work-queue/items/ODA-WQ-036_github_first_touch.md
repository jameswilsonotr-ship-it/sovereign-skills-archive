# ODA-WQ-036 — GitHub first touch: grab the page and the README

**Date:** 2026-09-07 21:41 EDT
**Status:** OPEN / STANDING
**Owner:** olivia-dev-alpha
**Trigger:** any turn that starts “fucking with” a GitHub repository

## Law
First two files, before plugins, before probes, before vibes:

1. The **GitHub landing page** — about, topics, license, latest release, wiki/releases/actions, what a human sees in the right rail. Save as `*-GITHUB-FRONT.md`.
2. The **README** (raw if it exists) — the actual manual. Save as `*-README.md`.

Humans first. Then the dump.

Do this for every new repo, not just yt-dlp. Park both files in the active surface’s work-queue `refs/` (or Alpha `references/github-first-touch/<org>/<repo>/` when we grow that folder). Write a short WQ pointer that maps README sections onto *our* tickets.

## Why
2026-09-07 we downloaded the yt-dlp README and indexed flags, then Bunny said the joke was the *whole page*. The abort ate the front-page capture. That is the hole this ticket closes.

## First example (done tonight)

| file | where |
|---|---|
| landing page | `artifacts/inbound-queue/refs/yt-dlp-GITHUB-FRONT.md` |
| README raw | `artifacts/inbound-queue/refs/yt-dlp-README.md` |
| our map + test block | `artifacts/inbound-queue/IP-WQ-163_ytdlp_readme_manual.md` |

## Recipe

```
# landing (human)
browse https://github.com/ORG/REPO  → write REPO-GITHUB-FRONT.md

# manual
curl -fsSL -o REPO-README.md https://raw.githubusercontent.com/ORG/REPO/HEAD/README.md
# if README is .rst/.txt, take that instead. If none, say so in the FRONT file.
```

Do not claim “I read the manual” if only one of the two files exists.

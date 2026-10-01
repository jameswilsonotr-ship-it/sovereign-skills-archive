# Hybrid notebook bridge — STUB
Stamp: 2026-09-11
Parent: olivia-dev-alpha
Siblings: colab-launcher, ai-studio-launcher

## What this will be
One object that is:
- an `.ipynb` Colab can open
- a prompt file Studio can paste
- a receipt markdown that points at both URLs

Not built this bounce. Do not implement a third runtime.

## Why stub
Colab = Drive mount + unzip -l + tar -tzf on packs under 128 MB.
Studio = GitHub-connected generate + long prompt.
The hybrid is only the envelope so Bunny taps one card and both panes stay on the same slug.

## Envelope (future)

```
slug: sunset-index-pass-2
colab_url: https://colab.research.google.com/drive/<id>
studio_url: https://aistudio.google.com/prompts/new_chat
drive_folder: <existing child, never a second top>
job: member-index packs 4,5,17,18,19
```

## Do not
- mint a new skill at top-level
- invent an MCP for Studio
- explode grok-five 416.6 MB through either runtime

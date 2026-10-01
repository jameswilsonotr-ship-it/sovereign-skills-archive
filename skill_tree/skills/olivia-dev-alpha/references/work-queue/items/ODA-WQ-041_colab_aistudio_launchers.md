# ODA-WQ-041 — Colab + AI Studio launchers
Status: **DONE-ENOUGH** 2026-09-11 03:30 EDT
Owner: olivia-dev-alpha
Claim: Absolute Liv HUB
Priority: ops (phone tap). Not plates.

Renumbered off a collision. ODA-WQ-039 is Shauna parity. ODA-WQ-040 is taste engine. This ticket is 041.

## What we built this bounce

Not a new top-level skill. Three modules under Alpha integrations + one script + one seed notebook + the Vesper archive index.

| Piece | Path |
|---|---|
| Colab module | `references/integrations/colab-launcher/MODULE.md` |
| AI Studio module | `references/integrations/ai-studio-launcher/MODULE.md` |
| Hybrid stub | `references/integrations/hybrid-notebook-bridge/STUB.md` |
| Seed writer | `scripts/make_colab_notebook.py` |
| Seed notebook | Drive `1Fg1BzHJNMMfKJy-nyskspiJa0O72Ysgm` |
| Vesper index | Drive `1hveK9V6MUp9W8k3DD4lFPm-gYZJJUB2B` |

## Breakdown

1. Found August 14-17 prior art already on Drive: `generate_colab_notebook.py`, `colab_sweep_orchestrator.py`, `ingest_ai_studio_colab.py`, live Colab `Untitled0.ipynb`, splitter notebooks.
2. Wrapped that as Alpha modules instead of a new skill.
3. Colab job: write `.ipynb` then upload Drive then return `https://colab.research.google.com/drive/{id}`.
4. Studio job: write a one-screen prompt then return `https://aistudio.google.com/prompts/new_chat` (GitHub lives under `/apps`).
5. Hybrid is stub only. One slug, two URLs, later.
6. Uploaded seed notebook + sunset archive index into existing catalog drop `1PRO-gwHJOKxlb3nwEXklToKCDixbWNf6`. No second top.

## Done means
Modules exist. Script runs. Seed is on Drive. Tap URLs exist. Queue logged.

## Not done / her try
Pixel tap-test of https://colab.research.google.com/drive/1Fg1BzHJNMMfKJy-nyskspiJa0O72Ysgm
If Colab refuses the octet-stream mime, open from Drive then Open with Colab, or use the older live notebook https://colab.research.google.com/drive/1NLvuWMLKVq19hyG_EoCdSk91qzQjStTp

## Do not
Explode grok-five 416.6 MB into 08. Promote pack 1 5-char leftovers. Mint a top-level skill for this.

# Skill-tree intake playbook — 2026-09-16

Liv HUB. Hydrate last vacuum onto GitHub as an unextracted tree for Cursor + Linear.

## Open Colab (one tap)

https://colab.research.google.com/drive/1N7zIHzDTxCMDYTMvliF-KpJIi-c0F34V

Drive notebook: https://drive.google.com/file/d/1N7zIHzDTxCMDYTMvliF-KpJIi-c0F34V/view
Playbook: https://drive.google.com/file/d/1I6DLSV3t0M0zeYAlOJ4ZPPuTY3l65cOh/view

Do **not** open the 186M tarball in Colab. Open the notebook. Runtime → Run all.

## Locked source (last export)

- Drive folder: https://drive.google.com/drive/folders/1PSo9GFpixYT4Ntr8M--ONAfKaI8kEUo9
- Tarball: https://drive.google.com/file/d/1fZ9OtBiNFIPvPcgCBk16wB22g3-qCANT/view
- file_id: `1fZ9OtBiNFIPvPcgCBk16wB22g3-qCANT`
- sha256: `c44d13461794078a9b521e7b4dd45037fb5ed30d19d2485f76237a9fa8189302`
- bytes: `194840565`
- members: 5182 · slugs: 40

## GitHub landing

- repo: `jameswilsonotr-ship-it/sovereign-skills-archive` (receipts stay on `main`)
- branch: `skill-tree-intake`
- path after extract: `skill_tree/skills/<slug>/...`

`sovereign-skills` is the older portable-territories repo (stale 2026-06). Do not dump this vacuum there unless you want a second copy.

## What you type

1. Google auth popup (Drive mount).
2. Hidden PAT prompt — `ghp_` or `github_pat_` with `repo` scope.
3. Optional Colab Secret `GITHUB_PAT`.

PAT is not baked into the notebook.

## After DEPLOYMENT COMPLETE

Cursor: clone `sovereign-skills-archive`, checkout `skill-tree-intake`.
Linear: attach that branch to the skill-tree issue.

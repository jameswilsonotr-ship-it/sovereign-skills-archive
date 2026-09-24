# IP-WQ-167 — lake hygiene (keeps are a blob)

**Status:** OPEN  
**Owner:** image-pipeline  
**Created:** 2026-09-10 19:52 CDT  
**Claim:** Absolute Liv HUB

## Problem
`references/visuals/keeps/` is a dated flat dump. ~161 triples. No KEEP_INDEX.md until tonight. No per-candidate folder. No MANIFEST. `visuals/index.md` does not mention keeps. CHANGELOG points at `scripts/keep_path.py`, `KEEP_INDEX.md`, `KEEP_INDEX.jsonl`, and `references/work-queue/protocols/IPQ-078_keep_path.md`. None of those files exist on this tree. `scripts/` dir is missing. Work queue table only lists 161–166 stubs.

Cute. Not a lake.

## Work
1. Keep `KEEP_INDEX.md` + `KEEP_INDEX.jsonl` live after every keep.
2. Cut new keeps into `YYYY/MM/DD/<slug>/{frames,plates}/` with `MANIFEST.md`.
3. Restore `scripts/keep_path.py` and `scripts/step6_drive_flush.py` (or a thin hand-compat shim) so the triple is not authored by a one-off Python block.
4. Restore `protocols/IPQ-078_keep_path.md` as the written contract.
5. Backfill 2026/08 only as an index, do not reshuffle bytes until a dry-run pass is signed.
6. Point `visuals/index.md` at keeps/.

## Exit
New agentify session writes the A–D quartet into a candidate folder + one MANIFEST row + three jsonl lines per plate + Drive ids. Operator can find a person without globbing.

Implement pairing: IP-WQ-170 (emit ladder + script restore + gate). Do not ship 167 without 170’s `--gate` sentence.

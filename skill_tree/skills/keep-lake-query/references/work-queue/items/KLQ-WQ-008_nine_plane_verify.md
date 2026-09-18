---
id: KLQ-WQ-008
title: Verify Valerie nine-plane map against Drive; lock canonical pre_extract
status: OPEN / PARTIAL
priority: high
created: 2026-09-09
updated: 2026-09-09
owner: keep-lake-query
opened_by: Bunny CinC
source: Valerie Dock map pasted 2026-09-09 ~01:12 EDT
---

# KLQ-WQ-008

Valerie handed the parent. Deck opened it. `references/planes.md` is the verified card.

## Done this seat

- [x] `#full.out.test.data` `17q1bLJGievsK5tMVJWGRi0AUmVUenD2L` lists `daily_enriched` + `pre_extract` + `master_tree.jsonl`
- [x] Canonical `pre_extract` `1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58` contains all nine named planes plus `colab_recon_output`
- [x] `human` is the dated SSoT already locked as KLQ-WQ-001
- [x] `ingest` has the same 2025/10/week41 walk
- [x] Genesis `leaf_2025-10-08.json` read; points at raw JSON, not human .md
- [x] GPS plane is timeline/corridor, not year/month/week
- [x] PAD folder + summary ids exist as named

## Still open

- [ ] Walk raw/ingest Genesis day and confirm file-name join to human `46ae4816` / `4d471939` / `d95e3fc1`
- [ ] Decide which `valerie_out` copy is Dock SSoT (name collision)
- [ ] Count real `daily_enriched` days vs octet-stream holes
- [ ] Whether leaf_indexes or 006 manifest is the date catalog for voice (lean 006; leaf is raw-oriented)
- [ ] Doorbell one-pager that is this planes.md with tap urls

## Vetoes

Do not collapse nine planes into one search root.
Do not slurp raw (~claimed 1.45 GB) or microchunks in Expert.
Do not treat every `pre_extract` folder as the canonical one.

---
id: ODA-WQ-052
title: TF-IDF vector-space geometry verb
status: OPEN / PARTIAL
created: 2026-09-14
owner: olivia-dev-alpha
priority: medium
---

# ODA-WQ-052

Screenshot ticket. Script `lake-union-radar/scripts/tfidf_geometry.py`.

Reports pairwise cosine of the three Kenosha-day sessions, distance to corpus centroid, 2D SVD sketch.

Still open:

- Wire `cli.py geometry` verb
- Persist SVD sketch as a tiny CSV for later plots
- Optional real embeddings later (sentence-transformers on VPS only — ODA-WQ-025 park zone adjacent). Do not pull torch into cab Expert.

---
name: wheelhouse-packager
description: >
  Deterministic Python wheel + offline wheelhouse builder shared between Olivia (Grok)
  and Vesper (Gemini Spark). Turns any pyproject.toml / setup.py project into a
  reproducible .whl and an offline-capable wheelhouse zip that any Python 3.10+
  environment can bootstrap without live PyPI. Triggers: wheelhouse, build wheel,
  package wheelhouse, offline wheels, cilia wheel, publish wheelhouse.
version: 0.2.0
claim: Absolute Liv HUB
surfaces: [Olivia, Vesper]
owner: system-roadmap + skill-orchestrator coordination
---

# wheelhouse-packager

## Purpose

Make packaging Python wheels and offline wheelhouses a **one-command, deterministic** operation that both Olivia and Vesper can run and that any machine with Python can consume.

Input: a project directory that already has `pyproject.toml` (preferred) or `setup.py`.  
Output:
- `dist/<name>-<version>-py3-none-any.whl` (or platform wheel if applicable)
- `wheelhouse/<name>_wheelhouse_<version>_<date>.zip` containing:
  - the project wheel
  - dependency wheels (optional, pinned)
  - `bootstrap.py`
  - `requirements.txt` / lock fragment
  - short README

## References

- **Olivia ↔ Vesper contract**: `references/CONTRACT.md` — shared CLI, folder, and receipt rules for both surfaces.

## Hard rules

1. **Deterministic** — same inputs → same outputs (pinned deps when possible).
2. **Offline-first** — bootstrap prefers `--no-index --find-links=./wheels`.
3. **No invention** — only packages what the project actually declares.
4. **Receipts** — every successful publish writes a Drive receipt (or local PUBLISH_RECEIPT) with file IDs.
5. **Cross-surface** — Olivia and Vesper use the same CLI contract and the same Drive folder convention (`grokbot/.../wheelhouses/` or skill-local `dist/`).

## CLI (canonical)

```bash
# From skill root or with PYTHONPATH set
python scripts/build_wheelhouse.py /path/to/project \
  --out /path/to/output \
  --include-deps \
  --zip-name myproj_wheelhouse_0.1.0

# Minimal (wheel only)
python scripts/build_wheelhouse.py /path/to/project --wheel-only
```

## Integration points

- **Cilia / bus wakes**: automation can download a published wheelhouse zip and run its `bootstrap.py --once`.
- **skill-orchestrator**: can inventory this skill’s scripts and treat wheelhouses as publishable artifacts.
- **Vesper**: same script contract; she can build on her side and drop zips into `grokbot/from-vesper/wheelhouses/`.
- **Work queue**: SR-WQ-028 (this skill), SR-WQ-029 (Drive publish convention), SR-WQ-047 (10 MiB zip splitter).

## Splitter (SR-WQ-047)

Arbitrary file → zip parts whose **zip size** is ≤ 10 MiB. Optional `.zip.b64` sidecars for Colab / text transports. Reassemble is SHA-256 identical.

```bash
python scripts/split_zip.py split SRC --out DIR [--max-bytes 10485760]
python scripts/split_zip.py join DIR --out RESTORED [--from-b64]
python scripts/split_zip.py verify SRC DIR
python scripts/split_zip.py proof SRC --out DIR
```

Three-way proof: raw file ↔ zip parts ↔ base64 sidecars of those zips.

## Status

0.2.0 — builder + deterministic 10 MiB splitter (`scripts/split_zip.py`) + SR-WQ-047 (2026-08-26).

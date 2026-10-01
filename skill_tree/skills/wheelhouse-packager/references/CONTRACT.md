# Olivia ↔ Vesper wheelhouse contract

## Shared CLI

Both surfaces run the same entry point:

```bash
python scripts/build_wheelhouse.py <project_dir> --out <out_dir> [--include-deps] [--wheel-only] [--zip-name NAME]
```

## Shared outputs

| Artifact | Meaning |
|----------|---------|
| `*.whl` | Installable project wheel |
| `*_wheelhouse_*.zip` | Offline bundle: wheels/ + bootstrap.py + requirements.txt + README |
| `PUBLISH_RECEIPT_*.md` | Local receipt of what was built |

## Shared Drive convention (recommended)

- Olivia publishes under `grokbot/from-olivia/cilia_bus_wheelhouse/` (or a general `wheelhouses/` sibling)
- Vesper publishes under `grokbot/from-vesper/wheelhouses/`
- Receipts can also land in `grokbot/receipts/`

## Bootstrap contract for consumers

Any Python 3.10+ environment:

```bash
unzip <wheelhouse>.zip
cd <staging or root of zip>
python3 bootstrap.py --once
```

Offline install is preferred when `wheels/` is present.

## Splitter (shared, SR-WQ-047)

```bash
python scripts/split_zip.py split SRC --out DIR [--max-bytes 10485760]
python scripts/split_zip.py join DIR --out RESTORED [--from-b64]
python scripts/split_zip.py proof SRC --out DIR
```

- Each `.partNNNN.zip` is ≤ max-bytes (default 10 MiB).
- `SPLIT_MANIFEST.json` carries source SHA-256 and per-part hashes.
- `.zip.b64` sidecars are optional Colab / text-only transport (they are larger than the zip; the *zip* is the size-capped artifact).
- Join from zip or from b64 must equal source SHA-256.

## Versioning

Skill version and project version are independent. Skill currently 0.2.0.

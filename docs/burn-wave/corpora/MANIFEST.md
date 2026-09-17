# BURN HARD corpus manifest

The machine-readable manifest is [`MANIFEST.json`](MANIFEST.json). It lists the
optional local blobs used by the offline harness:

| Corpus | Blob | Output | Missing-blob behavior |
| --- | --- | --- | --- |
| phone health | `blobs/phone_health.json` | `phone_health.json` | Generate the deterministic health fixture |
| connector call log | `blobs/connector_call_log.jsonl` | `connector_call_log.jsonl` | Generate the deterministic four-call JSONL corpus |

Blobs are deliberately not checked in. A local export can be dropped at the
manifest paths and is used only after its declared SHA-256 matches. If a blob
is absent, the harness records `source: "synthetic"` in its receipt and uses
the bounded synthetic data in `MANIFEST.json`; it never fetches a remote URL.

To ingest the corpus into a scratch harness directory:

```bash
PYTHONPATH=harness/src python -m sovereign_harness.corpus \
  --manifest docs/burn-wave/corpora/MANIFEST.json \
  --output harness/.generated/burn-wave
```

## Provenance annotation

**2026-09-17 audit:** This manifest entered the repository in commit
`a17e0db` (`2026-09-17T04:32:43Z`). It has no capture date and is not labeled
current or stale; treat its snapshot status as **UNDATED — UNKNOWN**. See
[`../PROVENANCE_AUDIT.md`](../PROVENANCE_AUDIT.md). The current JSON entries
do not declare `sha256`; checksum validation is available when a future entry
provides one, but this manifest does not establish a checksum for a local blob.

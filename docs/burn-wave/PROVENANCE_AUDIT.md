# Burn-wave provenance audit

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-04-provenance-audit` |
| Slot | `S2-04` |
| Audit date | `2026-09-17` (UTC) |
| Scope | Included Ultra only |
| Base revision | `cf7afbe782b7cc790aa3683c8d4268aa4ed29ba4` (`skill-tree-intake`) |
| Source revision for the audited docs | `a17e0db53b925b86c0c4e1b172629a2400af1632` |

## Scope and method

This audit covers the two pre-existing files under
[`docs/burn-wave/`](.): [`corpora/MANIFEST.md`](corpora/MANIFEST.md) and
[`corpora/MANIFEST.json`](corpora/MANIFEST.json). It uses repository contents,
local Git history, and the offline loader/tests; it does not use connector,
network, Box, or other service calls.

No OD material is included. `Willow SKILL.md`, `CONV2_B`, and unrelated S2
slots are out of scope. `Vultr` and `Cold Steel` are distinct labels; this
audit makes no equivalence claim between them.

## Date audit

| Artifact | Date evidence | Finding |
| --- | --- | --- |
| `corpora/MANIFEST.md` | Introduced in `a17e0db` at `2026-09-17T04:32:43Z` | The Git commit date is known, but the document has no capture date, `as_of` date, or last-updated field. |
| `corpora/MANIFEST.json` | Introduced in the same commit and timestamp | Same gap; `schema_version: "1"` is a schema version, not a date. |
| Synthetic phone-health payload | `version: "0.1.0"` | Payload version only; it is not evidence of when the fixture was captured. |

The commit timestamp is provenance for when these files entered this
repository. It must not be interpreted as the capture date of either a local
blob or the synthetic fixture.

## Source-claim audit

| Claim in the historical Markdown manifest | Evidence | Result |
| --- | --- | --- |
| The JSON file is the machine-readable manifest. | `MANIFEST.json` exists and is consumed by `harness/src/sovereign_harness/corpus.py`. | **Supported.** |
| Blobs are optional and local. | The loader resolves each entry below the manifest directory and falls back when the path is absent. | **Supported.** |
| A blob is used only after its declared SHA-256 matches. | The loader checks `sha256` only when an entry contains one; neither current entry declares `sha256`. | **Conditionally supported, easy to overread.** The current manifest provides no checksum assurance for a present blob. |
| Missing blobs produce `source: "synthetic"`. | `_artifact_bytes()` selects the deterministic manifest fallback when a local path is absent; tests assert synthetic receipts. | **Supported.** |
| The loader never fetches a remote URL. | The corpus loader has only a manifest-relative file path and synthetic fallback; the offline tests exercise the no-network contract. | **Supported for corpus ingestion.** |

No source owner, source location, capture event, blob digest, or review
receipt is recorded in the current JSON entries. Therefore the synthetic
fixtures are reproducible from the manifest, but any future local blob is not
independently attributable from these docs.

## Stale-snapshot label audit

Neither audited file declares `snapshot_date`, `captured_at`, `as_of`,
`current`, `stale`, or `superseded`. The manifest is therefore:

> **UNDATED — stale/current status unknown. Do not treat it as a current
> snapshot.**

This is a provenance-status label, not a claim that the files are stale. The
historical Markdown manifest carries a minimal annotation pointing here; the
machine-readable JSON was left unchanged.

## Required follow-up for a dated source claim

Before treating a future burn-wave corpus as current or source-backed, record
the capture date, source label (`included-ultra`), source revision or event
identifier, and a SHA-256 for every local blob in the machine-readable
manifest. Keep synthetic receipts explicitly marked `source: "synthetic"`.

## Fence receipt

- Included lane: Ultra only.
- Excluded: OD, Willow `SKILL.md`, `CONV2_B`, and all other S2 slots.
- Naming fence: `Vultr` is not `Cold Steel`.
- Secrets: none added or copied.

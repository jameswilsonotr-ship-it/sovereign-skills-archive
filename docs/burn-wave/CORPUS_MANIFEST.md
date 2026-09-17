# S2-14 corpus manifest

**OpenSpec change-id:** `second-salvo-14-corpus-manifest`  
**Slot:** `S2-14`  
**Profile:** **Ultra only**  
**Boundary:** one offline BURN HARD corpus set; this file is not a registry for
other S2 slots.

## Inclusion

This manifest records the existing local BURN HARD corpus declaration and its
deterministic fallback output. The included set contains:

| Artifact | Role | Provenance mode | SHA-256 |
| --- | --- | --- | --- |
| `docs/burn-wave/corpora/MANIFEST.json` | Machine-readable corpus declaration | Tracked local file | `47115b2aa27d573abac58d2b52093a2fc2b9d0929e6abe6b45d6bd0e824a4bff` |
| `docs/burn-wave/corpora/MANIFEST.md` | Human-readable corpus declaration | Tracked local file | `4de03d43dbedf387cdb65ec983929069664f2d0edbf257638e06c32b14b4a549` |
| `phone_health.json` | Deterministic phone-health fixture | Synthetic, generated locally | `5e27c1848e8c73a92fdda35f50ec596a80bcc6ab9c6bbfc484fb41c2899df008` |
| `connector_call_log.jsonl` | Deterministic connector-call fixture | Synthetic, generated locally | `568bf12fe6208e7433a45ff200cb08a09daca2a972b60579d57328b456a9c6fb` |

The last two hashes are for the canonical bytes produced when the optional
blobs are absent. They are output hashes, not claims about an undisclosed
source blob. The checked-in corpus manifest intentionally declares no remote
source and no blob payload.

## Provenance

- The declarations and loader are present in local Git history at
  `a17e0db53b925b86c0c4e1b172629a2400af1632`
  (`feat: ingest offline BURN HARD corpora (#27)`).
- The S2-14 review base is the local `skill-tree-intake` line at
  `cf7afbe782b7cc790aa3683c8d4268aa4ed29ba4`.
- The fixture hashes above were obtained by running the repository's local
  `sovereign_harness.corpus` loader against
  `docs/burn-wave/corpora/MANIFEST.json` with its blobs absent.
- A missing blob resolves only to the manifest's deterministic synthetic
  value. A present local blob is accepted only after its declared SHA-256
  matches.

## Local-only boundaries

This corpus set may read tracked files and optional blob files below the local
manifest directory only. It may write generated artifacts to a caller-selected
scratch directory. It must not:

- make external calls, including network, MCP, API, connector, provider
  console, or live account calls;
- add secrets, credentials, tokens, personal data, or unredacted payloads;
- treat synthetic connector records as evidence of real connector activity;
- fetch or resolve a remote URL when a local blob is absent;
- read, copy, or include `OD` material;
- read or include `Willow SKILL.md`;
- read or include `CONV2_B`;
- treat `Vultr` as `Cold Steel`; those names are distinct and neither is a
  source for this corpus set;
- modify, summarize, or claim coverage for any S2 slot other than `S2-14`.

The absence of a blob is therefore a valid, reproducible local state. Any
future payload addition requires a new, explicitly scoped change rather than
enlarging this manifest implicitly.

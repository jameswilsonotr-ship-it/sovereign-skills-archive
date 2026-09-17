# Burn-wave shelf index

| Field | Value |
| --- | --- |
| OpenSpec change | `second-salvo-06-shelf-index` |
| Slot | `S2-06` |
| Inclusion profile | **Ultra only** |
| Operating mode | Offline; repository-local paths only |
| Historical material | Reference-only; not rewritten by this change |

This is the index for the included Ultra burn-wave shelf. It is deliberately
small: it points at the checked-in offline corpus and harness surfaces without
copying historical documents or claiming contents that are not present in the
repository.

## Included shelf

| Shelf item | Path | Role |
| --- | --- | --- |
| Corpus manifest | [`corpora/MANIFEST.json`](corpora/MANIFEST.json) | Machine-readable phone-health and connector-call-log inputs |
| Corpus notes | [`corpora/MANIFEST.md`](corpora/MANIFEST.md) | Offline ingestion instructions and missing-blob behavior |
| Harness package | [`../../harness/pyproject.toml`](../../harness/pyproject.toml) | Local test and tooling contract |
| Harness implementation | [`../../harness/src/sovereign_harness/`](../../harness/src/sovereign_harness/) | Deterministic corpus, connector, phone, MCP, and hygiene surfaces |
| Deterministic fixtures | [`../../harness/src/sovereign_harness/fixtures/`](../../harness/src/sovereign_harness/fixtures/) | Checked-in local fixture data; no provider fetches |
| Offline tests | [`../../harness/tests/`](../../harness/tests/) | Smoke, property, and bounded stress coverage |
| CI entry point | [`../../.github/workflows/harness.yml`](../../.github/workflows/harness.yml) | Offline harness checks |

## Hard fences

- **Ultra only:** this index does not include OD or OD-derived material.
- **No Willow live-skill content:** no Willow `SKILL.md` is added, indexed, or
  changed.
- **No `CONV2_B`:** it is outside this shelf.
- **Separate labels:** Vultr and Cold Steel are distinct; neither is an alias
  for the other.
- **No external calls:** the included shelf is repository-local and offline.
- **No secrets:** no credentials, tokens, private identifiers, or secret
  material belong in this index.
- **No other S2 slots:** this file covers `S2-06` only.

The existing corpus manifest and historical documents remain unchanged. Refresh
this file when the included Ultra shelf changes; do not use it to rewrite the
historical record.

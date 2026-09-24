# Second-salvo documentation link check

Receipt for OpenSpec change-id `second-salvo-36-link-check` and slot `S2-36`.

## Scope fence

- Included lane: **Ultra only**.
- OD is excluded.
- Shelf checked: the repository's `docs/**/*.md` documentation shelf on
  `skill-tree-intake`.
- The receipt itself was written after the scan and is not part of the input
  count.
- This slice did not inspect or modify imported skill content, other S2 slots,
  `Willow SKILL.md`, or `CONV2_B`.
- The Vultr runbook remains Vultr-only; it is not treated as Cold Steel.
- The check is local and offline. No external URLs were fetched, and no
  secrets were read or recorded.

## Method

For each Markdown file in the shelf, the check:

1. collected Markdown link occurrences;
2. resolved repository-relative paths from the source file;
3. verified that each resolved path exists; and
4. validated local heading fragments using the repository's lowercase,
   punctuation-stripping heading-slug rule.

External URLs and `mailto:` links would be reported separately and would not be
fetched. None were present in this shelf.

## Receipt

| Measure | Result |
| --- | ---: |
| Markdown files scanned | 9 |
| Link occurrences | 12 |
| Repository-relative link occurrences | 12 |
| External link occurrences | 0 |
| Repository-relative paths that exist | 12 |
| Fragment references | 6 |
| Broken local links | 3 |

All three failures are the same stale fragment target:

| Source | Target | Finding |
| --- | --- | --- |
| `docs/bridges/SPARK_BIND.md:90` | `#basic-tier-alignment` | The heading `BASIC_TIER alignment` slugs to `#basic_tier-alignment`. |
| `docs/bridges/stubs/GEMINI_SPARK_SEND.md:6` | `../SPARK_BIND.md#basic-tier-alignment` | The target heading uses `#basic_tier-alignment`. |
| `docs/bridges/stubs/VESPER_MCP_BIND.md:6` | `../SPARK_BIND.md#basic-tier-alignment` | The target heading uses `#basic_tier-alignment`. |

All other 9 local link occurrences resolve to existing paths and valid
fragments. The three stale fragments are recorded as follow-up findings; this
ATOMIC slice changes only this receipt.

## Reproduction

Run the local link checker from the repository root. The check must remain
offline and must not be changed to fetch remote URLs:

```text
docs/**/*.md -> resolve local targets and fragments -> report missing paths/fragments
```

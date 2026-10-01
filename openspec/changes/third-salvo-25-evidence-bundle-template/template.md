# T3 Evidence Bundle

Copy this file for the `T3-25` evidence bundle. Keep the identity block
unchanged. Replace bracketed values only where the field is marked editable.

## Identity (immutable)

```yaml
change_id: third-salvo-25-evidence-bundle-template
salvo: THIRD_SALVO
slot: T3-25
inclusion: INCLUDED
tier: Ultra
on_demand: false
network: disabled
status: draft
```

## Bundle metadata (editable)

- `bundle_id`: `[unique local identifier]`
- `created_at_utc`: `[YYYY-MM-DDThh:mm:ssZ]`
- `root`: `[repository-relative directory]`
- `purpose`: `[one-sentence description]`

## Evidence records

Add one record for every artifact used to support the bundle. Do not paste
artifact contents into this manifest.

### Evidence `[E-001]`

- `path`: `[repository-relative path]`
- `bytes`: `[integer]`
- `sha256`: `[64 lowercase hexadecimal characters]`
- `collected_at_utc`: `[YYYY-MM-DDThh:mm:ssZ]`
- `inspection_command`: `[exact local command]`
- `result`: `[what the command established]`
- `reviewer`: `[name or handle]`

<!-- Duplicate the evidence record section for E-002, E-003, and so on. -->

## Integrity checks

- [ ] Every path is repository-relative.
- [ ] Every record has a byte count and SHA-256 digest.
- [ ] Every timestamp is UTC and uses the stated format.
- [ ] Every inspection command runs with network access disabled.
- [ ] No record includes credential material or pasted artifact contents.

## Review gate

- [ ] `change_id`, `salvo`, and `slot` match the requested change.
- [ ] `inclusion` is exactly `INCLUDED`.
- [ ] `tier` is exactly `Ultra`.
- [ ] `on_demand` is exactly `false`.
- [ ] No On-Demand label or fallback appears in the bundle.
- [ ] All evidence records are complete and locally reproducible.

## Completion

Set `status` to `complete` only after every check above is selected.

- `reviewed_at_utc`: `[YYYY-MM-DDThh:mm:ssZ]`
- `review_notes`: `[short review result]`

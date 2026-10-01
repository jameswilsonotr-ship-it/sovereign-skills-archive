# Receipt — T4-22 mag SSOT snapshot

UTC: 2026-09-17

## Result

- Added the T4-22 magazine SSOT snapshot stub.
- Included reload behavior is fixed to `CONTINUOUS_INCLUDED`.
- On-demand reload is explicitly forbidden.
- The `spent`, `wet`, and `fired` fields are present and intentionally
  unobserved (`null`).

## Published paths

- `snapshots/2026-09-17/T4-22_MAG_SSOT_SNAPSHOT.md`
- `snapshots/2026-09-17/T4-22_RECEIPT.md`

## Verification

- Offline-only static review.
- No live state, credentials, or network-dependent value was added.
- The stub contains no deferred reload path.

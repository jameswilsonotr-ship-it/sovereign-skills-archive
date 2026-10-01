# Receipt — third-salvo-24-receipt-schema-v2

schema_version: 2
change_id: third-salvo-24-receipt-schema-v2
salvo: THIRD_SALVO
slot: T3-24
entitlement: INCLUDED
tier: ULTRA
on_demand: false

## Execution

- network: OFFLINE
- status: COMPLETE

## Artifacts

| path | kind | status |
|---|---|---|
| `openspec/changes/third-salvo-24-receipt-schema-v2/proposal.md` | proposal | COMPLETE |
| `openspec/changes/third-salvo-24-receipt-schema-v2/design.md` | design | COMPLETE |
| `openspec/changes/third-salvo-24-receipt-schema-v2/tasks.md` | tasks | COMPLETE |
| `openspec/changes/third-salvo-24-receipt-schema-v2/specs/receipt-schema/spec.md` | requirement-spec | COMPLETE |
| `openspec/changes/third-salvo-24-receipt-schema-v2/specs/receipt-schema/schema.json` | json-schema | COMPLETE |
| `openspec/changes/third-salvo-24-receipt-schema-v2/receipt.md` | receipt | COMPLETE |

## Verification

- v1 receipt files unchanged.
- All v2 fields are additive.
- `INCLUDED` / `ULTRA` is explicit.
- `on_demand: false` is explicit.
- No runtime or network operation was used.

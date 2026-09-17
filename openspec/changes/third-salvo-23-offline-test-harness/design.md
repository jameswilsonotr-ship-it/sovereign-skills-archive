# Design

## Boundary

`OfflineTestHarness` is intentionally a fixture resolver, not a client. It
has no transport dependency and exposes only:

- `register_fixture(endpoint, response, payload)`
- `request(endpoint, payload)`
- `run(HarnessCase)`
- `requests`

An unknown request raises `FixtureNotFound` from the low-level method and is
reported as a failed `HarnessResult` by `run`. This makes missing test data
visible without creating an implicit fallback.

## Slot policy

`SlotPolicy.validate()` is called during harness construction. It requires:

| Field | Required value |
| --- | --- |
| `slot_id` | `T3-23` |
| `availability` | `included` |
| `tier` | `ultra` |
| `on_demand_fallback` | `False` |

The policy is part of the executable stub so a future caller cannot widen the
slot accidentally while reusing the harness.

## Determinism

Fixture keys contain the endpoint and a canonical JSON encoding of the
payload. Key ordering therefore does not affect lookup. Requests are recorded
as immutable `RequestRecord` values, and results can be rendered with
`HarnessResult.as_dict()` for a local receipt.

## Verification

The tests use `unittest` and import the harness directly from this change
directory. No package installation or service startup is required:

```text
python -m unittest discover -s openspec/changes/third-salvo-23-offline-test-harness/tests -p 'test_*.py'
```

# Offline harness performance

## Contract

The stress suite is a bounded concurrency check, not a provider benchmark. It
must stay deterministic and must not require network access, credentials, or a
running MCP service.

| Surface | Workload | Concurrency | Assertion |
| --- | ---: | ---: | --- |
| Fixture connector ledger | 500 calls | 64 workers | Every response is recorded exactly once |
| Phone bridge health | 128 requests | 16 workers | Every local response is HTTP 200 |
| Property checks | 40 examples per generated request family | Hypothesis-managed | Request values round-trip unchanged |

Connector calls construct responses from checked-in JSON fixtures. The ledger
uses one in-memory DuckDB connection and a lock around inserts; connector
construction and fixture reads happen outside that critical section. This
keeps the test representative of concurrent call completion without creating
an external database dependency.

## Local measurement

Run the same bounded workload used by CI:

```console
cd harness
python -m pytest -m stress -vv --durations=10
```

For the full offline gate:

```console
python -m ruff check src tests
python -m mypy
python -m pytest -m "smoke or property"
```

Do not add wall-clock assertions to these tests. Shared CI runners, Python
versions, and dependency installation make absolute timings noisy. A timeout
or materially slower run should be investigated with pytest durations and
reported alongside the runner and Python version before changing the workload
or the CI budget documented in `CI_TIMEOUTS.md`.

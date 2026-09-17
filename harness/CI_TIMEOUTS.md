# CI timeout budget

The offline harness workflow gives both jobs a five-minute job timeout:

| Job | Workload | Timeout |
| --- | --- | --- |
| `offline` | Ruff, mypy, smoke tests, property tests, and the KEEP hygiene gate | 5 minutes |
| `stress` | 500 concurrent fixture-backed connector calls and 128 local phone-health requests | 5 minutes |

The timeout includes dependency installation. Test execution itself must remain
offline: connectors read checked-in fixtures, the phone test binds only to
`127.0.0.1`, and no provider credentials or live MCP services are used.

To investigate a timeout locally:

```console
cd harness
python -m pytest -m stress -vv --durations=10
```

If the stress job times out, first inspect dependency-install or runner
contention rather than raising the limit. The stress suite is bounded by
`CONCURRENT_CALLS = 500` and uses a 64-worker pool; a regression that needs a
larger timeout should include a measured explanation in `PERFORMANCE.md`.

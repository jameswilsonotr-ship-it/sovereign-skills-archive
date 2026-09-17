# Harness CI timeouts

The OpenSpec harness workflow is intentionally small and offline:

- The pytest job has a hard GitHub Actions limit of **10 minutes**.
- Pytest stops after the first failure with `--maxfail=1`.
- The workflow does not install packages or make dependency/network requests.
- `NO_NETWORK=1` and `OPENSPEC_OFFLINE=1` are set for tests that need an
  explicit offline-mode switch.

When adding a test that can hang, give it its own bounded wait or use a
fixture-level timeout supported by the test suite. Do not increase the job
timeout to mask a stalled test.

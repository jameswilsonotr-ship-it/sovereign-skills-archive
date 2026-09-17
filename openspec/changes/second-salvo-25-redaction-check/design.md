# Design

The check is implemented in
`sovereign_harness.redaction.check_fixture_directory`. It recursively reads
local `.json` files and applies a small fixed set of regular expressions for
email, phone, credential-assignment, private-key, and bearer-token patterns.

`RedactionFinding` stores only `source`, `rule`, and one-based `line`. The
scanner never stores or prints the matched substring, which keeps a failure
receipt from becoming a secondary leak.

The command-line entry point is:

```text
PYTHONPATH=harness/src python -m sovereign_harness.redaction
```

The test uses the repository fixtures for the passing path and in-memory
synthetic canaries for the detection path. No network or external corpus is
needed.

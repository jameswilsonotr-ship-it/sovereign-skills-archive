# Offline link-check script note

This is an implementation note for `third-salvo-27-link-check-offline`, not a
network probe. The eventual checker should use the language standard library
only and accept a workspace root plus optional Markdown paths.

## Required behavior

1. Discover Markdown files beneath the root when paths are not supplied.
2. Parse inline links, reference links, and images while retaining source
   line numbers.
3. Skip `#fragment`-only links after checking the current document.
4. Skip non-local schemes and targets without dereferencing them.
5. Resolve relative paths against the source document, then confirm the
   resolved path remains inside the workspace.
6. For Markdown/HTML targets, compare fragments with heading slugs and
   explicit `id` values.
7. Print sorted `path:line: target` failures and return:
   - `0` — no local failures
   - `1` — one or more missing paths or fragments
   - `2` — invalid arguments or an invalid root

## Minimal smoke harness

The implementation can be exercised without a package install or network
access:

```sh
python3 path/to/offline_link_check.py ./workspace
python3 path/to/offline_link_check.py ./workspace README.md docs/guide.md
```

For a focused smoke case, create a temporary local tree containing one valid
relative link, one missing relative link, and one missing fragment. The
expected result is a sorted report and exit status `1`. Replace the missing
targets and rerun; the expected result is no output for failures and exit
status `0`.

## Guardrails

- Do not add package installation, DNS lookup, HTTP requests, or service
  configuration to the checker.
- Do not read values from credential stores or environment variables.
- Do not follow symlinks that escape the requested workspace root.
- Keep the `INCLUDED` / `Ultra` gate at the caller boundary and reject
  `On-Demand` before scanning.

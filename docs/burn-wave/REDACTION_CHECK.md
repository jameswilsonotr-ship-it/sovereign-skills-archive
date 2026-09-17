# S2-25 redaction check

This is the **included Ultra-only** redaction gate for OpenSpec change
`second-salvo-25-redaction-check`. It checks the checked-in offline JSON
fixtures and does not contact a service, inspect a live skill, or modify a
fixture.

## What it checks

The single check scans
`harness/src/sovereign_harness/fixtures/**/*.json` for high-confidence:

- email addresses;
- North American phone numbers;
- credential assignments such as API keys, access tokens, client secrets, or
  passwords;
- private-key PEM headers; and
- bearer tokens.

Findings contain only the fixture path, line number, and rule name. Matched
values are deliberately not returned or printed.

Fixtures must use placeholders or reserved test values. No real secrets or
personal data belong in this repository. This slot covers only the local Ultra
fixture surface; adjacent slots and infrastructure/provider material are out
of scope.

## Exercise locally

From the repository root:

```bash
PYTHONPATH=harness/src python -m sovereign_harness.redaction
PYTHONPATH=harness/src pytest harness/tests/test_redaction.py
```

The command exits zero only when the local fixture set has no findings. To
exercise the failure path without changing a repository fixture:

```bash
tmpdir="$(mktemp -d)"
printf '{"email":"fixture.person@example.invalid"}\n' > "$tmpdir/canary.json"
PYTHONPATH=harness/src python -m sovereign_harness.redaction "$tmpdir"
rm -rf "$tmpdir"
```

The second command is expected to exit nonzero and report the `email` rule
without printing the canary address.

## Receipt

- Slot: `S2-25`
- OpenSpec change-id: `second-salvo-25-redaction-check`
- Included surface: local Ultra fixtures only
- Verification: `test_ultra_local_fixtures_pass_the_redaction_check`
- Failure-path verification: synthetic `.invalid` email, synthetic phone, and
  synthetic credential canaries in memory/temp space
- Network access: none
- Real secrets committed: none

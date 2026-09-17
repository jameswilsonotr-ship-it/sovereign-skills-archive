# SMS default-deny — S2-22

Offline receipt for OpenSpec change-id
`second-salvo-22-sms-default-deny`.

## Scope

This slice covers the **included Ultra** lane only. It does not authorize,
configure, or exercise a live SMS or phone path.

The offline contract is default-deny when consent is absent, explicitly false,
or not recognized. The existing `PhoneBridgeStub` enforces that boundary by
raising `NotImplementedError` for every SMS send attempt; it has no provider
transport.

## Cases

The cases are stored in
[`fixtures/sms_default_deny.json`](fixtures/sms_default_deny.json) and are
loaded by
[`harness/tests/test_sms_default_deny.py`](../../harness/tests/test_sms_default_deny.py).

| Case | Consent input | Expected result |
| --- | --- | --- |
| `consent-missing` | `null` | deny |
| `consent-false` | `false` | deny |
| `consent-unrecognized` | `"unknown"` | deny |

Every case uses a synthetic recipient label and an offline fixture body. No
phone number, secret, provider account, or message is used.

## Verification

Run from the repository root:

```bash
PYTHONPATH=harness/src pytest -q harness/tests/test_sms_default_deny.py
```

The test replaces socket creation with a failing guard and asserts that the
offline stub denies each case. A passing result therefore records zero live
SMS sends and zero phone calls.

## Hard fences

- Included Ultra only; no OD.
- No Willow `SKILL.md`.
- No `CONV2_B`.
- Vultr is unrelated to Cold Steel.
- No live SMS or phone activity.
- No secrets.
- No changes to other S2 slots.

## Receipt

- Slot: `S2-22`
- OpenSpec change-id: `second-salvo-22-sms-default-deny`
- Mode: offline fixture and harness test
- Live SMS/phone sends: `0`
- Fixture: `docs/burn-wave/fixtures/sms_default_deny.json`
- Test: `harness/tests/test_sms_default_deny.py`

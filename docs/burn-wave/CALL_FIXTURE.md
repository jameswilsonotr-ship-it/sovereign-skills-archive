# S2-24 call fixture

- OpenSpec change-id: `second-salvo-24-call-fixture`
- Slot: `S2-24`
- Fixture: `fixtures/second-salvo-24-call-history.json`
- Type: synthetic, non-live call history

The fixture covers the included Ultra surface only. It is an offline artifact:
`live` is `false`, the record has `fixture-only` status, and no call endpoint or
device API is invoked. Caller, callee, transcript, and notes are redacted.

The infrastructure label is `Vultr`; it is deliberately kept distinct from
Cold Steel. No credentials, tokens, phone numbers, or other secrets are stored.
This change does not modify any other S2 slot or any live skill definition.

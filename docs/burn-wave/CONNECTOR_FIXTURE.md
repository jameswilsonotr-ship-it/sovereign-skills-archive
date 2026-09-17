# S2-12 connector fixture

`docs/burn-wave/fixtures/s2-12-included-ultra.json` is a deterministic,
read-only fixture for OpenSpec change
`second-salvo-12-connector-fixture`.

- Scope is **included Ultra** only; OD is excluded.
- `source`, `network_access`, and `provider_access` make the offline boundary
  explicit. The fixture performs no provider calls.
- Vultr and Cold Steel are distinct and are not conflated or represented as
  provider data here.
- The fixture contains no credentials, tokens, or other secrets.

Validate the fixture locally with:

```bash
python -m json.tool docs/burn-wave/fixtures/s2-12-included-ultra.json
```

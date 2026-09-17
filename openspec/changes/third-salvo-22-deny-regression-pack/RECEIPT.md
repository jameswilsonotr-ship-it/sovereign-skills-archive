# Receipt: third-salvo-22-deny-regression-pack

- Change ID: `third-salvo-22-deny-regression-pack`
- Slot: `T3-22`
- Boundary: `INCLUDED` + `Ultra` only
- Test mode: offline, local fixtures, Python standard library
- Network or service calls: none
- Runtime implementation: not included; this pack defines the contract

## Verification

Command:

```text
python3 -m unittest discover -s tests -v
```

Result: **PASS** — 5 tests, 8 contract fixtures (`Ran 5 tests in 0.001s`).

The pack proves that the exact Included Ultra tuple is the only allowed case,
On-Demand Ultra is denied, malformed and non-matching inputs fail closed, and
denials have no fallback target.

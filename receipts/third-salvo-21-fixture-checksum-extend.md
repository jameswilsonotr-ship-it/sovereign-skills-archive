# Receipt: THIRD_SALVO T3-21 fixture-checksum-extend

- Change ID: `third-salvo-21-fixture-checksum-extend`
- Slot: `T3-21`
- Surface: included `Ultra` only
- On-Demand: forbidden
- Mode: offline
- Branch: `cursor/third-salvo-21-fixture-checksum-extend-cd4a`
- Pull request: https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/186

## Fixture

`fixtures/third-salvo/t3-21-ultra-included.json`

SHA-256:

`53d095806cec9931881f6b03767128d677f8d1dc148d9b829216ef2e8cc78979`

## Verification

```text
python3 scripts/verify_t3_21_fixture.py
verified fixtures/third-salvo/t3-21-ultra-included.json sha256=53d095806cec9931881f6b03767128d677f8d1dc148d9b829216ef2e8cc78979
```

Additional checks passed:

- Python bytecode compilation
- `git diff --check`
- scope scan for prohibited task surfaces

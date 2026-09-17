# T3-22 deny-regression pack

This pack is the executable offline companion to the OpenSpec change
`third-salvo-22-deny-regression-pack`.

Run from this directory:

```text
python -m unittest discover -s tests -v
```

The contract allows only the exact tuple:

```text
slot=T3-22, entitlement=INCLUDED, tier=Ultra
```

All other inputs are denied. In particular, On-Demand is never eligible, even
when its tier is `Ultra`.

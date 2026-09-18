# S2-37 — Tube 2 Spent Rule

## Mag rule

An item is **spent** when, and only when, both conditions are true:

1. The title contains the literal substring `salvo:`.
2. A live PR URL is present.

Formally:

```text
spent = title contains "salvo:" AND live PR URL exists
```

If either condition is false, the item is not spent.

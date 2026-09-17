# Salvo Count Board

## ATOMIC INCLUDED BURN

This board is the countable record for the atomic salvo shared by Cursor Liaison
and Torpedo Mag. The tally counts named agent identities only; it does not
estimate downstream work, delegated workers, or tools used by an agent.

### Current tally

| Agent identity | Included | Count |
| --- | :---: | ---: |
| Cursor Liaison | yes | 1 |
| Torpedo Mag | yes | 1 |
| **Total included agents** |  | **2** |

Machine-readable equivalent:

```yaml
salvo: atomic-included-burn
included_agents:
  - cursor-liaison
  - torpedo-mag
included_count: 2
```

### Counting contract

1. Add an agent only when its canonical identity is explicitly included in the
   salvo.
2. Count each canonical identity once. Aliases, retries, and handoffs do not
   increase the tally.
3. Do not infer an agent from a tool, model, subtask, or recipient.
4. Keep excluded, proposed, and unresolved identities out of
   `included_count`.
5. Update the named-agent table and the machine-readable block in the same
   change so the human and handoff views cannot drift.

### Handoff check

Before dispatch or closeout, Cursor Liaison and Torpedo Mag should report the
same `included_count` (`2`) and the same two canonical identities. A mismatch
is a count failure, not an invitation to guess; resolve the identity list
before treating the salvo as complete.

### Change record

| Date (UTC) | Change |
| --- | --- |
| 2026-09-17 | Created the atomic included-burn board with Cursor Liaison and Torpedo Mag. |

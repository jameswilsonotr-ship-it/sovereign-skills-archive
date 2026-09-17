# ATOMIC INCLUDED BURN: Stagger Policy

## Purpose

This policy defines when a burn wave may stagger execution. Included work is
treated as an atomic execution set: once work is included in the wave, soft
contention must not freeze or partially suspend that included set.

## Policy

1. **Do not stagger for soft contention.** Queue pressure, transient lock
   contention, ordinary backpressure, or a temporary resource shortage are
   soft conditions. Keep included work eligible and moving while the system
   applies its normal contention controls.
2. **Stagger only for a hard fault or merge melt.** A stagger requires an
   observed safety or correctness boundary:
   - **Hard fault:** an unrecoverable worker, process, data-integrity, or
     safety failure.
   - **Merge melt:** merge or reconciliation capacity is saturated, or
     concurrent arrivals are producing conflicts faster than they can be
     reconciled.
3. **Stagger atomically.** When a qualifying condition occurs, hold or
   serialize the affected wave at a clear boundary. Do not selectively freeze
   individual included items merely because they are experiencing contention.
4. **Resume deliberately.** Record the triggering condition, the boundary
   used, and the signal that cleared it before releasing the stagger.
5. **Do not infer a hard condition from uncertainty.** If the evidence is
   insufficient to distinguish a hard fault or merge melt, treat the condition
   as soft contention for admission purposes and escalate it for diagnosis.

## Decision table

| Condition | Included work | Stagger |
| --- | --- | --- |
| Soft contention | Remains included and eligible | **No** |
| Hard fault | Preserve atomic boundaries; isolate affected work as needed | **Yes** |
| Merge melt | Preserve atomic boundaries; reduce merge pressure | **Yes** |
| Unknown or unclassified | Remains included while classification is resolved | **No** |

## Operator check

Before applying a stagger, answer both questions:

- What concrete hard fault or merge-melt signal triggered it?
- What atomic boundary will be held or serialized?

If either answer is missing, the condition does not yet qualify for a
stagger.

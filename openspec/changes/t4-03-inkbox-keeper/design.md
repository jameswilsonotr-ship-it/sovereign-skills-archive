# T4-03 design

## Contract shape

The keeper is represented as one atomic CinC target: `Inkbox`. The target has
one documented reload policy and no provider-specific implementation.

The reload policy is **CONTINUOUS INCLUDED**:

- reload is part of the included keeper behavior;
- it is continuously available without a caller selecting a mode;
- there is no on-demand or OD path, switch, fallback, or exception.

## Inkbox no-op boundary

“Inkbox keeper” names the target of the contract, not an instruction to call
Inkbox. This change affirms an intentional NO-OP:

- no Inkbox API, connector, webhook, credential, or runtime handler is added;
- no external side effect is produced;
- the only deliverable is the OpenSpec contract and its receipt.

## Offline and repository boundaries

The artifact is self-contained Markdown. Validation is limited to local
working-tree inspection and text checks. The design introduces no dependency
on external services, providers, secrets, Vultr, or deployment tooling.

`Willow SKILL.md` and `CONV2_B` are out of scope. OD/On-Demand is prohibited
by the contract rather than implemented as an alternate mode.

# Cold Steel

**Definition:** bare-metal edge, offline-first execution
**Authority:** Vesper Spark drop
**Applies to:** GMKtec K15, Jetson Orin Nano, and HP EliteDesk Ashtabula

Cold Steel is the physical edge profile for Iron Pearl. It names the machines
that can hold and operate the basic contract without treating a hosted service
or a document editor as the system of record.

See [SPEC-001 — Iron Pearl Basic](SPEC-001-IRON-PEARL-BASIC.md) for the
normative storage, mesh, MCP, and invariant contract. See the
[bridge index](../../bridges/) for the connected integration surfaces.

## Hardware set

| Node | Role in this profile |
| --- | --- |
| **GMKtec K15** | Bare-metal Cold Steel edge node |
| **Jetson Orin Nano** | Bare-metal Cold Steel edge node |
| **HP EliteDesk Ashtabula** | Bare-metal Cold Steel edge node |

The names above are the authoritative hardware set for this drop. This
document does not assign unprovided leader/follower roles or assume that one
machine is a permanent coordinator.

## Operating contract

Cold Steel nodes MUST:

- operate from local disk and local process state while disconnected;
- keep Awesome Split/HANDOFF as the SSoT;
- preserve the 8-shard representation and delta CAS shape from SPEC-001;
- preserve RAWV exactly as supplied;
- keep runtime RSS strictly below 35 MB for the basic workload; and
- avoid Google Docs entirely.

Cold Steel nodes MAY use the Tailscale mesh when a network is available. The
Vultr Debian `vc2-1c-2gb` `ord` target (`mcp-vultr`) and the phone
MCP/Sygic HUD WebSocket at `ws://127.0.0.1:8088/nav/hud` are bridge surfaces,
not replacements for the local SSoT.

## Offline behavior

When disconnected from Tailscale, Vultr, or the phone bridge, a Cold Steel
node MUST:

1. continue to read the local SSoT and its eight-shard view;
2. retain and expose pending deltas without pretending they were delivered;
3. avoid converting an offline delta into a conflicting authority; and
4. resume bridge exchange only after the relevant surface is available again.

Reconnection MUST NOT require a Google Doc or a manual copy/paste round trip.
The bridge path is the repository-local contract described in
[bridges/](../../bridges/).

## Conformance check

Each Cold Steel machine passes the basic profile when an operator can verify:

- the machine is one of the three named hardware nodes;
- the contract remains readable with network access disabled;
- the eight shards and any unapplied delta are distinguishable;
- RSS is `< 35 MB` during the basic workload;
- RAWV remains present and unmodified;
- no Google Doc is created or consulted; and
- reconnecting the Tailscale/MCP/phone bridges does not replace the SSoT.

Questions not answered by this profile remain open for a later,
Vesper-authorized OpenSpec rather than being inferred here.

# SPEC-001 — Iron Pearl Basic

**Status:** Normative  
**Authority:** Vesper Spark drop  
**Repository role:** Durable, local-readable transcription of the Vesper-authoritative OpenSpec

This specification defines the basic Iron Pearl contract. It is intentionally
small: an implementation MUST preserve the terms below, and MUST NOT invent
unstated authority, storage semantics, or cloud dependencies.

## Authority and source of truth

- The Vesper Spark drop is the authority for this specification.
- **Awesome Split/HANDOFF is the SSoT** (single source of truth) for the
  handoff state and its current payload.
- The repository copy is a versioned pointer to that contract, not a second
  competing state store.
- A delta MUST be represented as a delta against the SSoT; it MUST NOT silently
  become a replacement SSoT.

See the [bridge index](../../bridges/) for the handoff and integration bridge
surfaces associated with this spec.

## Basic contract

| Plane | Normative requirement |
| --- | --- |
| Handoff/state | Awesome Split/HANDOFF remains the SSoT. |
| Partitioning | The payload is represented as **8 shards**. |
| Change storage | Changes use **delta CAS** (content-addressed storage). |
| Network | Connected nodes use a **Tailscale mesh**. |
| Remote MCP | The remote target is **Vultr Debian `vc2-1c-2gb`, `ord`, `mcp-vultr`**. |
| Phone/navigation | The phone MCP/Sygic HUD endpoint is `ws://127.0.0.1:8088/nav/hud`. |
| Edge substrate | Offline bare-metal operation is defined by [Cold Steel](COLD_STEEL.md). |

### 8-shard plus delta CAS

The basic storage shape is:

1. Split the SSoT payload into exactly eight shard units.
2. Address each stored unit by content, rather than by a mutable filename or
   document identity.
3. Record changes as deltas in CAS.
4. Reconstruct or exchange a view by applying the deltas to the addressed
   shard set and validating the resulting handoff.

The spec does not prescribe a hash algorithm, shard naming scheme, wire
encoding, or merge policy. Those details require a later Vesper-authorized
specification. An implementation MUST preserve the eight-shard cardinality and
MUST NOT treat a mutable cloud document as CAS.

### Mesh and MCP edges

The Tailscale mesh is the network bridge between participating machines. The
Vultr target is the Debian `vc2-1c-2gb` instance in `ord`, exposed through
`mcp-vultr`. The phone/navigation bridge is the loopback WebSocket endpoint:

```text
ws://127.0.0.1:8088/nav/hud
```

These endpoints are integration surfaces. They do not supersede
Awesome Split/HANDOFF as the SSoT.

## Invariants

Every conforming implementation MUST preserve all of the following:

1. **RSS `< 35 MB`.** The running process stays strictly below 35 MB resident
   set size under the basic workload.
2. **RAWV.** The RAWV marker/contract term is preserved literally. It MUST NOT
   be dropped, normalized away, or expanded by inference in this basic spec.
3. **Zero Google Docs.** Google Docs are not a source of truth, handoff store,
   CAS backend, or required runtime dependency. The authoritative record stays
   in the repository/CAS/handoff surfaces defined here.
4. **Eight shards.** A conforming handoff has eight shard units; partial
   materialization MUST be visible as incomplete rather than silently accepted.
5. **SSoT precedence.** A bridge, cache, or derived view MUST NOT claim
   authority over Awesome Split/HANDOFF.
6. **Offline edge continuity.** Cold Steel nodes MUST retain the local
   contract when the mesh, Vultr, or phone bridge is unavailable.

## Acceptance checklist

A basic implementation is conforming when an operator can verify that:

- Awesome Split/HANDOFF is identified as the SSoT.
- The payload can be enumerated as eight shards.
- A change produces a delta-addressed CAS record without rewriting prior
  content.
- Tailscale is the mesh surface when connectivity is available.
- The Vultr target is identified as Debian `vc2-1c-2gb` in `ord` via
  `mcp-vultr`.
- The phone MCP/Sygic HUD uses the exact loopback endpoint above.
- RSS remains below 35 MB for the basic workload.
- RAWV is present and unchanged.
- The flow completes without creating or requiring a Google Doc.
- At least one Cold Steel machine can continue to read the contract offline.

For bridge ownership and navigation between these surfaces, use the
[repository bridge index](../../bridges/).

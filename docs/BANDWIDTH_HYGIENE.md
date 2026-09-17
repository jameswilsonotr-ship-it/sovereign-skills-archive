# Bandwidth hygiene: what “Tailscale-only” does and does not imply

**Status:** operational inference and verification guide  
**Research date:** 2026-09-17  
**Constraint:** this document makes only Tailscale-specific networking
inferences. It does not claim a measured byte count, a provider bandwidth
quota, or a complete route map that the repository does not contain.

## Bottom line

The repository supports this statement:

> **Some administration and peer access are intentionally carried over
> Tailscale; a named exit node is used for a specific datacenter-IP problem.**

It does **not** support this stronger statement:

> **All system bandwidth is Tailscale-only.**

Why not? Tailscale is split tunnel by default. Ordinary internet traffic does
not enter Tailscale merely because the client is installed. A full-tunnel exit
node is a separate route choice, and the repository only records Gretchen as a
conditional exit-node workaround. The `tailscale nc` note also describes a
userspace ProxyCommand, which is evidence about that SSH/access path, not proof
of the host’s entire routing table.

## The safe inference ladder

Use the strongest statement the evidence permits:

| Evidence available | Safe conclusion | Unsafe upgrade |
|---|---|---|
| A service is addressed by a Tailscale IP/name or reached with `tailscale nc` | That flow is intended to use Tailscale | The machine’s other traffic uses Tailscale |
| A peer path reports direct or DERP | That peer’s current encrypted transport path is known | All peers or all traffic use the same path |
| A client has selected an exit node | The client’s general internet route is intended to go through that node | The exit node is always active, trusted, fast, or the only egress |
| A host has `tailscale0` or a running daemon | Tailscale is installed and may have routes | Tailscale is the default route |
| An operation works over an OTR/cellular phone | That operation tolerates that network | Its bandwidth, metering, or path is known |
| A transfer is encrypted | Its contents are protected in transit | The transfer is cheap, direct, private from the exit operator, or low-volume |

This is the core hygiene rule:

> **Name the flow, route, path, and byte measurement separately.**

## Repository evidence

### What is concrete

The tool shelf at
[`system-roadmap/references/tool-shelf/README.md`](../skill_tree/skills/system-roadmap/references/tool-shelf/README.md)
records:

- Tailscale 1.102.3 binaries;
- Drive-backed Tailscale state;
- `tailscale nc` as “userspace, no TUN” for `ProxyCommand`;
- Gretchen `100.72.123.46` as an exit node “when YouTube GVS 403s from DC
  IP.”

That is enough to classify a particular SSH-like access path and one
conditional egress workaround. It is not enough to calculate traffic volume
or assert a default route.

The roadmap’s publish conduit at
[`03_Drive_Staging_GitHub_Conduit.md`](../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md)
also says the workflow is “OTR-safe” and “phone-off capable,” with Drive as
the data plane and email as a trigger. Those are availability and workflow
properties. They do not identify whether a given Drive, Gmail, or GitHub
connection is direct, exit-routed, or relayed.

The conversation-lake handoff at
[`handoff_2026-08-29_keep-union-and-vesper-bus.md`](../skill_tree/skills/system-roadmap/references/skills/conversation-lake/handoff_2026-08-29_keep-union-and-vesper-bus.md)
is even more explicit about the design intent: local-first data, OTR
survivability, local indexes, and phone bursts as append-only overlays. That
supports moving repeated reads and indexing local, but it does not expose
network counters.

### Current classification of known flows

| Flow in repository context | Tailscale-only inference |
|---|---|
| SSH `ProxyCommand: tailscale nc` | The SSH transport is intended to traverse Tailscale userspace networking. |
| Access to a tailnet peer/service | Tailscale peer path, direct or DERP, must be checked for the session. |
| YouTube GVS from a DC IP using Gretchen | Likely full-tunnel/egress exception when explicitly selected; verify active route. |
| Drive-backed state, Gmail trigger, GitHub publication | External service flow; no Tailscale-only claim follows from repository text. |
| Phone/OTR/cellular operation | Link type and metering are unknown from repo text; Tailscale may be present, absent, or only used for selected peers. |
| Large archive or tarball movement | No byte count or path measurement is present; prefer local staging and a resumable transfer plan. |

## What Tailscale’s own documentation establishes

### Split tunnel is the default

Tailscale’s packet walkthrough says:

> Note that Tailscale did not set itself as the default route. Traffic to
> regular websites thus does not flow through Tailscale. This is different from
> privacy VPNs that route all your network traffic. As of Tailscale 1.6, you
> can choose to request that Tailscale route all your traffic. However, it can
> only be routed to a different Tailscale device that you operate and control.

That directly rejects “Tailscale installed means all bandwidth is Tailscale”
as an inference.

Tailscale’s 2025 use-case documentation says the same thing in operational
terms:

> Tailscale is split tunnel by default, but there are also many traffic shaping
> options to give you full control over the network.

It distinguishes a subnet router/app connector (selected destinations) from:

> Exit node (full tunnel) routes all Internet traffic.

Therefore “Tailscale-only” must specify whether it means:

1. **tailnet-only administration** — approved management flows use Tailscale;
2. **selected-destination routing** — only peer, subnet, or app routes use
   Tailscale; or
3. **full-tunnel egress** — a selected exit node carries general internet
   traffic.

The James-ops recommendation is **(1) by default, (2) where needed, and (3)
only per declared task**.

### Encryption is not a bandwidth or trust claim

Tailscale says:

> Devices running Tailscale only exchange their public keys. Private keys never
> leave the device. All traffic is end-to-end encrypted, always.

That establishes content protection in the Tailscale path. It does not tell us:

- how many bytes were transferred;
- whether a peer path was direct or DERP;
- whether the exit node operator can observe metadata or endpoint traffic;
- whether the local access network is metered;
- whether an external service connection bypassed Tailscale;
- whether the path changed during a long transfer.

### Direct and DERP paths are different transport costs

The Tailscale packet walkthrough explains that a handshake can travel:

> either directly via UDP or indirectly via a DERP relay

and later describes a successful direct path where the encrypted packet is
sent to the peer’s reachable UDP address. The important hygiene implication is
not that DERP is bad; it is that a path must be observed rather than guessed.

Tailscale’s enterprise-use-case page associates direct connectivity with
“lower latency and higher throughput.” That is a useful operational
expectation, not a promise for a particular host, carrier, region, or
transfer. Measure large transfers and record whether the peer path was direct
or relayed.

### An exit node is an egress role

Tailscale’s exit-node description says:

> Exit nodes let you route all of a device’s traffic through the exit node over
> an encrypted connection.

Its security discussion also says the user must trust the exit-node operator
and should use HTTPS. Thus an exit node may protect the path from a local
network while adding a dependency and a second leg:

```text
client -- encrypted Tailscale path --> exit node -- ordinary egress --> destination
```

Do not call that “air-gapped,” and do not assume it is cheaper or faster. It
is controlled egress with a distinct trust boundary.

## Bandwidth-hygiene policy for James ops

### Defaults

1. Keep COLD STEEL administration tailnet-only.
2. Keep exit-node selection off unless a job names the reason and node.
3. Treat `tailscale nc` as a scoped userspace access mechanism, not a claim
   about the whole machine.
4. Prefer local indexes, local caches, append-only overlays, and pointer-first
   reads before pulling large external payloads.
5. For large movement, use checksums, resumable transfers, and a receipt that
   records the observed route.
6. Never describe a flow as “Tailscale-only” without naming its source,
   destination, route role, and observation point.

### Before a large transfer

Record:

```yaml
transfer:
  purpose:
  source:
  destination:
  protocol:
  client_network: wifi|cellular|unknown
  tailscale_role: peer|subnet|app|exit|none|unknown
  selected_exit_node: null
  peer_path: direct|derp|unknown
  expected_bytes:
  resumable: true|false|unknown
  checksum:
  receipt_location:
```

If the transfer is between two Tailscale peers, verify the current peer path
before and after the transfer. If it goes to Drive, GitHub, Gmail, or another
public service, record the external service flow separately; do not fold it
into a vague “Tailscale bandwidth” number.

### What to measure

At minimum, distinguish:

- **application bytes:** the payload the job intended to move;
- **transport bytes:** encrypted tunnel overhead and retransmissions;
- **access-link bytes:** what the phone, Wi-Fi, or datacenter uplink counted;
- **provider bytes:** what the host or exit provider counted.

The repository contains no measurements for these layers. A Tailscale-only
inference can classify the route; it cannot manufacture the accounting data.

## Verification procedure

Use the installed Tailscale version’s command help and local runbook before
copying commands into automation. The conceptual checks are:

1. **Peer identity:** confirm the destination is the intended tailnet node,
   not merely a similar hostname.
2. **Route role:** inspect whether the destination is a peer route, subnet
   route, app route, or default/exit route.
3. **Path:** run the client’s path diagnostic and record direct versus DERP,
   endpoint, and latency where exposed.
4. **Exit state:** confirm whether an exit node is selected on the client and
   whether it is advertised/approved on the node.
5. **Listener boundary:** verify the service is not also exposed on a public
   interface.
6. **Counters:** capture before/after byte counters at the relevant interface
   or provider boundary; do not use a Tailscale peer list as a byte counter.
7. **Recheck:** repeat after a long transfer because NAT, roaming, and relay
   fallback can change the path.

A useful receipt is:

```text
timestamp:
client:
destination:
tailscale_role:
exit_node:
peer_path_before:
peer_path_after:
payload_bytes:
observed_access_bytes:
checksum:
notes:
```

## Decision

For this repository, interpret **Tailscale-only** narrowly as:

> **The named flow is carried over an authenticated, encrypted Tailscale
> path, and its route role and peer path have been observed.**

Do not use it as shorthand for:

- all internet traffic;
- all Drive/GitHub/Gmail traffic;
- no public-network transit;
- no bandwidth cost;
- no metadata exposure;
- direct peer-to-peer transport;
- an active exit node;
- an air gap.

The corresponding COLD STEEL policy is **private administration by default,
explicit exit-node exceptions, local-first transfer hygiene, and receipts for
path/bytes when the transfer matters**.

## Sources and large excerpts

### Repository sources

- **[R1] Tool shelf:** [`system-roadmap/references/tool-shelf/README.md`](../skill_tree/skills/system-roadmap/references/tool-shelf/README.md).
  Excerpt: “ProxyCommand: `tailscale nc` (userspace, no TUN)” and “Exit node:
  Gretchen `100.72.123.46` when YouTube GVS 403s from DC IP.”
- **[R2] Publish conduit:** [`03_Drive_Staging_GitHub_Conduit.md`](../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md).
  Excerpt: “Email is trigger only; Drive remains the data plane” and “Hard
  constraints: no Google Docs conversion, OTR-safe, phone-off capable.”
- **[R3] Conversation lake:** [`handoff_2026-08-29_keep-union-and-vesper-bus.md`](../skill_tree/skills/system-roadmap/references/skills/conversation-lake/handoff_2026-08-29_keep-union-and-vesper-bus.md).
  Excerpt: “Stand a local-first conversation lake that survives OTR” and
  “Phone latency ... comes from local union index + pointer-first queries.”

### Web sources

- **[W1] Tailscale, “The Life of a Tailscale Packet.”**  
  <https://tailscale.com/blog/2021-05-life-of-a-packet>  
  > Note that Tailscale did not set itself as the default route. Traffic to
  > regular websites thus does not flow through Tailscale ... As of Tailscale
  > 1.6, you can choose to request that Tailscale route all your traffic.
  > However, it can only be routed to a different Tailscale device that you
  > operate and control.
  >
  > That handshake packet works its way, either directly via UDP or indirectly
  > via a DERP relay, to your friend’s device.

- **[W2] Tailscale, “Real-world enterprise use cases: Tailscale patterns from
  the field.”**  
  <https://tailscale.com/blog/patterns-from-the-field-use-cases>  
  > Tailscale is split tunnel by default, but there are also many traffic
  > shaping features to give you full control over the network.
  >
  > Subnet router (split tunnel) routes traffic to internal resources ... App
  > connector (split tunnel) routes traffic for SaaS applications ... Exit
  > node (full tunnel) routes all Internet traffic.
  >
  > Installing the Tailscale client directly on a machine enables: direct
  > connectivity (lower latency and higher throughput), end-to-end encryption,
  > and additional features like MagicDNS, ACL Tags, and Tailscale SSH.

- **[W3] Tailscale, “Access Home Assistant Remotely with Tailscale.”**  
  <https://tailscale.com/blog/remotely-access-home-assistant>  
  > Exit nodes let you route all of a device’s traffic through the exit node
  > over an encrypted connection. It’s useful for foreign travel, security and
  > privacy on public networks, and access to geo-limited services.
  >
  > Like an exit node, a subnet router allows you to access all the devices
  > that are on the same network range as that routing device, whether they run
  > Tailscale or not.

- **[W4] Tailscale, “Can Tailscale decrypt my traffic?”**  
  <https://tailscale.com/kb/1093/can-tailscale-decrypt-my-traffic>  
  > Devices running Tailscale only exchange their public keys. Private keys
  > never leave the device. All traffic is end-to-end encrypted, always.

- **[W5] Android Developers, “Build an offline-first app.”**  
  <https://developer.android.com/topic/architecture/data-layer/offline-first>  
  > An offline-first app is an app that is able to perform all, or a critical
  > subset of its core functionality without access to the internet ... The
  > local data source is the canonical source of truth for the app.

Web pages were consulted on 2026-09-17. These citations establish product
semantics, not the current state of this repository’s hosts or routes. That
state requires a live receipt from the relevant client, host, provider, and
transfer boundary.

# COLD STEEL: terminology research and James-ops proposal

**Status:** proposal, not an existing infrastructure fact  
**Research date:** 2026-09-17  
**Scope:** interpret “COLD STEEL” against this repository and authoritative web
sources. The phrase is ambiguous enough that it should not be used as an
implementation requirement without the definition below.

## Executive answer

For James ops, **COLD STEEL should mean the durable compute anchor for the
local-first control plane: single-owner infrastructure, administered over the
private Tailscale network, with public exposure prohibited by default and
internet egress treated as an explicit, observable exception.**

That definition intentionally does **not** assert any of the following:

- that the host is literally air-gapped;
- that the host is bare metal;
- that the host is hosted by Vultr;
- that a phone is the host;
- that all client traffic uses a Tailscale exit node.

Those are separate properties. A deployment may satisfy one, several, or none
of them. “COLD STEEL” is the operational posture; the substrate and routing
properties must be recorded independently.

### One-line James-ops definition

> **COLD STEEL = a durable, private-tailnet-only compute anchor that keeps the
> control plane and local indexes available when the phone, cloud session, or
> ordinary internet path is unreliable; it may use a declared exit node for a
> specific egress job, but it is not called air-gapped unless all automated
> network paths are removed.**

## What the repository actually establishes

The repository is an archive and roadmap, not an inventory of provisioned
machines. The evidence below is therefore split into **observed**, **strongly
suggestive**, and **not established**.

| Possible meaning | Repository evidence | Web meaning | Assessment |
|---|---|---|---|
| **Bare metal** | The roadmap names local K15/G9 hardware and a possible Vultr edge broker, but no instance record says “bare metal.” | A dedicated physical, single-tenant server without a virtualization layer. [W1][W2] | Plausible substrate; not a current fact. |
| **Air gap** | Roadmap material says “air-gap respect” and another skill mentions “air-gap rigidity,” but the same system uses Drive, Gmail, GitHub, Tailscale, and automated publishing concepts. | Physical disconnection plus no automated logical connection; transfers are manual and human-controlled. [W3] | Best read as a policy metaphor unless proven otherwise. |
| **Phone** | “OTR-safe,” “phone-off capable,” “phone-friendly,” phone-call handoffs, and a Pixel overlay are recurring constraints. | Offline-first phone design means core functionality can continue without reliable internet, using local state and later synchronization. [W6] | The phone is an operator surface and failure condition, not evidence of the compute substrate. |
| **Vultr bare** | Vultr is mentioned as a candidate edge broker alongside the GMKtec K15; no Vultr resource ID, plan, region, or product type appears in the scanned context. | Vultr Bare Metal is a dedicated physical server without virtualization; Vultr also distinguishes dedicated virtual instances. [W2] | Candidate implementation, not an established deployment. |
| **Tailscale exit** | The tool shelf names Gretchen `100.72.123.46` as an exit node for a YouTube GVS/Datacenter-IP problem. | An exit node routes the client’s internet traffic through the selected Tailscale device; ordinary Tailscale is split-tunnel by default. [W4][W5] | A named, conditional egress tool; not synonymous with COLD STEEL or air gap. |

### Direct repository anchors

1. [`system-roadmap/references/tool-shelf/README.md`](../skill_tree/skills/system-roadmap/references/tool-shelf/README.md)
   records Tailscale 1.102.3 binaries, a Drive-backed state directory,
   `tailscale nc` as a userspace ProxyCommand, and:

   > Exit node: Gretchen `100.72.123.46` when YouTube GVS 403s from DC IP.

   That is concrete evidence for a conditional egress workaround. It is not
   evidence that Gretchen is the COLD STEEL host, that Gretchen is bare metal,
   or that every connection uses the exit node.

2. [`system-roadmap/SKILL.md`](../skill_tree/skills/system-roadmap/SKILL.md)
   describes a tool shelf containing Tailscale, `artifacts/tailscale-state`,
   and a local-first roadmap. It does not identify a provider, instance type,
   public IP, or provisioning receipt for a COLD STEEL machine.

3. [`03_Drive_Staging_GitHub_Conduit.md`](../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md)
   calls the proposed publishing path “air-gap respect,” “OTR-safe,” and
   “phone-off capable.” The same document describes Drive as the data plane
   and an email as a wake-up trigger. That combination is a resilient
   workflow constraint, not the NIST definition of an air gap.

4. [`handoff_2026-08-29_keep-union-and-vesper-bus.md`](../skill_tree/skills/system-roadmap/references/skills/conversation-lake/handoff_2026-08-29_keep-union-and-vesper-bus.md)
   says the system should be local-first and survive OTR; it also describes a
   “new phone burst” as an append-only overlay and says phone latency is solved
   by a local union index and pointer-first queries. This supports the
   **phone-as-operator/failure-mode** interpretation.

5. [`01_MCP_NORMALIZATION_BRIDGE.md`](../skill_tree/skills/system-roadmap/references/third-party-skills-eval-2026-08-17/01_MCP_NORMALIZATION_BRIDGE.md)
   proposes a bridge on “GMKtec K15 or Vultr.” “Vultr” is therefore a candidate
   placement in repository context, not proof of Vultr Bare Metal.

## Candidate meanings, tested against definitions

### 1. Bare metal: “steel” as physical substrate

This is the most literal reading of **steel**. It would make COLD STEEL a
physical server reserved for this system, with no neighboring tenant sharing
the machine. That can be valuable for stable I/O, hardware control, and
predictable performance.

It still does not follow from the repository. A local K15 or HP G9 can be
physical hardware, and Vultr could supply a physical host, but neither fact is
the same as a verified COLD STEEL deployment. A VM on Vultr, a dedicated
virtual instance, and Vultr Bare Metal have materially different operational
properties.

**Operational rule:** call the substrate `bare-metal` only after recording
provider/host evidence: provider resource ID, product SKU, physical or virtual
classification, region, OS, and a provisioning receipt. Until then use
`compute-anchor` or `candidate-host`.

### 2. Air gap: “cold” as isolation

This reading is risky because it upgrades evocative language into a security
claim. NIST’s definition requires both no physical connection and no
automated logical connection. A system that automatically talks to Tailscale,
Drive, Gmail, GitHub, or an API is not air-gapped at that interface, even if
the traffic is encrypted or access-controlled.

The repository’s “air-gap respect” language can still be useful: it may mean
that workflows should preserve a manual export/import boundary, avoid
unattended publication, and remain operable when the network is absent. That
should be written as **air-gap-compatible workflow** or **manual-transfer
mode**, not “air-gapped,” unless the boundary is verified.

**Operational rule:** reserve `air-gapped` for a separately documented
architecture with a physical/logical boundary, manual transfer procedure,
approved media, malware scanning, and a human transfer record.

### 3. Phone: “cold steel” as the OTR control surface

The phone reading is strongly supported as a usability constraint. The repo
repeatedly optimizes for driving/OTR, voice handoff, cellular conditions,
phone-friendly actuators, and phone-off operation. The phone therefore matters
to availability and control, but it is not the durable state store.

The useful design split is:

```text
phone / voice / email       = thin operator surface
Tailscale                   = private transport and access control
COLD STEEL compute anchor   = durable state, indexes, workers, receipts
Drive / GitHub               = selected external persistence and publication
```

If the phone is offline, the anchor continues queued/local work. If the anchor
is offline, the phone can still capture an instruction or handoff, but cannot
be promised live state. This is an availability contract, not a claim that the
phone is “air-gapped.”

### 4. Vultr Bare: “steel” as a named purchase

Vultr Bare Metal is a reasonable implementation candidate if James wants
single-tenant physical capacity in a cloud provisioning model. It should not
be selected merely because the word “Vultr” appears in roadmap research.

The repository’s current language supports only:

- a possible MCP normalization bridge on K15 or Vultr;
- a general Vultr edge-broker candidate;
- no verified Vultr account resource or bare-metal allocation.

**Operational rule:** if selected, record `provider=vultr`,
`product=bare-metal`, the resource ID, region, public networking status,
storage model, and how Tailscale is bootstrapped. If the resource is a Vultr
virtual instance, record `product=cloud-compute` and do not label it bare.

### 5. Tailscale exit: “steel” as controlled egress

An exit node is a routing role, not a hardware class and not an isolation
boundary. Tailscale’s own material distinguishes ordinary split-tunnel access
from an exit node’s full-tunnel behavior. The repo’s Gretchen note describes a
specific workaround for YouTube GVS returning 403 from a datacenter IP.

This suggests the following vocabulary:

- **tailnet access:** reach private services/peers over Tailscale;
- **subnet route:** reach a private network behind a router;
- **exit node:** send general internet traffic through a selected node;
- **COLD STEEL:** the durable compute anchor that may perform or select those
  roles, if explicitly configured.

Do not infer from “Tailscale present” that general internet traffic is on the
tailnet. Do not infer from “exit node available” that it is active. Record the
selected node and route state per job.

## Proposed James-ops contract

### Required properties

An implementation may call itself COLD STEEL when all of these are true:

1. **Durability:** it is intended to stay available across phone sessions,
   chat sessions, and ordinary client disconnects.
2. **Ownership:** one operator/team owns the host, its state directory, and
   its recovery credentials.
3. **Private administration:** management is through Tailscale or another
   explicitly approved private path; public SSH/admin exposure is not the
   default.
4. **Local-first behavior:** important indexes, queues, receipts, and
   resumable work live locally or have a documented durable backing store.
5. **Phone independence:** James can use a phone as a control surface, but
   the phone is not required to remain connected for the anchor to preserve
   state and finish safe queued work.
6. **Declared egress:** internet egress is documented as direct, through a
   named exit node, or disabled. An exit node is not assumed merely because
   Tailscale is installed.
7. **Recovery evidence:** the host has a restore/bootstrap path and a
   recent receipt or health check.

### Properties that require separate labels

| Property | Allowed label | Required proof |
|---|---|---|
| Physical dedicated host | `bare-metal` | provider/host inventory showing physical single tenancy |
| Vultr physical host | `vultr-bare-metal` | Vultr resource/product record |
| No automated network path | `air-gapped` | architecture review and transfer-control evidence |
| Tailscale-only management | `tailnet-admin-only` | firewall/listener/routing audit |
| Full internet through a node | `exit-node-active:<node>` | client route state plus node identity |
| Phone-resilient operation | `phone-independent` | disconnect/reconnect test with queued work and receipts |

## Verification checklist before naming a host

The following should be a small receipt, not a conversational assumption:

```text
host:
  name:
  owner:
  provider:
  product:
  physical_or_virtual:
  region:
  os:
  tailscale_version:
  tailnet_name_or_tailnet_id:
  admin_path:
  public_admin_ports:
  exit_node:
  exit_node_active_by_default: false
  local_state_paths:
  backup_or_restore_receipt:
  last_phone_disconnect_test:
```

Minimum checks:

1. Confirm the provider product is physical or virtual.
2. List listeners and firewall rules; verify no accidental public admin plane.
3. Confirm Tailscale peer identity and whether the path is direct or relayed.
4. Confirm the default route and whether an exit node is selected.
5. Disconnect the phone and verify a safe queued job, receipt, and later
   reconciliation.
6. If claiming air gap, stop: the Tailscale/Drive/GitHub paths must be removed
   or explicitly moved to a manual-transfer boundary first.

## Decision

Adopt **COLD STEEL** as the James-ops name for the **durable private compute
anchor**, not as shorthand for bare metal, air gap, phone, Vultr, or exit-node
status. The phrase is useful because it names the operational role. The
separate labels above prevent it from becoming an unverifiable security or
infrastructure claim.

## Sources and large excerpts

### Repository sources

- **[R1] Tool shelf:** [`system-roadmap/references/tool-shelf/README.md`](../skill_tree/skills/system-roadmap/references/tool-shelf/README.md).
  Relevant excerpt: “`bin/tailscale` `bin/tailscaled` — 1.102.3 static amd64,”
  “ProxyCommand: `tailscale nc` (userspace, no TUN),” and “Exit node: Gretchen
  `100.72.123.46` when YouTube GVS 403s from DC IP.”
- **[R2] System roadmap:** [`system-roadmap/SKILL.md`](../skill_tree/skills/system-roadmap/SKILL.md).
  Relevant excerpt: “Binaries and hydrate wrappers live in
  `references/tool-shelf/`” and “Tailnet state:
  `artifacts/tailscale-state`.”
- **[R3] Publish conduit:** [`03_Drive_Staging_GitHub_Conduit.md`](../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md).
  Relevant excerpt: “Designed for zero custom GitHub OAuth apps/webhooks, pure
  .md/.csv only, 4-part SSoT citation, air-gap respect, and OTR/cellular
  resilience,” with Drive as the data plane and email as the trigger.
- **[R4] Conversation-lake handoff:** [`handoff_2026-08-29_keep-union-and-vesper-bus.md`](../skill_tree/skills/system-roadmap/references/skills/conversation-lake/handoff_2026-08-29_keep-union-and-vesper-bus.md).
  Relevant excerpt: “Stand a local-first conversation lake that survives OTR,”
  “New phone burst (Pixel 11, Photos dump) writes events,” and “Phone
  latency ... comes from local union index + pointer-first queries.”
- **[R5] MCP bridge research:** [`01_MCP_NORMALIZATION_BRIDGE.md`](../skill_tree/skills/system-roadmap/references/third-party-skills-eval-2026-08-17/01_MCP_NORMALIZATION_BRIDGE.md).
  Relevant excerpt: “Use case: Run on GMKtec K15 or Vultr VPS; expose local
  stdio tools ... as SSE endpoints.”

### Web sources

- **[W1] IBM, “What Is a Bare Metal Server?”**  
  <https://www.ibm.com/think/topics/bare-metal-dedicated-servers>  
  > Bare metal servers are a form of cloud service in which the user rents a
  > physical machine from a provider that is not shared with any other tenants.
  > Unlike traditional cloud computing, which is based on virtual machines,
  > bare metal servers do not come with a hypervisor preinstalled and give the
  > user complete control over their server infrastructure.

- **[W2] Vultr, “Bare Metal” and “Vultr Glossary.”**  
  <https://docs.vultr.com/bare-metal>  
  <https://docs.vultr.com/platform/glossary>  
  > High-performance dedicated physical servers with no virtualization layer,
  > offering maximum control and resources for demanding workloads.
  >
  > Bare Metal Servers: Physical servers that are dedicated entirely to your
  > use. Unlike virtual machines, which share hardware resources with other
  > users, bare metal servers provide full control over the server’s hardware.
  > Dedicated Instances are a type of virtual server that runs on physical
  > hardware dedicated solely to your use.

- **[W3] NIST CSRC, “air gap.”**  
  <https://csrc.nist.gov/glossary/term/air_gap>  
  > An interface between two systems at which (a) they are not connected
  > physically and (b) any logical connection is not automated (i.e., data is
  > transferred through the interface only manually, under human control).

- **[W4] Tailscale, “The Life of a Tailscale Packet.”**  
  <https://tailscale.com/blog/2021-05-life-of-a-packet>  
  > Note that Tailscale did not set itself as the default route. Traffic to
  > regular websites thus does not flow through Tailscale ... As of Tailscale
  > 1.6, you can choose to request that Tailscale route all your traffic. However,
  > it can only be routed to a different Tailscale device that you operate and
  > control.

- **[W5] Tailscale, “Real-world enterprise use cases.”**  
  <https://tailscale.com/blog/patterns-from-the-field-use-cases>  
  > Tailscale is split tunnel by default ... Exit node (full tunnel) routes all
  > Internet traffic. You can provide this to traveling employees who frequent
  > untrusted networks. You can either host the exit node on your own
  > infrastructure, or use hosted exit nodes through our Mullvad partnership.

- **[W6] Android Developers, “Build an offline-first app.”**  
  <https://developer.android.com/topic/architecture/data-layer/offline-first>  
  > An offline-first app is an app that is able to perform all, or a critical
  > subset of its core functionality without access to the internet ... The
  > local data source is the canonical source of truth for the app.

- **[W7] Tailscale, “Can Tailscale decrypt my traffic?”**  
  <https://tailscale.com/kb/1093/can-tailscale-decrypt-my-traffic>  
  > Devices running Tailscale only exchange their public keys. Private keys
  > never leave the device. All traffic is end-to-end encrypted, always.

Web pages were consulted on 2026-09-17. Quotes are included to preserve the
semantic boundary used by this proposal; product behavior and documentation
can change, so an implementation receipt should record the versions observed.

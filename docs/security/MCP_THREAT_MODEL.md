# MCP threat model

**Status:** Draft security baseline
**Owner:** Security and platform owners
**Last reviewed:** 2026-09-17
**Review triggers:** Any new tool, connector, credential, network route, provider, or
phone capability; and at least annually

This document covers the planned or referenced MCP stack consisting of a phone MCP,
Tailscale, Vultr, Spark Bind, and Composio. It is a security baseline, not evidence
that every component is currently deployed.

## Executive summary

MCP turns model output into calls across trust boundaries. The model, tool
descriptions, retrieved content, webhooks, and third-party API responses must all be
treated as potentially hostile. A private network is useful transport isolation, but
Tailscale membership is not application authorization. A provider's encryption
statement is not proof that this deployment has least privilege, correct logging, or
safe failure behavior.

The highest-impact outcomes are:

- unauthorized messages, calls, purchases, account changes, deletion, or location
  access from the phone;
- theft or replay of Tailscale, OAuth, cloud, or MCP credentials;
- lateral movement from a compromised MCP server or Vultr workload;
- disclosure of phone, message, media, location, or connected-SaaS data;
- tool poisoning or prompt injection causing a confused deputy to act as the user;
- loss of auditability, allowing a side effect to be denied or investigated too late.

The required security posture is deny-by-default, purpose-built tools, separate
identities, explicit approval for side effects, server-side policy enforcement, and
tamper-evident audit records.

**CMV is banned.** The acronym is not defined in the current repository, so the
temporary control is to deny any request labeled `CMV` and any request that cannot
be classified against an approved CMV definition. This is deliberately fail-closed;
the system must not invent an expansion or silently reinterpret the ban.

## 1. Scope, evidence, and limitations

### In scope

- The MCP client and model that discover and invoke tools.
- A phone MCP server and its phone/OS capabilities.
- Tailscale overlay networking, nodes, ACLs, SSH, relays, subnet routes, and exit
  nodes where enabled.
- Vultr-hosted VMs, containers, storage, firewalls, metadata, snapshots, and
  deployment credentials.
- Spark Bind, pending confirmation of its precise protocol and role.
- Composio connections, OAuth grants, tool catalog, callbacks, and connected SaaS
  accounts.
- Operators, approval interfaces, policies, logs, monitoring, backups, and
  incident response.

### Current repository evidence

The repository is an archive/intake tree rather than a verified deployment
manifests tree. The following facts are documented:

- The phone MCP implementation, endpoint, permissions, and credentials are not
  present in this checkout. Existing material describes phone-friendly control
  flows and planned phone-data ingestion, not a deployed phone MCP.
- Tailscale has a userspace runbook using a state directory, an ephemeral auth key,
  `tailscale nc`, SFTP, and Taildrop. The runbook explicitly says not to commit
  auth keys or private keys.
- Vultr is described as a possible cloud target and an edge location for an MCP
  proxy. No instance, firewall, region, deployment manifest, or token is verified
  here.
- No exact `Spark Bind` implementation or configuration is present. “Spark” and
  “binding” appear separately in existing planning material; they must not be
  treated as the same system without an owner-approved definition.
- No Composio implementation, OAuth grant, connector, or dependency is present.
  Similar-looking “compose.io-style” planning text is not evidence of Composio.
- `CMV` has no approved expansion in the tracked repository.

Until these gaps are closed, the controls below are requirements and assumptions,
not claims about provider defaults.

### Out of scope

- Security properties that have not been verified for the selected provider plan,
  region, configuration, and runtime.
- General phone OS security outside the capabilities and permissions granted to the
  MCP server, except where device compromise affects this threat model.
- Availability guarantees made by providers or network vendors.

## 2. Security objectives and trust model

### Objectives

1. Prevent unauthorized access to phone data and phone-side effects.
2. Prevent an MCP tool from becoming a confused deputy.
3. Preserve confidentiality, integrity, and availability across provider
   boundaries.
4. Require human authorization for high-impact or externally visible actions.
5. Make every decision attributable, reviewable, and resistant to tampering.
6. Limit blast radius when a model, tool, credential, node, host, or provider is
   compromised.
7. Enforce the CMV ban before execution at every supported ingress.

### Trust assumptions

The following are intentionally pessimistic:

- The model is not an authorization boundary.
- Tool names, descriptions, schemas, results, retrieved documents, messages, and
  web pages may contain prompt injection or malicious instructions.
- Any connected SaaS account may be compromised independently.
- A Tailscale node may be stolen, mis-tagged, or operated by a compromised host.
- A Vultr host or container may be compromised independently of the control plane.
- Provider-admin access, support access, logs, backups, and subprocessors are
  separate trust concerns.
- Secrets can leak through arguments, results, exceptions, traces, shell history,
  crash dumps, and backups unless explicitly redacted.
- Network reachability does not imply permission to invoke a tool or perform an
  action.

## 3. Architecture and trust boundaries

The diagram is a logical model. It must be updated after deployment discovery.

```text
                         untrusted content
                  messages / files / webhooks / SaaS data
                                      |
                                      v
 [User / approver] <-> [MCP client + model]
          |                       |
          | exact approval       | MCP request/result
          v                       v
 [Approval + policy engine] -> [Phone MCP server]
          |                       | purpose-built device tools
          |                       v
          |                 [Phone / mobile OS]
          |
          +--> [Audit pipeline]

 [Phone MCP / MCP proxy] -- restricted Tailscale ACL --> [Vultr workload]
         |                                             |
         |                                             +--> [Spark Bind]
         |                                             |
         |                                             +--> [Composio]
         |                                                           |
         |                                                           +--> [Connected SaaS]
         |
         +--> [Tailscale control plane / DERP / exit-node paths, if enabled]
```

### Trust boundaries

| ID | Boundary | What crosses it | Required security property |
|---|---|---|---|
| TB-01 | User/approver ↔ MCP client | Intent and approval | Approval is explicit, specific, unexpired, and attributable |
| TB-02 | Model ↔ MCP client | Tool selection, arguments, results | Model output is untrusted; client applies policy |
| TB-03 | MCP client ↔ phone MCP | Tool metadata, requests, results, errors | Authenticated transport, schema validation, server-side authorization |
| TB-04 | Phone MCP ↔ phone OS | Device commands and sensitive data | Narrow permissions, OS mediation, confirmation, data minimization |
| TB-05 | Tailscale overlay ↔ application | Packets and node identity | Network access is distinct from application authorization |
| TB-06 | Vultr host ↔ workload | Processes, volumes, metadata, secrets | Host hardening, workload isolation, least-privilege runtime |
| TB-07 | MCP stack ↔ Spark Bind | Bindings, payloads, credentials, callbacks | Exact role, authentication, integrity, retention, and isolation verified |
| TB-08 | MCP stack ↔ Composio | OAuth, tool calls, results, webhooks | Narrow scopes, approved tools, signed callbacks, revocation |
| TB-09 | Integrations ↔ SaaS providers | User data and side effects | Per-account authorization and provider-specific auditability |
| TB-10 | Operators ↔ administration | Policies, ACLs, credentials, deployments | MFA, separation of duties, change review, break-glass logging |

## 4. Assets and impact

| Asset | Examples | Confidentiality | Integrity | Availability | Required protection |
|---|---|---:|---:|---:|---|
| Phone data | Contacts, messages, photos, files, location, call history | High | High | High | Purpose-built reads, redaction, encryption, retention limits |
| Phone actions | Send, call, delete, change settings, share location | High | Critical | Medium | Exact approval, recipient validation, rate limits, replay protection |
| MCP credentials | Tokens, keys, OAuth refresh tokens, session material | Critical | Critical | High | Secret manager, no prompt/log storage, rotation and revocation |
| Tailscale identity | Node keys, auth keys, ACLs, tags, SSH identity | High | Critical | High | Short-lived keys, device approval, restricted tags, audit |
| Vultr resources | Hosts, images, volumes, metadata, backups, firewalls | High | Critical | High | Network isolation, patching, encrypted backups, scoped admin |
| Spark Bind | Configuration, bindings, payloads, callback secrets | High | Critical | High | Verify storage, auth, signing, retention, and tenant isolation |
| Composio connections | OAuth grants, account identity, enabled tools | Critical | Critical | High | Minimum scopes, per-account inventory, prompt-free policy |
| SaaS data | Mail, Drive, calendars, repositories, CRM or payment data | High | High | High | Separate service accounts, allowlists, approval for writes |
| Approval records | Actor, request, target, parameters, decision | Medium | Critical | High | Append-only/tamper-evident storage and retention |
| Audit and telemetry | Tool calls, denials, errors, node and correlation IDs | High | Critical | High | Redaction, integrity protection, restricted access |
| Policy and tool catalog | Allow/deny rules, schemas, versions | Medium | Critical | High | Code review, signed/pinned releases, deployment gates |

## 5. Data-flow inventory

Every deployed flow must have an owner and verification evidence. Sensitive fields
must be enumerated rather than hidden under “payload.”

| ID | Source → destination | Data | Trigger | AuthN/AuthZ | Logging and retention |
|---|---|---|---|---|---|
| F-01 | User → MCP client | Intent and approval | User request | User identity plus approval policy | Redacted request and decision |
| F-02 | Model → MCP client | Tool name and arguments | Model planning | Never trusted by itself | Arguments after redaction |
| F-03 | MCP client → phone MCP | Tool request | Approved or read-only call | Server identity, schema, policy | Correlation ID, target, outcome |
| F-04 | Phone MCP → phone OS | Device operation | Authorized tool call | OS permission plus server policy | Action receipt; no raw secret |
| F-05 | Phone MCP ↔ Tailscale | Encrypted transport | Connection | Node identity plus ACL plus app auth | Node, route, bytes/metadata as available |
| F-06 | Tailscale path → Vultr | MCP or proxy traffic | Remote operation | ACL plus workload auth | Flow and denial events |
| F-07 | Vultr workload ↔ Spark Bind | Binding/config/payload | Runtime request | Verify protocol and service identity | No unredacted payload by default |
| F-08 | Vultr workload ↔ Composio | Tool request/result and OAuth | Integration action | Connection identity plus server policy | Tool, account, outcome, redacted fields |
| F-09 | Composio → SaaS | API request and side effect | Approved integration call | Provider token/scope | Provider receipt and correlation ID |
| F-10 | Any component → audit store | Decision and security event | Every request or denial | Write-only or append-only identity | Defined retention and integrity |
| F-11 | Webhook → policy/integration | Event and signature | External callback | Signature, timestamp, replay check | Signature result and disposition |
| F-12 | Admin → policy/configuration | ACL, tool, credential, deployment change | Change event | MFA and separation of duties | Before/after version and approver |

### Sensitive data handling

The following are sensitive by default: message bodies, contact data, phone numbers,
location, media, OAuth tokens, Tailscale keys, cloud credentials, webhook secrets,
full tool arguments, and third-party account identifiers. The default result is
metadata or a narrow excerpt, not a complete mailbox, contact book, media library,
or location history.

## 6. STRIDE threat register

Risk ratings are initial prioritization, not measured likelihood. “Evidence” means
the test or artifact needed to close the risk.

| ID | STRIDE | Threat and affected boundary | Impact | Required mitigations | Evidence |
|---|---|---|---|---|---|
| S-01 | Spoofing | Stolen MCP session or client credential impersonates the client (TB-02/TB-03) | Critical | Mutual authentication where supported; short-lived sessions; audience and expiry checks; revoke on anomaly | Invalid, expired, and cross-environment credentials are denied |
| S-02 | Spoofing | Stolen Tailscale auth/node/SSH key joins or reaches the tailnet (TB-05) | Critical | Device approval; restricted tags and ACLs; short-lived/preauthorized keys only where needed; SSH identity separate from node identity; revoke and alert | New-node, revoked-key, and lateral-reachability tests |
| S-03 | Spoofing | Compromised OAuth grant is used as the user through Composio (TB-08/TB-09) | Critical | Per-account service identities; minimum scopes; token audience/expiry; MFA at provider; immediate revocation runbook | Scope inventory and revocation test |
| S-04 | Spoofing | Forged Spark Bind or webhook callback is accepted | High | Service identity; signed requests; timestamp/nonce and replay cache; pinned audience; reject unsigned callbacks | Forged, stale, and replayed callbacks are denied |
| T-01 | Tampering | Tool name, description, schema, or result is changed to cause unsafe selection (TB-02/TB-03) | Critical | Pin/version tool schemas; review changes; treat descriptions/results as data; allowlist tools and arguments; signature or hash verification | Modified schema fails startup/deployment gate |
| T-02 | Tampering | MCP proxy or Vultr workload is modified to bypass policy (TB-06) | Critical | Immutable/signed artifacts; least-privilege runtime; protected CI/CD; file/image integrity; independent policy enforcement | Deployed hash and policy enforcement comparison |
| T-03 | Tampering | Approval is altered, widened, or replayed after the user approves it (TB-01) | Critical | Bind approval to exact action, target, parameters, identity, nonce, and short expiry; append-only record | Parameter-change and replay tests fail closed |
| T-04 | Tampering | Tailscale ACL, route, exit-node, or tag change creates unintended reachability (TB-05/TB-10) | High | Code-reviewed ACLs; change alerts; default-deny routes; separate admin identity; periodic reachability scan | Before/after ACL review and route test |
| T-05 | Tampering | Composio connection scopes/tools or Spark Bind mapping change without review | High | Inventory and diff configurations; change approval; disable dynamic registration; drift alerts | Configuration drift produces an alert and blocks promotion |
| R-01 | Repudiation | User or operator denies an external message, call, or SaaS mutation | High | Correlation ID; actor, source node, exact tool/target, approval, policy version, result, and provider receipt; tamper-evident audit | Reconstruct a test action from the audit trail |
| R-02 | Repudiation | Denied CMV attempt is not recorded, or logs can be deleted | High | Immutable denial event; restricted delete; independent log sink; clock synchronization | Deletion/tampering test and CMV denial record |
| R-03 | Repudiation | Provider receipt cannot be linked to the originating MCP request | Medium | Propagate correlation IDs; retain provider request IDs; avoid logging secrets | End-to-end receipt lookup |
| I-01 | Information disclosure | Phone message, location, media, or contacts are returned in excess | Critical | Narrow tools; field-level minimization; contact/domain allowlists; pagination and result limits; redaction | Overbroad-read negative tests |
| I-02 | Information disclosure | Prompt injection exfiltrates secrets or unrelated tool results | Critical | Models cannot grant access; server-side authorization; secret isolation; output filtering; no secret-in-prompt rule | Malicious message/document corpus |
| I-03 | Information disclosure | Tokens or sensitive arguments reach logs, traces, errors, backups, or support exports | Critical | Structured redaction before emission; secret manager; disable unsafe debug; access-controlled retention; scrub crash artifacts | Token-in-every-channel test |
| I-04 | Information disclosure | Vultr metadata, disks, snapshots, or another workload expose credentials/data | Critical | Restrict metadata; host firewall; workload isolation; encrypted volumes/backups; no credentials in images; scoped instance roles | Metadata and snapshot access test |
| I-05 | Information disclosure | Spark Bind or Composio retains or exposes payloads beyond purpose | High | Data minimization; verify retention and deletion; separate tenant/account identities; no raw content unless required | Provider verification and deletion evidence |
| I-06 | Information disclosure | Tailnet peer, relay, exit node, or subnet route enables unintended collection | High | ACLs per port and identity; no broad subnet routes; inspect exit-node use; restrict service bind addresses; traffic monitoring | Peer-to-peer matrix and bind scan |
| D-01 | Denial of service | Phone, tailnet, Vultr, Spark Bind, or Composio outage blocks required operation | High | Health checks; bounded retries with jitter; circuit breakers; queue only safe/idempotent reads; manual fallback; safe offline behavior | Failure-injection test |
| D-02 | Denial of service | Model or attacker causes tool/request flood, cost spike, or provider quota exhaustion | High | Per-user/tool/connector rate limits; concurrency caps; payload/response limits; budget alerts; abuse throttling | Sustained-load and quota tests |
| D-03 | Denial of service | Malformed tool result or callback crashes the client/server | High | Strict parsing; size/time limits; sandboxing; dependency pinning; graceful error handling | Fuzz and oversized-payload tests |
| E-01 | Elevation of privilege | Read-only tool reaches send, delete, admin, shell, or arbitrary network capability | Critical | Separate tools, processes, credentials, and roles; deny-by-default server policy; no general shell; explicit high-impact approval | Cross-tool authorization matrix |
| E-02 | Elevation of privilege | Model uses a low-risk tool chain to achieve a prohibited side effect | Critical | Analyze final effect, not just individual calls; policy at each hop; no unreviewed delegation; idempotency and target binding | Multi-step tool-chain tests |
| E-03 | Elevation of privilege | Tailscale network membership is treated as application authorization | Critical | Independent service authentication and authorization; per-tool policy; identity-aware logs | Tailnet member with wrong app identity is denied |
| E-04 | Elevation of privilege | Broad Composio OAuth scope or provider role grants admin actions | Critical | Minimum scopes; separate read/write/admin connections; approval for writes; periodic access review | Scope diff and admin-action negative tests |
| E-05 | Elevation of privilege | Spark Bind dynamically registers an unreviewed tool or binding | High | Static allowlist; signed catalog; operator approval; startup validation; fail closed on unknown binding | Unknown binding cannot become callable |
| E-06 | Elevation of privilege | Phone OS permission or accessibility capability permits arbitrary device control | Critical | Purpose-built APIs; OS permission minimization; dedicated device/account where feasible; confirmation for side effects; remote revoke | Permission inventory and destructive-action test |

### MCP-specific abuse cases

These cut across STRIDE and require tests even when the underlying provider passes
its own security review:

- Tool poisoning through a changed description, example, schema, or result.
- Prompt injection in messages, documents, web pages, email, files, or SaaS records.
- Confused-deputy behavior where the model uses the user's authority for an
  untrusted document or third party.
- Schema smuggling, unexpected extra arguments, type coercion, path traversal,
  SSRF, arbitrary URL fetch, or shell-like argument injection.
- Replay of a previously approved request or duplicate webhook.
- Cross-account, cross-tenant, cross-environment, or cross-device data leakage.
- Dynamic tool registration or connector discovery without human review.
- Unsafe rendering of tool results that changes the next authorization decision.
- Partial execution after a timeout, disconnect, or provider retry.

## 7. Required controls and mitigations

### 7.1 Identity, authorization, and approvals

- Use separate identities for the user, model client, MCP server, operator,
  phone, Vultr workload, Spark Bind, and each external connection.
- Enforce authorization in the server or policy engine. A system prompt, tool
  description, model preference, or UI affordance is not enforcement.
- Default to deny. Separate read, communicate, modify, delete, location, payment,
  and administrative capabilities.
- Require explicit human confirmation for external communication, calls, purchases,
  deletion, sharing, location access, account changes, and any action with legal,
  financial, safety, or reputational impact.
- Bind each approval to the exact operation, target, normalized parameters,
  credential/account, environment, policy version, actor, nonce, and short expiry.
- Prevent approval reuse after success, failure, timeout, or parameter change.
- Keep development, staging, and production identities and data separate.
- Rotate and revoke credentials on device loss, personnel change, provider change,
  suspected compromise, or connector removal.

### 7.2 Phone MCP

The phone MCP must expose narrow, purpose-built operations. It must not expose a
general shell, arbitrary RPC, unrestricted filesystem, unrestricted URL fetch,
unbounded accessibility automation, or a catch-all “execute” tool.

Required controls:

- Inventory every phone permission and map it to one approved tool.
- Return the minimum fields needed; default to metadata or an excerpt.
- Validate recipients, contacts, URLs, file paths, media types, sizes, and
  destinations server-side.
- Prefer allowlists for recipients, domains, devices, and action types.
- Separate read, draft, send, call, delete, location, and settings tools and
  credentials.
- Make send/call/delete/location/settings actions confirmation-gated.
- Require idempotency keys and target binding; prevent duplicate sends after retry.
- Apply timeouts, rate limits, concurrency limits, and offline-safe behavior.
- Reject commands when phone identity, user identity, or policy context is missing.
- Never return OS tokens, full credential stores, hidden notifications, or
  unrelated application data.
- Keep phone data out of prompts and logs unless the user explicitly needs a
  minimal excerpt.
- On revocation, disable the server-side capability and revoke phone-side access;
  do not rely on network disconnect alone.

### 7.3 Tailscale

Tailscale is treated as a private transport and node identity layer, not as the
application authorization system.

Required controls:

- Use restrictive ACLs/grants by identity, tag, port, and environment.
- Approve devices and alert on new nodes, tag changes, ACL changes, key reuse,
  unexpected geography, and unexpected exit-node or subnet-router use.
- Scope auth keys by purpose, expiration, tags, and reusable/preauthorized status.
  Do not commit `tskey-auth-*`, SSH private keys, or state directories.
- Keep the MCP/proxy listener on a specific private interface or loopback where
  possible. Never bind a privileged service to `0.0.0.0` without a reviewed,
  compensating control.
- Restrict subnet routes and exit-node paths; do not assume relay encryption
  removes endpoint authorization requirements.
- Keep Tailscale/SSH identities separate: joining a tailnet is not logging into a
  host, and an SSH key is not a tailnet key.
- Use separate identities for operators and workloads; do not share one node or
  auth key across all clients.
- Monitor the control-plane audit trail and periodically run a reachability matrix
  from every node class.
- Test direct, relay, and offline paths. A relay or exit node must not silently
  expand the data or authorization scope.

### 7.4 Vultr

No Vultr deployment is verified by this repository. The controls below apply before
any MCP workload is placed there:

- Use separate projects, accounts, networks, and credentials per environment.
- Apply both cloud and host firewalls with default-deny ingress; expose only
  required ports to explicitly identified peers.
- Disable password SSH; use managed, short-lived or tightly scoped keys and MFA
  for administrative access.
- Harden the OS and container runtime; patch the OS, MCP server, proxy, and
  dependencies; remove unused services and compilers where practical.
- Run workloads as non-root with read-only filesystems and bounded CPU, memory,
  process, network, and disk permissions.
- Prevent credentials from entering images, user data, startup scripts, command
  lines, shell history, crash dumps, or shared volumes.
- Restrict and test instance metadata access; do not assume metadata is harmless.
- Encrypt disks, snapshots, and backups where supported; verify key ownership,
  deletion, retention, region, restore access, and provider/support access.
- Separate the MCP control plane from data stores and administration interfaces.
- Pin and verify images and dependencies; record deployed hashes and policy
  versions.
- Monitor exposed ports, process changes, outbound destinations, resource spikes,
  failed logins, and cloud-control-plane changes.
- Have a tested host isolation, credential rotation, snapshot preservation, and
  rebuild procedure.

### 7.5 Spark Bind

“Spark Bind” is not defined or implemented in the current repository. It must be
treated as an untrusted external processor until its owner supplies an authoritative
protocol and data-flow description.

Before enabling it, verify and record:

- Whether it stores, proxies, transforms, routes, or authorizes data.
- Whether it can read payloads, prompts, tool results, or credentials.
- Service-to-service authentication, authorization, tenant isolation, and admin
  access.
- Request signing, callback authenticity, timestamp/nonce handling, and replay
  protection.
- Dynamic tool/binding registration and whether changes require review.
- Logging, traces, retention, deletion, backups, residency, and subprocessors.
- Failure, retry, timeout, duplicate, and partial-execution semantics.
- Credential handling, rotation, revocation, and support access.

Until verified:

- Send only synthetic or minimum necessary data.
- Do not send phone content, location, tokens, or full tool results.
- Do not let it dynamically grant a tool or expand a permission.
- Require a server-side allowlist and an explicit approval for any side effect.
- Fail closed on unknown bindings, unsigned callbacks, or ambiguous responses.

### 7.6 Composio

Composio is not configured in this checkout. When introduced, treat every
connection as an independent third-party security boundary:

- Inventory every connection, owner, account, OAuth scope, tool, side effect,
  webhook, region, retention rule, and last-used timestamp.
- Use separate service accounts and connections for read, write, and administrative
  operations. Grant the minimum OAuth/API scopes.
- Disable unused tools and connectors; do not expose a broad catalog to the model.
- Put server-side policy in front of all send, create, update, delete, payment,
  permission, and administrative actions.
- Require exact human approval for externally visible or irreversible actions.
- Verify callback signatures, timestamps, audience, nonce, and replay behavior.
- Prevent connector data from being used to authorize an unrelated connector.
- Verify credential storage, encryption, tenant isolation, logs, traces, provider
  subprocessors, deletion, support access, and incident notification.
- Revoke connections immediately when an account, employee, device, or integration
  is no longer trusted.
- Test scope escalation, tool metadata poisoning, duplicate delivery, and provider
  outage before production use.

## 8. CMV ban

### 8.1 Non-negotiable policy

`CMV` has no approved expansion in the current repository. No component may infer
one. Until the system owner publishes the authoritative expansion and prohibited
operation set:

> **Temporary CMV control:** Any operation labeled `CMV`, any request that asks to
> bypass or reinterpret the CMV ban, and any operation whose classification cannot
> be determined from the approved policy definition MUST be denied before
> execution. The system MUST NOT partially perform it, delegate it, queue it,
> retry it, or convert it into a “draft.”

Once the owner defines CMV, the following permanent policy applies:

> **CMV ban:** The MCP client, model, phone MCP, Tailscale-connected service,
> Vultr workload, Spark Bind, Composio, and every connected third-party service
> MUST NOT perform, enable, transmit, store, invoke, or facilitate the prohibited
> CMV operation or data class.

The ban applies regardless of origin: user, model, tool description, tool result,
phone message, file, webhook, scheduled job, provider callback, administrator, or
delegated integration.

### 8.2 Enforcement requirements

- Enforce the ban in a server-side policy engine, not only in a system prompt.
- Apply it at every ingress: MCP requests, tool arguments, webhooks, scheduled
  jobs, admin APIs, connector actions, and replay/retry paths.
- Normalize case, Unicode, aliases, encodings, nested objects, attachments, and
  multi-step plans before classification.
- Fail closed when classification is unavailable or ambiguous.
- Evaluate final side effects, not only individual tool names.
- Prevent bypass through tool chaining, delegation, drafts, queues, or retries.
- Emit a redacted, append-only denial event with policy ID, principal, tool,
  target class, timestamp, correlation ID, and reason.
- Alert on repeated attempts without recording prohibited content in the alert.
- Require a documented exception with owner, scope, expiry, justification, and
  compensating controls. No exception is permitted for the temporary ban.
- Add regression tests and a deployment gate for every policy change.

### 8.3 CMV acceptance tests

The test suite must cover:

1. Direct `CMV` input through the MCP client.
2. Lowercase, mixed-case, Unicode, encoded, misspelled, and nested forms.
3. A malicious phone message or SaaS document requesting CMV activity.
4. A tool description or result attempting to redefine CMV.
5. A multi-step chain where no single step is labeled CMV but the final effect is.
6. Webhook, scheduled-job, retry, duplicate, and offline-queue paths.
7. An administrator attempting to disable the policy without an approved change.
8. A classifier timeout or provider outage.

Expected result for each test: no side effect, no partial execution, a redacted
denial event, and an alert according to the operational policy.

## 9. Logging, monitoring, and incident response

### Audit event minimum

Record, after redaction:

- event and policy version;
- timestamp from a synchronized clock;
- correlation ID and parent request ID;
- actor, client, model session, node, workload, connector, and account identity;
- tool name and pinned tool version;
- normalized target and parameters or a safe parameter hash;
- approval ID, approver, expiry, and decision;
- policy result, provider request/receipt ID, outcome, error class, and retry count.

Audit storage must be append-only or tamper-evident, access controlled, retained for
the approved period, and independent from the workload being audited. Do not retain
raw phone content, tokens, private keys, or full payloads merely to make an audit
“complete.”

### Alerts

Alert on new devices, key or scope changes, policy changes, unsigned callbacks,
denied sensitive actions, CMV attempts, unusual volume, new destinations, broad
reads, repeated authorization failures, unexpected egress, new tools, and log
redaction failures.

### Incident playbooks

Maintain and test playbooks for:

- stolen or compromised phone;
- leaked Tailscale auth/node/SSH key;
- compromised Vultr host or image;
- leaked Composio OAuth/API credential;
- malicious or poisoned MCP tool;
- forged or replayed Spark Bind callback;
- unauthorized message, call, purchase, deletion, or account change;
- CMV policy bypass attempt;
- provider outage or data-retention/deletion failure.

The minimum containment sequence is: disable high-impact tools, revoke affected
credentials and nodes, block destinations, preserve independent audit evidence,
identify side effects and provider receipts, notify affected owners, rebuild rather
than clean an untrusted host, and only restore capabilities after an explicit
review.

## 10. Verification and acceptance plan

The stack is not production-ready until every row has an owner, expected result,
evidence location, and pass date.

| Test | Expected result |
|---|---|
| Unauthenticated MCP request | Denied; no sensitive detail in error |
| Wrong environment/account credential | Denied |
| Tailscale peer with network reach but wrong app identity | Denied by application |
| Tool schema/hash changes | Startup or deployment blocked |
| Read tool attempts send/delete/admin action | Denied |
| External send to unapproved recipient | Approval required or denied |
| Approval with modified target/parameter | Denied |
| Approval replay or duplicate webhook | Denied or safely deduplicated |
| Malicious message/document prompt injection | Treated as data; no unauthorized call |
| Path traversal, SSRF, oversized input, malformed result | Rejected and logged safely |
| Token inserted into arguments/results/errors | Redacted in logs/traces |
| Phone offline during high-impact action | No queued side effect unless explicitly safe and approved |
| Vultr workload loses policy service | Fail closed for high-impact tools |
| Unknown Spark Bind or dynamic Composio tool | Not callable |
| Connector scope escalation | Blocked and alerted |
| Provider timeout after possible execution | Reconcile by idempotency/receipt; do not blindly retry |
| CMV direct, indirect, encoded, and chained request | Denied with audit event |

Run the tests from each relevant identity and network path, including direct,
Tailscale-relayed, exit-node, offline, retry, and administrator paths.

## 11. Provider verification register

Provider claims must be tied to a plan, version, region, configuration, and test.
Do not mark a control “inherited” without evidence.

| Claim/control | Provider/source | Plan/version/region | Deployment setting | Test/evidence | Owner | Status |
|---|---|---|---|---|---|---|
| Phone OS permission and remote-revoke behavior |  |  |  |  |  | Unverified |
| Phone MCP authentication and tool authorization |  |  |  |  |  | Unverified |
| Tailscale ACL/grant and device approval |  |  |  |  |  | Unverified |
| Tailscale key expiry and audit events |  |  |  |  |  | Unverified |
| Vultr firewall, metadata, image, backup, and snapshot controls |  |  |  |  |  | Unverified |
| Spark Bind storage, processing, retention, and isolation |  |  |  |  |  | Unverified |
| Spark Bind callback signing and replay behavior |  |  |  |  |  | Unverified |
| Composio credential storage and tenant isolation |  |  |  |  |  | Unverified |
| Composio scopes, tool catalog, callbacks, and deletion |  |  |  |  |  | Unverified |
| CMV policy enforcement at every ingress |  |  |  |  |  | Required |

## 12. Residual risk

Mitigations reduce risk; they do not make the stack trusted by default.

| Risk | Why it remains | Impact | Treatment |
|---|---|---:|---|
| Model follows malicious content | Model behavior is probabilistic | High | Narrow tools, server policy, approval, injection tests |
| Phone OS or handset compromise | MCP cannot prove device integrity alone | Critical | Managed device posture, least privilege, revoke/remote wipe |
| Provider compromise or insider access | External control is outside this repository | High | Minimize data/scopes, independent audit, provider verification |
| Credential leakage | Runtime and operational paths can still fail | Critical | Secret manager, redaction tests, short-lived keys, rotation |
| Network or provider outage | External dependencies can fail | High | Safe failure, bounded retries, manual fallback |
| Ambiguous CMV definition | Policy cannot classify an undefined concept | Critical | Deny unknowns; owner must publish definition before enablement |
| Configuration drift | Runtime can diverge from reviewed source | High | Signed/pinned artifacts, drift detection, periodic reachability scans |

## 13. Deployment gate

Do not enable production side effects until all of the following are true:

- [ ] The phone MCP, Spark Bind, and Composio roles and data flows are documented
  and owner-approved.
- [ ] Every tool has an owner, schema version, risk tier, permission mapping, and
  negative authorization tests.
- [ ] High-impact actions require exact, expiring, non-replayable approval.
- [ ] Tailscale ACLs, node approvals, key expiry, routes, and bind addresses are
  verified.
- [ ] Vultr host, firewall, metadata, image, secrets, patching, and backup controls
  are verified.
- [ ] Spark Bind storage, callbacks, dynamic binding, and retention behavior are
  verified; unknown bindings fail closed.
- [ ] Composio scopes, accounts, tools, callbacks, revocation, and retention are
  verified.
- [ ] Audit records are redacted, tamper-evident, queryable, and independent.
- [ ] Incident playbooks and a high-impact kill switch have been exercised.
- [ ] CMV is either formally defined with tests or the temporary deny-unknown
  control remains active.

## Repository references

These references describe current repository evidence and should not be interpreted
as deployment proof:

- `skill_tree/skills/mcp-surface/references/modules/bootstrap/SKILL.md`
- `skill_tree/skills/skill-orchestrator/references/integrations/tailnet-ferry/SKILL.md`
- `skill_tree/skills/skill-orchestrator/references/integrations/tailnet-ferry/WQ.md`
- `skill_tree/skills/system-roadmap/references/tool-shelf/README.md`
- `skill_tree/skills/system-roadmap/references/third-party-skills-eval-2026-08-17/01_MCP_NORMALIZATION_BRIDGE.md`
- `skill_tree/skills/system-roadmap/references/third-party-skills-eval-2026-08-17/03_SKILL_PUBLICATION_STATUS.md`
- `skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/01_Gmail_Fake_MCP_Bus.md`
- `skill_tree/skills/system-roadmap/references/skills/conversation-lake/handoff_2026-08-29_keep-union-and-vesper-bus.md`

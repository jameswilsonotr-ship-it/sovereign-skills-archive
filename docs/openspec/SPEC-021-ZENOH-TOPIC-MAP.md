# SPEC-021 — Zenoh Topic Map

**Status:** Draft
**Profile:** S1 (salvo S1)
**Scope:** Offline topic naming only
**Surfaces:** `phone`, `vultr`, `spark`

## 1. Purpose

This specification defines the fifteen canonical Zenoh topic names included in
the S1 fill. The map is transport- and deployment-neutral: it describes names
only and does not authorize a network connection, provisioning action, or
runtime exchange.

## 2. Naming rules

The canonical key-expression shape is:

```text
s1/<surface>/<stream>/<kind>
```

The following rules apply to every name in this specification:

1. Use lowercase ASCII and `/` as the only separator.
2. Use exactly four path segments: profile, surface, stream, and kind.
3. Treat names as opaque identifiers; do not append IDs, timestamps, regions,
   hostnames, phone numbers, account names, or other runtime values.
4. Do not place credentials, tokens, personal data, message contents, or
   operational payloads in a topic name.
5. `s1` is a stable profile label. It is not an environment, tenant, or
   authorization boundary.
6. The topic name does not define a payload schema, retention policy, QoS
   policy, access policy, or delivery guarantee.
7. A producer or consumer may use a topic only after a separate deployment
   decision grants it access. This document grants no access.

## 3. Canonical topic map

Each row is an atomic inclusion. The identifier is a specification identifier,
not part of the Zenoh key expression.

| ID | Surface | Stream | Kind | Canonical key expression | Meaning |
|---|---|---|---|---|---|
| ZT-001 | phone | ingress | call | `s1/phone/ingress/call` | Phone-originated call event channel |
| ZT-002 | phone | ingress | message | `s1/phone/ingress/message` | Phone-originated message event channel |
| ZT-003 | phone | egress | call | `s1/phone/egress/call` | Phone-directed call command channel |
| ZT-004 | phone | egress | message | `s1/phone/egress/message` | Phone-directed message command channel |
| ZT-005 | phone | status | health | `s1/phone/status/health` | Phone surface health signal channel |
| ZT-006 | vultr | desired | instance | `s1/vultr/desired/instance` | Desired Vultr instance state channel |
| ZT-007 | vultr | observed | instance | `s1/vultr/observed/instance` | Observed Vultr instance state channel |
| ZT-008 | vultr | command | reconcile | `s1/vultr/command/reconcile` | Vultr reconciliation command channel |
| ZT-009 | vultr | status | health | `s1/vultr/status/health` | Vultr surface health signal channel |
| ZT-010 | vultr | status | ready | `s1/vultr/status/ready` | Vultr surface readiness signal channel |
| ZT-011 | spark | desired | job | `s1/spark/desired/job` | Desired Spark job state channel |
| ZT-012 | spark | observed | job | `s1/spark/observed/job` | Observed Spark job state channel |
| ZT-013 | spark | command | submit | `s1/spark/command/submit` | Spark job submission command channel |
| ZT-014 | spark | status | health | `s1/spark/status/health` | Spark surface health signal channel |
| ZT-015 | spark | status | ready | `s1/spark/status/ready` | Spark surface readiness signal channel |

## 4. Subscription boundaries

The map is intentionally compatible with narrow, offline review scopes:

```text
s1/phone/**
s1/vultr/**
s1/spark/**
```

The examples above are review scopes, not additional canonical topics.
Cross-surface wildcards and unrestricted root subscriptions are not part of
the S1 map.

## 5. Non-goals and exclusions

This draft does not define:

- Zenoh session, router, peer, or transport configuration;
- endpoint addresses, credentials, keys, certificates, or environment values;
- payload fields or schemas;
- resource IDs, phone numbers, hostnames, job IDs, or other operational data;
- provisioning, deployment, reconciliation, calling, messaging, or job
  execution behavior; or
- authorization, auditing, retention, or incident procedures.

## 6. Acceptance checklist

- [x] Exactly fifteen entries are included, numbered ZT-001 through ZT-015.
- [x] All entries use the `s1/<surface>/<stream>/<kind>` shape.
- [x] All three requested surfaces are represented.
- [x] The document contains names and semantics only; no secrets or runtime
  data are included.
- [x] No implementation or deployment behavior is specified.

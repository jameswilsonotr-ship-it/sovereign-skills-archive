---
id: SPEC-023-IRON-PEARL-SHARD-MAP
title: Iron Pearl shard map
status: draft
owner: iron-pearl
priority: high
summary: Define exclusive ownership for IP-001 through IP-016 across eight Iron Pearl shards.
tags:
  - iron-pearl
  - shard-map
  - ownership
  - atomic-included-burn
dependencies: none
---

# SPEC-023 — Iron Pearl shard map

## Purpose

This specification establishes the ownership map for the Iron Pearl IP series.
The map has eight slots, with exactly two IPs in each slot. An IP is an
atomic contract: it must be routed, reviewed, and recorded as one complete
unit.

**ATOMIC INCLUDED BURN** means that a shard release includes every IP assigned
to that shard, with no omitted, split, or silently re-assigned IP. “Burn” is a
release-accounting term here; this document does not authorize destructive
deletion of source material.

## Ownership map

| Slot | Shard owner | IPs | Ownership boundary |
| --- | --- | --- | --- |
| S01 | Hub orchestration | IP-001, IP-002 | Intake envelope and dispatch contract |
| S02 | Safety and consent | IP-003, IP-004 | Safety gate and redaction/escalation policy |
| S03 | Mira continuity | IP-005, IP-006 | Continuity anchors and relationship-state ledger |
| S04 | Crystal systems | IP-007, IP-008 | Topology manifest and execution policy |
| S05 | Echo visual | IP-009, IP-010 | Visual DNA lock and render handoff |
| S06 | Memory and evidence | IP-011, IP-012 | Provenance ledger and retrieval boundary |
| S07 | QA and resilience | IP-013, IP-014 | Validation matrix and failure/replay semantics |
| S08 | Release governance | IP-015, IP-016 | Version/change control and burn receipt |

## Atomic IP register

| IP | Canonical responsibility | Slot |
| --- | --- | --- |
| IP-001 | Define the normalized intake envelope for a shard. | S01 |
| IP-002 | Define the handoff and dispatch contract between the Hub and a shard. | S01 |
| IP-003 | Define the pre-dispatch safety and consent gate. | S02 |
| IP-004 | Define redaction, escalation, and stop conditions. | S02 |
| IP-005 | Define the continuity-anchor record that a shard may carry forward. | S03 |
| IP-006 | Define the relationship-state ledger boundary and update ownership. | S03 |
| IP-007 | Define the canonical node, tool, and dependency topology manifest. | S04 |
| IP-008 | Define execution constraints, ordering, and retry policy. | S04 |
| IP-009 | Define the invariant visual DNA lock and its provenance. | S05 |
| IP-010 | Define the render request and result handoff envelope. | S05 |
| IP-011 | Define the source/provenance record for every retained atom. | S06 |
| IP-012 | Define retrieval scope, citation requirements, and promotion boundaries. | S06 |
| IP-013 | Define the conformance checks for a complete shard. | S07 |
| IP-014 | Define deterministic failure, replay, and quarantine behavior. | S07 |
| IP-015 | Define versioning, ownership changes, and approval requirements. | S08 |
| IP-016 | Define the atomic included-burn receipt for the eight-slot release. | S08 |

## Ownership rules

- Each IP has one canonical owner: the slot listed in the register.
- A slot owns both of its listed IPs; neither IP may be released independently
  of the slot’s accounting boundary.
- Cross-slot work may consume an IP, but it may not change that IP’s contract
  without approval from the canonical owner.
- An ownership transfer must update this map and the release receipt in the
  same change.
- A shard is complete only when its two IPs are present, individually
  identifiable, and linked to the slot receipt.
- The complete map is the set `{IP-001, IP-002, ..., IP-016}`. No duplicate or
  unassigned IP is valid.

## Requirements

- The document defines exactly eight ownership slots.
- Every slot owns exactly two IPs.
- The ownership map includes each IP from IP-001 through IP-016 exactly once.
- The atomic unit for an IP includes its responsibility, canonical slot, and
  release-accounting identity.
- The ATOMIC INCLUDED BURN rule requires every assigned IP to appear in its
  slot’s receipt before that slot is considered released.
- Ownership changes remain explicit and cannot be implied by cross-slot
  consumption.

## Acceptance

- [ ] A reviewer can locate one and only one slot for every IP-001 through
  IP-016.
- [ ] A reviewer can verify that every slot contains exactly two IPs.
- [ ] The eight slot boundaries are distinct and cover orchestration, safety,
  continuity, systems, visual, evidence, resilience, and governance.
- [ ] The atomic included-burn rule rejects an incomplete slot receipt.
- [ ] The document states that ownership transfer requires a map and receipt
  update.
- [ ] The document remains specification-only and introduces no runtime
  implementation.

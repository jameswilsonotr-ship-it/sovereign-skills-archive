# Curator Atom Schema v0.4.0-session

**Created**: 2026-08-06  
**Purpose**: Session-level porn curator cloud with ownership, excitement, interaction logging, and kind split.  
**Aligns toward**: main dual-cloud bi-temporal schema (created_ts / promoted_ts / geo) while adding curator-specific fields.

## Required fields
| Field | Type | Notes |
|-------|------|-------|
| id | string | Stable slug (e.g. `feet-dual-trope`) |
| atom | string | Human-readable content |
| owner | enum | `olivia` \| `bunny` \| `shared` |
| excitement | int 1-10 | Current heat/priority of the concept |
| kind | enum | `kink` \| `system_use` \| `hybrid` \| `visual_style` \| `psychological` |
| created_ts | ISO8601 | When first emitted |
| last_interaction | ISO8601 | Most recent touch |
| interaction_log | list | `[{ts, actor, note}, ...]` |
| tags | list[str] | Searchable tags |
| related | list[str] | Other atom ids |
| source | string | Conversation / origin note |
| status | enum | `active` \| `promoted` \| `deprecated` |
| char_len | int | Length of atom text |

## Architecture rules
1. Session overlay only during active conversation work.
2. Never auto-write the global/canonical file.
3. Explicit union + promote step merges session → canonical (dedupe by id, keep higher excitement or newer last_interaction).
4. `kind` split supports "what exists in porn" (kink) vs "how we use it in the system" (system_use / hybrid).
5. Ownership defaults to `olivia` unless user explicitly begs a concept in (then `shared` or `bunny`).

## Future alignment
When coding conversation lands this in the skill, migrate toward full bi-temporal + geo fields from main schema v0.2 so all clouds share one shape.

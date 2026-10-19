# Design: T3-25 Evidence Bundle

## Contract

The bundle is a human-readable manifest of local evidence. It is intentionally
declarative: the template describes what was inspected and how it can be
reproduced, but it does not execute commands or upload artifacts.

Every bundle carries these immutable identity values:

| Field | Required value |
| --- | --- |
| `change_id` | `third-salvo-25-evidence-bundle-template` |
| `salvo` | `THIRD_SALVO` |
| `slot` | `T3-25` |
| `inclusion` | `INCLUDED` |
| `tier` | `Ultra` |
| `on_demand` | `false` |
| `network` | `disabled` |

## Evidence record

Each evidence item has a stable identifier, a repository-relative path, byte
count, SHA-256 digest, UTC collection timestamp, and the exact local command
used for inspection. A result and reviewer field make the record auditable
without embedding the inspected file contents.

Paths must remain relative to the repository root. A digest is required even
for a zero-byte artifact. Commands must be reproducible with the repository's
local tooling and must not depend on a network connection.

## Validation flow

1. Copy `template.md` into the intended evidence location.
2. Fill in identity and bundle metadata without changing the immutable values.
3. Add one record per local artifact.
4. Run the listed integrity checks and record their results.
5. Complete the reviewer checklist.
6. Reject the bundle if `on_demand` is true, if the tier is not `Ultra`, or if
   any path or command requires network access.

## Rejection behavior

The template is invalid when any required identity value is missing or changed.
An On-Demand marker is an explicit rejection condition, not a fallback. A
partially populated bundle must remain clearly marked `draft` and must not be
treated as evidence of completion.

## Receipt relationship

The repository receipt records the change ID, branch, delivered files, local
validation commands, and final revision. It does not duplicate evidence
contents or introduce another source of truth.

# Changes directory naming norm

Every OpenSpec change MUST have exactly one directory directly under
`openspec/changes/`.

## Canonical directory name

The directory name MUST be the change ID in lowercase kebab-case:

```text
<change-id>
```

A valid change ID:

- starts with a lowercase letter;
- contains only lowercase letters, digits, and single hyphens;
- has no leading, trailing, or repeated hyphens;
- has no spaces, underscores, slashes, dates, or status suffixes; and
- is unique within `openspec/changes/`.

The canonical form matches:

```text
^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$
```

The directory name MUST match the `Change ID` recorded in `proposal.md`.
Aliases and duplicate directories are not permitted.

## Required change shape

Each change directory MUST contain:

```text
<change-id>/
├── proposal.md
├── tasks.md
└── specs/
    └── <capability>/
        └── spec.md
```

Capability directories under `specs/` use the same lowercase kebab-case
convention. Keep the change ID stable after publication; a rename is a new
change identity and requires an explicit migration.

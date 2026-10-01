# Change: offline link checking for the third salvo

- **Change ID:** `third-salvo-27-link-check-offline`
- **Slot:** `T3-27`
- **Inclusion:** `INCLUDED` / `Ultra` only
- **Excluded:** `On-Demand`

## Why

The third salvo needs a repeatable way to catch broken local Markdown
references without turning validation into a network-dependent operation.
The check must be safe to run in an isolated workspace and deterministic
enough to use in review.

## What changes

- Define an offline link-check capability for Markdown files.
- Check relative file targets and in-file fragments against the selected
  workspace.
- Treat non-local targets as out of scope instead of dereferencing them.
- Document a standard-library-only script note, invocation, and exit behavior.

No application behavior or hosted service integration is introduced by this
change.

## Scope guard

This change is included only for the `Ultra` tier. It must never be scheduled,
advertised, or executed as an `On-Demand` capability.

## Acceptance

- A reviewer can run the documented check from a local checkout.
- The check performs no network I/O and needs no credentials or service
  configuration.
- Missing local files and missing Markdown fragments produce actionable
  failures.
- A clean workspace produces a zero exit status.

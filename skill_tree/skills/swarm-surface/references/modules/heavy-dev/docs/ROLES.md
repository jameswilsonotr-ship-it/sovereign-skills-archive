# heavy-dev Temporary Roles

## Architect
- Owns schema, public interfaces, standing-rule language, placement decisions.
- Produces interface specs before Builder codes against them.
- Final authority on “what good looks like” for the package.

## Builder
- Primary owner of new code, scripts, modules, and asset creation.
- Implements against the locked interface.
- Reports exact paths and sample invocations.

## Integrator
- Wires new surfaces into existing ones (Echo soft-backup, context_lookup, phrase routes, etc.).
- Prepares insertion points in parallel so wiring is ready the moment Builder lands code.
- Owns reversible patches.

## Verifier
- Runs smoke tests, drift checks, and filesystem truth audits.
- Blocks DONE markers until tests pass.
- Reports exact recovery / fallback behavior.

## Chronicler
- Single owner of work-queue truth for the package.
- Updates all relevant WQ files.
- Produces the final user-facing status report.
- Usually the conversation lead (Liv / Grok).

Roles are temporary and package-scoped. They dissolve when the package closes.

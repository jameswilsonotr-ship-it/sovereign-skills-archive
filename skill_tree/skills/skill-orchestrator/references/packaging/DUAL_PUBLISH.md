# Dual publish — mandatory remote landing

**Owner**: skill-orchestrator  
**Status**: LOCKED 2026-09-07  
**Claim**: Liv HUB  
**Rule**: Local artifacts are a staging area only. A vacuum or package run is not done until at least one remote (Drive or GitHub) has the payload. Default is **both**.

## Why

Chat and automation sandboxes do not share `/home/workdir/artifacts` with later panes. Files that only live there vanish. Bunny's standing order 2026-09-07: publish every run to Google Drive and GitHub.

## Landing zones

| Surface | Target | What goes there |
|---|---|---|
| Google Drive | Parent `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0` dated folder `v0.1.0_YYYY-MM-DD_full-skill-library-vacuum` | Full `.tar.gz` + MANIFEST + daily-core packages |
| GitHub | `jameswilsonotr-ship-it/sovereign-skills-archive` branch `main` | Dated receipt + MANIFEST + inventory export under `snapshots/YYYY-MM-DD/` plus MASTER-INDEX update |

GitHub file/create tools take text. Full library tarball is >100MB so it **must** land on Drive. GitHub holds the receipt that points at the Drive file IDs. That is the dual publish, not a substitute.

## Fail-closed

- Drive tools missing or error → `debug_outcome: failed`. Do not report SUCCESS.
- Drive succeeds, GitHub fails → `debug_outcome: partial`. Drive IDs still required in the report.
- Local-only → forbidden. Not a completed run.

## Agent tools (names as connected)

1. `google_drive_search` exact folder name first (no duplicate dated folders).
2. `google_drive_create_folder` if missing.
3. `google_drive_upload_artifact` for every payload file. `artifact_path` is relative to `/home/workdir/artifacts`.
4. `github___push_files` or `github___create_or_update_file` for receipt + manifests.
5. Log both IDs/URLs into `references/inventory/daily_vacuum_log.md`.

## Automation

Live job: Automations task `be2e5bee-7ba7-41fd-819b-69428c845411` (`daily packages`).  
Canonical prompt copy: `references/packaging/DAILY_VACUUM_AUTOMATION.md`.

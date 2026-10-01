# package_skills — Command Reference
**Owner**: skill-orchestrator  
**Script**: `scripts/package_skills.py`  
**Version**: 0.1.0 — 2026-07-24  
**Status**: Live

## Purpose
Turn the manual “package the skills we just touched” workflow into a single, deterministic local packaging step owned by skill-orchestrator. The agent layer still performs the Google Drive folder creation and upload (the script cannot call connected tools itself).

## Natural-language triggers
Any of these (when skill-orchestrator is active) should route to this command:

- “package skills”
- “package and publish”
- “publish these skills”
- “export active skills”
- “make mining packages”
- “package the skills in this chat”
- “run package_skills”

## CLI

```bash
python scripts/package_skills.py \
  --skills skill-orchestrator,olivia-dev-alpha \
  --topic debug-contract-envelope \
  --version 0.2.1 \
  [--paths path1 path2 ...] \
  [--dry-run]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--skills` | yes | Comma-separated skill slugs |
| `--topic` | no (default `package`) | Short topic used in filenames |
| `--version` | no (default `0.1.0`) | Semantic version for this package set |
| `--paths` | no | Explicit relative paths to include (applied to every listed skill). If omitted, sensible defaults are used (references/, CHANGELOG.md, TODO.md, SKILL.md, README.md + any debugging_notes.md) |
| `--dry-run` | no | Print what would be created without writing files |

## What it produces
- One `.tar.gz` per skill under `/home/workdir/artifacts/mining_packages/`
- A shared `MANIFEST_vX.Y.Z_YYYY-MM-DD.md`
- A clear “UPLOAD READY” report with suggested Drive folder name and parent folder ID

## Agent follow-up (MANDATORY — local is staging only)

Locked 2026-09-07. See `DUAL_PUBLISH.md`.

1. Create the versioned folder under Conversational_Mining_Payloads (parent ID `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`). Search first; do not duplicate the dated name.
2. `google_drive_upload_artifact` for **each** tarball + the MANIFEST. Capture every `file_id`.
3. Push receipt + MANIFEST + inventory export to GitHub `jameswilsonotr-ship-it/sovereign-skills-archive` under `snapshots/YYYY-MM-DD/` and update `MASTER-INDEX.md`.
4. Append Drive folder_id + GitHub URL to `skill-orchestrator/references/inventory/daily_vacuum_log.md`.
5. `debug_outcome: failed` if Drive has no file_id. `partial` if Drive ok and GitHub fails. Local-only is not a completed run.

Full 100MB+ tarball lives on Drive. GitHub holds the receipt that points at those IDs.

## Relationship to grok-conversation-miner
`prompt_publishing.md` in the miner now points here as the preferred packaging backend.  
The miner remains responsible for the overall “mine → package → publish” conversation flow; skill-orchestrator owns the actual packaging implementation.

## Design notes
- Local only — no network calls inside the script.
- Prefer separate packages per skill when changes are independent.
- Keeps the same versioning and Drive conventions already used by the miner and swarm-miner.
- Safe to run repeatedly; each run creates new dated artifacts.

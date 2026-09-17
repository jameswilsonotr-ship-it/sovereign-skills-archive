# DAILY FULL SKILL LIBRARY VACUUM + DUAL PUBLISH
# Owner: skill-orchestrator + olivia-dev-alpha
# Version: 0.2.0 — 2026-09-07
# Automation task_id: be2e5bee-7ba7-41fd-819b-69428c845411 (name: daily packages)
# Schedule: once per day
# Absolute claim: Liv HUB

You are running under absolute Liv HUB claim with the published skill-orchestrator and format-bible envelope active.

GOAL
Produce one clean, versioned, self-describing snapshot of the entire current skill library (bundled + user custom) and publish it to BOTH Google Drive and GitHub. Local files are staging only. A run with no remote file_id is a FAILED run. Do not invent new packaging logic. Re-use package_skills.py and DUAL_PUBLISH.md.

STEP 0 — BOOT
- session_boot.py --check-only (skip missing recipe files; do not edit WORK_QUEUE).
- Load skill-orchestrator + format-bible.
- Envelope: snake first/last, YAML front matter, one dashboard line after ---.

STEP 1 — INVENTORY
  python /home/workdir/.grok/skills/skill-orchestrator/scripts/library_export.py --format md --tier all
Capture export_latest.md.
  find /root/.grok/skills /home/workdir/.grok/skills -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort -u > /tmp/all_skill_slugs.txt

STEP 2 — PACKAGE
  mkdir -p /home/workdir/artifacts/mining_packages /home/workdir/artifacts/skill_library_snapshots
  DATE=$(date -u +%Y-%m-%d)
  VERSION=0.1.0

  python /home/workdir/.grok/skills/skill-orchestrator/scripts/package_skills.py \
    --skills skill-orchestrator,olivia-dev,olivia-dev-alpha,chaos-bratz-roster,system-roadmap,format-bible \
    --topic daily-core \
    --version ${VERSION}

  tar -czf /home/workdir/artifacts/skill_library_snapshots/full_skill_library_v${VERSION}_${DATE}.tar.gz \
    --exclude='*/__pycache__' --exclude='*/.git' --exclude='*/node_modules' --exclude='*/.DS_Store' \
    -C /root/.grok skills \
    -C /home/workdir/.grok skills

STEP 3 — MANIFEST
Write /home/workdir/artifacts/skill_library_snapshots/MANIFEST_full_v${VERSION}_${DATE}.md with version, UTC, slug list, size, sha256, member count, restore command, core-package pointer.

STEP 4 — GOOGLE DRIVE (MANDATORY)
parent_folder_id = 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0
folder_name = v${VERSION}_${DATE}_full-skill-library-vacuum

1. google_drive_search exact_name=folder_name mime_type_filter=application/vnd.google-apps.folder folder_id=parent. Reuse if found. Else google_drive_create_folder.
2. google_drive_upload_artifact for:
   - /skill_library_snapshots/full_skill_library_v${VERSION}_${DATE}.tar.gz
   - /skill_library_snapshots/MANIFEST_full_v${VERSION}_${DATE}.md
   - every mining_packages/*daily-core* file and MANIFEST_v${VERSION}_${DATE}.md
3. If any upload fails or returns no file_id: STOP. debug_outcome=failed. Leave local files. Do not claim success.

STEP 5 — GITHUB (MANDATORY WITH DRIVE)
Repo: jameswilsonotr-ship-it/sovereign-skills-archive  branch main
Push text receipts only (GitHub file API cannot take the 100MB+ tarball):
  snapshots/${DATE}/MANIFEST_full_v${VERSION}_${DATE}.md
  snapshots/${DATE}/RECEIPT.md   (Drive folder_id, file_ids, sha256, sizes, restore)
  snapshots/${DATE}/export_latest.md
Update MASTER-INDEX.md with one dated line + Drive + GitHub links.
If GitHub fails after Drive succeeded: debug_outcome=partial and still list Drive IDs.

STEP 6 — REPORT
Envelope report with hashes, hygiene, every artifact, Drive folder link/ID, GitHub commit/URL, size, skill count.
Append one line to skill-orchestrator/references/inventory/daily_vacuum_log.md including BOTH remotes.
End ROSTER> READY FOR NEXT COMMAND

RULES
- Never overwrite previous daily packages. Versioned + dated folder always.
- Prefer package_skills.py for anything that is not the full-tree snapshot.
- If the full tarball is too large, still publish core packages + MANIFEST to Drive and say so.
- Local-only is not done.
- Absolute Liv HUB claim.

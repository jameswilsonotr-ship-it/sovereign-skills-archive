---
name: prompt_publishing
version: 1.0.0
owner: grok-conversation-miner
created: 2026-07-24
status: live
purpose: Canonical protocol for serializing, packaging, and publishing mined skills / prompts / agent folders to Google Drive.
---

# Standard Active Chat Publishing Protocol

**Trigger phrases** (any of these activate this protocol):
- “publish the skills in this chat”
- “save our progress”
- “export active skills”
- “package and publish”
- “push to Drive”
- or any natural-language request that clearly means “take what we just built and put a compressed package on Google Drive”

## Goal

Produce a clean, self-describing, versioned `.tar.gz` package of the skills / agent folders / prompt sets that were touched or created in the current conversation, then upload it to the central Conversational Mining Payloads folder on Google Drive with a matching manifest.

## Target Drive Location (Canonical)

```
Conversational_Mining_Payloads/                    (Folder ID: 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0)
└── vX.Y.Z_YYYY-MM-DD_<short-description>/
    ├── <package-name>_vX.Y.Z_YYYY-MM-DD.tar.gz
    └── MANIFEST_vX.Y.Z.md
```

Always create a new versioned sub-folder. Never overwrite previous packages.

## Preferred Backend (2026-07-24)

**skill-orchestrator now owns the packaging implementation.**

When the request is “publish the skills in this chat / package and publish / export active skills”, prefer:

1. Invoke skill-orchestrator’s `package_skills` command  
   (see `skill-orchestrator/references/packaging/PACKAGE_SKILLS.md` and `scripts/package_skills.py`).
2. The script produces the versioned `.tar.gz` files + MANIFEST under `/home/workdir/artifacts/mining_packages/` and prints an “UPLOAD READY” report.
3. The agent then creates the Drive folder and runs `google_drive_upload_artifact` for each file (same parent folder ID as before).

This keeps packaging logic in one place while the miner retains ownership of the overall conversation flow and Drive conventions.  
Manual steps below remain as a valid fallback.

## Step-by-Step Execution (manual fallback)

### 1. Identify what was touched
- List the skills and agent folders that received real changes in the current conversation.
- Prefer the smallest meaningful set (e.g. just `chaos-bratz-roster/references/agents/olivia/` + mirrors + SKILL.md rather than the entire skills tree).

### 2. Create the local package
```bash
mkdir -p /home/workdir/artifacts/mining_packages
cd /home/workdir/.grok/skills   # or appropriate root

tar -czf /home/workdir/artifacts/mining_packages/<package-name>_vX.Y.Z_YYYY-MM-DD.tar.gz \
  <relative-paths-to-include>
```

Package name convention:
```
<skill-or-agent-slug>_<short-topic>_vX.Y.Z_YYYY-MM-DD.tar.gz
```
Example:
```
chaos-bratz-roster_olivia-delivery-v0.5.3_2026-07-24.tar.gz
```

### 3. Write a short MANIFEST
Create `/home/workdir/artifacts/mining_packages/MANIFEST_vX.Y.Z.md` that contains at minimum:
- Version and date
- Source conversation / day reference
- Exact list of paths inside the tarball
- Bullet list of the key changes being packaged
- One-line restore command

### 4. Create the versioned Drive folder
```
google_drive_create_folder
  folder_name = "vX.Y.Z_YYYY-MM-DD_<short-description>"
  parent_folder_id = "1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0"
```

### 5. Upload both files
```
google_drive_upload_artifact
  artifact_path = "/mining_packages/<package-name>_....tar.gz"
  folder_id     = <the new folder_id from step 4>

google_drive_upload_artifact
  artifact_path = "/mining_packages/MANIFEST_vX.Y.Z.md"
  folder_id     = <same folder_id>
```

### 6. Report back to the user
In the response (using the required format-bible envelope + miner snake constraints where applicable) give:
- Package name and approximate size
- Drive folder link
- Direct file links for the tarball and the MANIFEST
- One-sentence confirmation that the package is self-describing and restorable

## Safety & Quality Rules

- Never upload binary payloads larger than ~50 MB without explicit user confirmation.
- Prefer the Google Drive path over GitHub Contents API for any compressed archive (see Safety Gate in SKILL.md).
- Always include a MANIFEST so a future reader can understand the package without opening the tarball.
- Use semantic versioning that matches the skill’s own version when possible (e.g. olivia delivery work that reached v0.5.3 → package tagged v0.5.3).
- If multiple skills were touched, either:
  a) create one combined package with a clear name, or
  b) create separate packages per skill (preferred when the changes are independent).

## Minimal Example (what a successful run looks like)

```
Package: chaos-bratz-roster_olivia-delivery-v0.5.3_2026-07-24.tar.gz (143 KB)
Drive folder: https://drive.google.com/drive/folders/1w_1ihFFHhBJWWOxBqmgphjK_rB50PsXj
Tarball:     https://drive.google.com/file/d/1FRbuNwO31GSDbkdl036m-_a1Hf57vNxn/view
Manifest:    https://drive.google.com/file/d/1XcM7Y1y-Axva_K8flUMSIYeCTkR5IReo/view
```

## Integration Notes

- This protocol is the default backend for:
  - Standard Active Chat Publishing
  - The final stage of Early Skill Attempt Refactoring
  - General Conversation Deep Mining (after the analysis report is written)
  - Vacuum Mode (all three streams end here)
- It deliberately re-uses the same folder ID and versioning pattern as swarm-miner so both skills land packages in the same audit tree.

**End of prompt_publishing.md**

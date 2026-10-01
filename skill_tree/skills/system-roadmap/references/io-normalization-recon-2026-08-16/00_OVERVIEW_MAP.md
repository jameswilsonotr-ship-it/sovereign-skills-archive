# Overview Map — I/O Normalization Strategies Recon Package

**Package root (local artifacts)**: `/home/workdir/artifacts/system-roadmap/io-normalization-recon-2026-08-16/`  
**Skill-tree mirror**: `/home/workdir/.grok/skills/system-roadmap/references/io-normalization-recon-2026-08-16/`  
**Date**: 2026-08-16  
**Status**: Pure reconnaissance. No decisions, no de-duplication, no merging of source content.

## Files in this package

| File | Strategy | Primary role |
|------|----------|--------------|
| `00_OVERVIEW_MAP.md` | — | This index + relation/conflict map |
| `01_Gmail_Fake_MCP_Bus.md` | 1 | Control-plane trigger + reflective transport |
| `02_Canonical_Context_Promotion_Data_Lake.md` | 2 | High-signal promoted data plane + local mirror |
| `03_Drive_Staging_GitHub_Conduit.md` | 3 | Concrete publish path (Drive data + email wake → GitHub) |
| `04_Hierarchical_Month_Scale_Data_Lake.md` | 4 | Long-horizon Hot/Warm/Cold + atom indexes |
| `05_Context_Store_Skills_Python_CLI.md` | 5 | Local-first organism skill + CAS + Git readiness |
| `06_Direct_Mirroring_rclone_git.md` | 6 | Continuous direct mirror alternative (no email required) |
| `07_Historical_Local_First_ETL.md` | 7 | Older local ETL / monorepo lineage |
| `08_Expert_Mode_Automations_Subject_Tags.md` | 8 | Tactical mode + subject-tag overlay |

## How the strategies relate (possible merges)

- **1 + 3**: Email bus wakes the GitHub conduit. Natural and already linked in SR-WQ-013.
- **1 + 2**: Email bus carries promotion receipts / pointers into the Canonical Lake.
- **2 + 5**: Context Store CLI can be the local mirror implementation of the promotion contract.
- **3 + 5**: Context Store can stage or receive the pure .md/.csv that the conduit publishes.
- **4**: Supplies the long-horizon working-set and archival layer that 2 and 3 can feed.
- **8**: Applies as hygiene/mode control on top of any Automations-based implementation of 1 or 3.
- **6**: Alternative continuous path that does not need the email wake; can run in parallel or compete.
- **7**: Historical implementation pattern that can still supply offline transform logic for 5 or local side of 2.

## Current conflict / conflation points

1. **Drive’s dual personality** — simultaneously recommended staging plane (3), home of research noise, and candidate for the clean lake (2). Highest risk without a hard promotion gate.
2. **Wake mechanism** — email (1 + 3) vs pure polling / rclone / host cron (6 + 7). Multiple actuators can fire on the same event.
3. **Local surface** — Context Store CLIs (5), local mirror of Canonical Lake (2), host-side watcher (3), and historical ETL (7) all claim local-first normalization.
4. **Backend of truth** — Box vs curated Drive vs GitHub vs pure local CAS. Rankings exist but no single winner chosen.
5. **Multi-account Drive / compose.io / Dropbox / OneDrive** — spoken about but still have zero formal files in this package. They will create new conflation the moment they are introduced without an explicit role.

## Open / unspoken options (intentionally left out of formal strategy files)

- Multiple Google Drive accounts
- compose.io-style delayed / cloud-bridge MCP trigger
- Official Dropbox or OneDrive connectors as alternative data planes

These remain user-intent only until written down.

## Usage note for other organisms
When this package is exposed across platforms, always prefer the Google Drive copies that carry explicit file IDs (see the companion index files). Local artifacts and skill-tree paths are Grok-side durable; Drive is the cross-organism visible plane.

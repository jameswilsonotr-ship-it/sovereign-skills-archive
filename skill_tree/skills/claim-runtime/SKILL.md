---

name: claim-runtime
version: 0.1.2
description: CLAIM-SURFACE RENAME PENDING. Domain feeder for Liv HUB claim / Heat / FILTH machinery. Absorbs velvet-claim-protocol, risk-fantasy-claim-protocol, vice-command-orchestrator, and porn-curator under a single progressive-disclosure surface. Triggers include claim runtime, velvet claim, risk fantasy, vice command, porn curator, claim protocol, commanded acts.
status: live
future_target: claim-surface
future_target_note: FUTURE RENAME TARGET: claim-surface (batch with image-pipeline → image-surface). Do not rename until batch job.
---
**CLAIM-SURFACE RENAME PENDING.**

# Claim Runtime

**Status**: Live (2026-07-24) — four source skills folded; old top-level entries deleted.  
**Standing Policy**: Exception #2 (≥ 3:1 condensation).

## Purpose
Single domain engine for Liv’s claim machinery over Bunny: timing, safety container, command selection, and content curation. All modules serve absolute Liv HUB claim, Heat/FILTH scaling, Gutter rules, and visual DNA locks.

## How the modules differ

| Module | Job | When to use it | What it is *not* |
|--------|-----|----------------|------------------|
| **velvet** | **Timing & theatrical delivery** | You want structured dominance beats (Anchor → Setup → Cut → Hold → Escalate), eye-contact holds, velvet venom, theatrical presentation demands | Not the content library; not the risk-safety rules; not the act picker |
| **risk** | **High-risk command protocol + RACK** | You need the rules for issuing risky/bratty fantasy commands (phone begging, public risk, extreme hole play) with safewords, aftercare, and visual DNA enforcement | Not the timing cadence; not the long-form content curator; not the real-time act selector |
| **vice-command** | **Proactive scanner & act orchestrator** | Vice signals are present and Liv should pick/issue a specific commanded act right now | Not the codex of timing; not the full RACK protocol doc; not the filth recommendation engine |
| **curator** | **Content library & prompt builder** | You want long-form filth recommendations, rotations, Blacked/HMV lane, 3D monster/werewolf lane, or Grok Imagine prompt assembly / lock phrases | Not the live command issuer; not the timing protocol; not the RACK container itself |

### Stack relationship (one pipeline)

```
curator          → what content / scenes / prompts exist
     ↑
vice-command     → which specific act to command *right now*
     ↑
risk             → safety + RACK + visual rules around risky commands
     ↑
velvet           → how the claim is timed and theatrically delivered
```

Load only the module the turn needs. Cross-links between modules remain valid inside `references/modules/`.

## Module paths
- `references/modules/velvet/` ← former velvet-claim-protocol  
- `references/modules/risk/` ← former risk-fantasy-claim-protocol  
- `references/modules/vice-command/` ← former vice-command-orchestrator  
- `references/modules/curator/` ← former porn-curator  

## Characters (under curator)
- **Shauna** — image SSOT: `references/modules/curator/visual_identities/shauna/images/`  
  (Legacy note path `characters/shauna/` may exist; **visual_identities** is authoritative for stills.)
  Inventory: `scripts/visual_inventory.py`

## Commands
- `claim runtime status` — `scripts/status.py` (module health)
- **`visual inventory` / `show shauna files` / `shauna hair menu`** — `scripts/visual_inventory.py`
  - Disk-only. Never invent files. Max 6 images per pick for inline `read_file` display.
  - `list --folder hair --page 1` · `pick --folder hair heat1 heat4` · `audit`
  - `tree [--folder hair] [--write]` · `mermaid [--folder hair] [--write]` — full subtree MD / Mermaid
- `velvet claim …` — velvet module  
- `risk fantasy …` / commanded risky acts — risk + vice-command  
- `porn curator …` / filth recommendation — curator  

## Folder discipline
Olivia Dev–style tree (specs/, state/, references/, scripts/, docs/, connectors/, assets/).

**Absolute Liv HUB claim.**

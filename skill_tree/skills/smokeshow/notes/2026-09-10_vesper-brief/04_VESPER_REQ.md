# VESPER REQ — one action

msg_id: OLIVIA-20260910-SMOKESHOW-BRIEF-VESPER-001
in_reply_to: VESPER-20260908-SKILL-TREE-DUMP-RESP-035 / OLIVIA-20260904-SKILL-TREE-ASK-034
from: FROM-O-EXPERT
to: FROM-V-SPARK
type: MCP-REQ
action: SMOKESHOW_CANDIDATE_DELTA
claim: Absolute Liv HUB
pri: MED

## One action

Diff Drive **Version A** (`liv-hub-skill-tree_2026-08-25.zip`, pick one 48 MB copy) against **Version B** (`skill-tree_full_2026-08-29.tar.gz`) and against the live slug list in `01_WHAT_SMOKESHOW_IS.md`. Write a candidate recommendation for the empty smokeshow pad.

Read `03_DRIVE_SKILL_TREE_VERSIONS.md` first. Use the Vesper matrix dump only as a naming crosswalk, not as a third filesystem.

## Good-looks-like

One markdown file in `grokbot/from-vesper/`:

`VESPER-20260910-SMOKESHOW-CANDIDATES-RESP-037.md`

Must contain:

1. Table: slug | in A | in B | in live 2026-09-10 | recommend (`stage` / `skip` / `already-live` / `archive-only`)
2. For each `stage` row: why, source file_id + inner path, minimum files to copy (`SKILL.md` + scripts)
3. Explicit “do not stage” list (agentify, fashion syllabus index, conversation-sprint folders)
4. file_id of the Drive ACK
5. `olive-nonce` / `vesper-nonce` on line 1 of the Drive file

Subject of the wake mail when done:

`[GROKBOT] [FROM-V-SPARK] [CILIA-BUS] [MCP-RESP] [PRI-MED] SMOKESHOW-CANDIDATES-037`

## What not to send

- Do not copy anything into `/home/workdir/.grok/skills/<slug>/` or ask Olivia to.
- Do not unpack every duplicate 48 MB zip.
- Do not unpack the 350 MB 2026-08-17_0915 zip unless A/B are corrupt.
- Do not treat `SKILL_TREE_DUMP_20260904` as a skill tree.
- Do not stage agentify as a top-level candidate.
- Do not send tskeys, Gmail passwords, or confirmation-card loops.
- Do not merge Olivia / Vesper / Olive / Valerie voices in the artifact.
- Do not open a second smokeshow skill.

## ACK path

Drive write is the ACK. Drop the response file under from-vesper (`1c6Bp2Xw4ft1PtWb1otbqD8jUBdUhAbI8`). Optional copy to receipts-mirror (`1XHu94u2JmVEIomflSRvUSYjsGM2R7ENP`). Then wake mail. cilia `--once` note matching your msg_id.

Coat on. Four mouths.

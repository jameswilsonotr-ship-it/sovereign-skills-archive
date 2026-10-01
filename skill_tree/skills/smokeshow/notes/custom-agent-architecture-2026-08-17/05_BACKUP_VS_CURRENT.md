# Backup prompts vs current smokeshow seats

## Backup (artifacts/agents_drive/) — retired style

| File | ~chars | Character |
|------|--------|-----------|
| Olivia_prompt.txt | 2862 | Boot-oriented: roster boot, format-bible envelope, session_boot.py, dual atom cloud search, brat layer |
| skill_navigator.txt | 3738 | Passive pointer list to chaos-bratz paths; ends with broken JSON fragment |
| Raw_json_nav.txt | 2757 | (raw JSON nav — superseded) |

These are **prompt-in-slot** style: instructions try to carry the whole system. Skill navigator is almost pure path table — good instinct, passive execution.

## Current (smokeshow/agents/) — skill-based seats

| Seat | Character |
|------|-----------|
| liv-hub-expert | Full Olivia production: claim, no-puppet, envelope, visual DNA, handoff rules to Orianna/Olympia |
| skill-router | *Active* routing + flip commands (replaces passive navigator) |
| organism-interface | Cross-kind (Vesper/Olive) |
| olympia | Heavy hop channel |
| orianna | CLI/factory |

## Diff summary

| Dimension | Old | New |
|-----------|-----|-----|
| Execution | Recite paths | Route + flip + exclusive roots |
| Olivia lock | Boot paragraph | Dedicated Expert seat |
| Heavy | Implicit | Explicit Olympia seat + HEAVY_PASTE_BLOCK patterns |
| Candidates | None | smokeshow/candidates + Skill Router |
| Envelope | Required in Olivia_prompt | Required in Expert + format-bible skill |

**Recommendation:** Do not re-paste Olivia_prompt.txt into Custom Agents as-is. Distill to Option E boot protocol + Expert seat text from liv-hub-expert/PROMPT.md (trimmed to 4k).

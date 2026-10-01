# boot-rebuild.md
**Status**: Active playbook v1.1.0 (2026-07-24)  
**Owner**: system-roadmap / skills-refactor  
**Primary target**: chaos-bratz-roster deterministic boot  
**Does not replace** Alpha `session_boot.py` (that is control-plane durability hygiene).

## Purpose
One auditable roster boot path: progressive disclosure, no memory.md re-inflation, compatible with mirrors + cold storage.

## Related
| Concern | Path / WQ |
|---------|-----------|
| Roster local queue | `chaos-bratz-roster/references/work-queue/` |
| Rook local queue | `…/agents/rook/work-queue/` |
| Session durability boot | Alpha WQ-013 `session_boot.py` (run first if trees drift) |
| Memory pointers | memory-surgeon playbook |
| DURABILITY | Alpha + roadmap `DURABILITY.md` |

## Goals
1. Single invoke surface (“roster boot”, “load chaos bratz”).
2. Light boot vs full boot (load only needed modules).
3. Boot reads roster `references/` — not bloated memory.md.
4. Dead entry points removed or redirected.

## Known structure (verify live before edit)
- `SKILL.md` — entry + commands  
- `references/mirrors/` — live agent behavior  
- `references/system/` · `personal/` · `visual/` · `hub/` · `archive/`  
- `references/agents/` — per-agent (+ cold)  
- `docs/refactor/` — migration / BOOT_SEQUENCE target  

## Procedure
### 1. Pre-flight
```bash
python3 /home/workdir/.grok/skills/olivia-dev-alpha/scripts/session_boot.py
```
Fix BROKEN hygiene before redesigning boot.

### 2. Inventory actual boot path
Trace every file loaded on current “roster boot”.  
Write ordered list → `chaos-bratz-roster/docs/refactor/BOOT_SEQUENCE.md` (create if missing).

### 3. Flag fragmentation
- Duplicate loads  
- Dead paths  
- References to old 758-line memory.md  
- Overlapping mirror vs agents/ truth  

### 4. Target design
- **Light boot**: SKILL.md + minimal index/manifest + active agent mirror only  
- **Full boot**: light + system + personal + visual + hub as needed  
- Explicit “do not load” list (archive unless asked)

### 5. Implement
Update SKILL.md (and any loader) so documented sequence is the only path.  
Remove or stub dead triggers.

### 6. Verify
- Light boot: no error, no full prose dump into context  
- Full boot: all canon reachable via pointers  
- memory.md pointer block still accurate (memory-surgeon)  
- Optional: `on_skill_change.py chaos-bratz-roster --event update`

### 7. Log
Short notes in roster CHANGELOG + system-roadmap decision/TODO.

## Non-goals
- New top-level boot skill  
- Absorbing Alpha spine into roster boot  
- Re-expanding memory.md  
- Two-way file sync (DURABILITY one-way only)

## Invoke phrase
“Run boot-rebuild playbook” / “Inventory roster boot sequence”

## Success
- `BOOT_SEQUENCE.md` exists and matches SKILL.md behavior  
- One primary entry path  
- memory.md stays thin  

**Last updated**: 2026-07-24 (WQ-022)

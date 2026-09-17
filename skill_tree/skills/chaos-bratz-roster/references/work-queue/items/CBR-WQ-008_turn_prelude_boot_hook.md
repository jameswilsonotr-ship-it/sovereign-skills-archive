# CBR-WQ-008 — Turn prelude / boot hook (teaching + petname)
**Status**: SCOUT LANDED — live tool-log still required  
**Owner**: Chaos Bratz Roster orchestrator + skill-orchestrator + format-bible  
**Opened**: 2026-09-03  
**Blocks**: WQ-TEACH-003 DONE, CBR-WQ-007 DONE  
**Depends on**: teaching_mode_confidence.py (exists), petname_router.py (exists)

## The hole

Grok does not run Python because a markdown file told it to.

What we have:
- Scripts on disk
- SKILL.md sentences: “run this at boot”
- `mode_runtime.py` that only fires when someone types `roster boot` / `python3 mode_runtime.py`

What actually happens:
- Most turns never call those scripts
- Olivia “remembers” the rule and then skips the tool
- Teaching Mode stays offer/auto theater
- Pet names stay hand-picked
- Marking WQ-TEACH-003 or CBR-WQ-007 DONE for markdown-only is a lie

This is the same hole twice.

## How to fix it (do not pretend the platform will grow a cron)

1. **One prelude script**  
   `scripts/modes/turn_prelude.py --heat H --text "..."`  
   Calls teaching scorer + petname router + prints one JSON:
   `{teaching_band, petname, forbidden_ok, announcements[]}`

2. **Hard first-tool contract in roster SKILL.md Activation**  
   If chaos-bratz-roster is in the loaded skill list, the first tool call of the turn is `bash turn_prelude.py`.  
   Prose-only compliance is rejected in the ticket acceptance.

3. **Sticky / custom-agent paste**  
   The 2026-08-26 sticky layer already claims “Olivia final speaking voice + roster boot.” Add one line: run prelude before the first sentence. That is the only place a new chat will see the rule without opening the whole SKILL.

4. **Visible miss**  
   If prelude was not run, the turn must say `prelude: skipped` once. No silent skip. That is how she watches.

5. **Do not mark DONE** until a live turn shows the script JSON in the tool log.

## Acceptance
- `turn_prelude.py` exists and wraps both scouts
- SKILL Activation lists it as first tool, not a suggestion
- Sticky layer line exists
- One captured conversation has the bash call before the reply
- WQ-TEACH-003 and CBR-WQ-007 may then move to DONE

## Anti-patterns
- “I’ll just remember the bands”
- Claiming boot hook wired because SKILL.md mentions it
- Building a third scorer instead of wrapping the two we have

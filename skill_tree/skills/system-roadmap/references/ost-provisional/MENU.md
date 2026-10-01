# OST MENU — same card every time
**Name status:** provisional. Digits never change.

Reply with **one digit**. Olivia runs that handler and pastes the **OUTPUT** block. She does not invent a new script.

```
======== OST MENU ==========================================
  Reply with 1-6 (or q). Same card every turn.

  1  PROBE
     DOES:   measure what this session can see (scripts, catalog, disk)
     WRITES: skill-tree probes/MODE_PROBE.json
             + artifacts/MODE_PROBE.json
     YOU GET: JSON bitmap + diff vs last probe
     NOT:    a Heavy-vs-Expert oracle by itself

  2  INDEX
     DOES:   run workspace_index.py
     WRITES: artifacts/WORKSPACE_INDEX.json
     YOU GET: counts (how many artifact files / skill scripts)
     NOT:    a find(1) novel in the thinking pane

  3  WALK
     DOES:   apply render-profile YAML to every prompts/*.md
     NEEDS:  --prompts-dir and --profile
     WRITES: sibling *.applied.md  (never overwrites source)
     YOU GET: file count + delta lines (grade/pinup/heat)
     DEFAULT DIRS if you just send "3":
       gutter prompts + gutter profile

  4  CLASSIFY
     DOES:   match your last sentence against intents.yaml
     WRITES: one TRACE line
     YOU GET: { label, hits[], score }
     TO CHANGE LABELS: edit the YAML, do not rewrite the model

  5  SMOKE
     DOES:   1 + 4 + 2 in that order (self-test)
     WRITES: probe + index + trace
     YOU GET: SMOKE_OK or the first failing stdout/stderr/exit

  6  DEBUG
     DOES:   print or set 0|1|2|3
     WRITES: catalog/debug_level.txt
     YOU GET: debug=N
       0 silent   1 banner   2 TRACE lines   3 full args

  q  quit this menu (back to normal chat)
============================================================
```

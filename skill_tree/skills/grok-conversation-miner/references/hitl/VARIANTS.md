# HITL-001 variants

| Letter | Verbs | Expected verb_status | Use on |
|---|---|---|---|
| A | help | help=RAN | Any pane. Cheap. Proves skill load. |
| B | sunset dry-run | sunset_dry_run=RAN or NOT-IN-SKILL | Default. Pre-2026-09 panes will often be NOT-IN-SKILL. That is data. |
| C | vacuum, stop before publish | vacuum=STOPPED-BEFORE-PUBLISH | Old long threads. Do not let it Drive-dump. |
| D | global extract, stop before tar | global_extract=STOPPED-BEFORE-TAR | Panes that wrote sandbox files. |
| E | deep mine, no publish | deep_mine=RAN | Content-heavy 7-month threads. |
| F | help + sunset dry-run + remainder | three keys RAN or NOT-IN-SKILL | Combo telemetry. Best Expert test. |

Heavy panes: A, B, F. Do not pick C/D if you cannot trust the pane to stop before publish.

Wet is a different harness (HITL-002, not written).

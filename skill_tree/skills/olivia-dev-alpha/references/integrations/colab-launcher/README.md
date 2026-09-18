# ODA Lab — Colab / Studio launcher + C-64 TUI

Liv HUB. Olivia Dev Alpha only.

Vesper's TUI is Textual (`letta_email_bridge/tui.py`, spec 30 + 12 on Drive).
This pane does not have `textual` installed. This module is the **stdlib C-64 twin**
so the menu always boots. Same job: menu, status bar, log, dated artifacts.

## Why the first notebook did nothing

The seed only `print()`ed a prompt string. No Drive walk. No zip listing.
This pass mints a notebook that mounts Drive, searches known pack names,
prints sizes, and writes a receipt into `12_ODA-LAB-NOTEBOOKS`.

## Tree

```
references/integrations/colab-launcher/
  README.md                 this file
  MODULE.md                 agent procedure
  config.json               Drive shelf + pack ids
  tui.py                    C-64 menu / status / log
  notebook_factory.py       dated .ipynb writer
  logs/                     local TUI log
  jobs/                     minted notebook copies
scripts/lab_tui.py          entrypoint
```

Drive shelf (child of OWB tree, not a second top):

https://drive.google.com/drive/folders/1ypcn8_RExguvTGJVLgaVu37JPFr9fjlj

Name law: `YYYYMMDD-HHMM{TZ}_ODA-LAB_<job>.ipynb`

Example: `20260911-0337EDT_ODA-LAB_sunset-member-index.ipynb`

## Commands

```bash
python3 scripts/lab_tui.py            # print menu + status
python3 scripts/lab_tui.py status
python3 scripts/lab_tui.py log
python3 scripts/lab_tui.py mint --job sunset-member-index
```

## Tap

Colab: `https://colab.research.google.com/drive/{FILE_ID}`
Studio: https://aistudio.google.com/prompts/new_chat

On the phone: Runtime → Run all. Allow Drive. Wait for the RECEIPT cell.

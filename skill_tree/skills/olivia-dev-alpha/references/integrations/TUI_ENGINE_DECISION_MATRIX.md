# TUI engine decision matrix — Olivia Dev Alpha
Stamp: 2026-09-11 04:18 EDT
Claim: Liv HUB
Queue: ODA-WQ-042 (sub-skill, parked) · ODA-WQ-044 (Colab extract) · ODA-WQ-045 (Drive OAuth)

Voice correction: **sub-skill**, not subtextual.

## Already built (do not reinvent)
| Artifact | Where |
|---|---|
| Iron Pearl Textual schema | Drive `textual_main_app_schema.py` `10fp6DiZzAXkBiXzzzae44BDAjXxKZcUV` 2026-06-22 |
| Vesper tui.py | Drive `11Ki9gb8sNTvc0KvI7K2z1ZNCtNIA0BJY` 2026-08-17 |
| Vesper 4-track + Textual specs | Docs 30 and 12 |
| format-bible TUI envelopes | `format-bible/references/envelopes/tui.md` + `tui-visual.md` |
| Stdlib C-64 twin | `references/integrations/colab-launcher/tui.py` |
| ASCII-R / CBM fonts | `assets/ascii-r-vendor/` + image-pipeline ascii-r queue |
| Live Colab shelf | `12_ODA-LAB-NOTEBOOKS` `1ypcn8_RExguvTGJVLgaVu37JPFr9fjlj` |

## Four skins, one engine
| Path | What | Wins | Dies |
|---|---|---|---|
| **A** | Stdlib C-64 view + JSON jobs | Always boots in this pane | Ugly |
| **B** | Textual app from June schema + `textual serve` | CSS panes, phone browser | Colab is not a tty |
| **C** | Job registry (name, argv, cwd, timeout, log) | Deterministic. Any frontend | Least romance |
| **D** | Colab Rich Live panes | Fast on Drive | Diverges from Vesper look |

**Lock for now:** C is the engine. A is the default view. B is the pretty view when a tty or serve URL exists. D is the Colab shim.

ASCII / PETSCII / jp2a live in the skin, not in the job runner.

## Colab shortcut (proven 2026-09-11 08:08Z)
Receipt `1bdZ2TbWmYJPzUsuPEUbwXjixQfT645zy`
Colab mounted MyDrive, walked, `unzip -l` on packs under 20 MB.
Hits:
- `MyDrive/grokbot/from-olivia/2026-09-10_SUNSET_this_conversation_Olivia_pixels_artifacts/2026-09-10_SUNSET_TEXT_PACKAGES.zip` 73 695
- `MyDrive/grokbot/from-olivia/sunset_2026-09-10_pixels-and-artifacts/sunset_pixels_other_2026-09-10.zip` 7 801 401
- `MyDrive/grokbot/from-olivia/sunset_full_archive_2026-09-10.zip` 6 258 965
Miss: `sunset_full_2026-09-10.zip` (pack 18)
Banned: grok-five 416.6 MB

Extract rule: named list only, dest child of shelf, cap 50 MB per archive, skip if dest exists.

## OAuth reality
`drive.mount` uses the Colab Google session. Runtime death = remount click.
Cannot fully skip the first allow. Reduce it: persistent Colab runtime, same account, Apps Script later (WQ-045). Do not drop a service-account JSON in the notebook.

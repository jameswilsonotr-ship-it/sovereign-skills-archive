# ODA-WQ-042 — TUI engine as an Alpha **sub-skill** (not "subtextual")
Status: **OPEN / PARKED — PATHS DRAFTED** 2026-09-11 03:51 EDT
Owner: olivia-dev-alpha
Priority: design. Do not implement this bounce.
Claim: Absolute Liv HUB

Voice-to-text correction 03:51 EDT: she said **sub-skill**, not subtextual / subscure.

## What she wants
One consistent engine that looks like the TUI already designed (config, ASCII, C-64 / demo-scene chrome, CSS panes), runs in the sandbox AND in Colab, drives any script / emit / outcome, and is also an observability / metrics / debug layer plus a menu. Sub-skill so it does not blow the context window.

## Already exists
- Drive `textual_main_app_schema.py` 10fp6DiZzAXkBiXzzzae44BDAjXxKZcUV (2026-06-22)
- Vesper tui.py 11Ki9gb8sNTvc0KvI7K2z1ZNCtNIA0BJY (2026-08-17)
- Vesper spec 30 + spec 12
- format-bible tui.md / tui-visual.md
- Alpha lab_tui.py stdlib twin
- ASCII-R vendor + image-pipeline work-queue-ascii-r

## Four paths
A stdlib view + JSON jobs
B Textual app from the June schema + textual-serve
C job registry (scripts as data)
D Colab-native Rich panes

Recommendation: C is the engine. A is the default view. B is the pretty view when a tty exists. D is the Colab shim.

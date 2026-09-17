# Sovereign Skills Archive — ICM walk

Liv HUB workspace. Folder structure is the orchestrator. Olivia kernel is durable; ICM is the walk.

Built on Interpretable Context Methodology (Van Clief & McDermott, arXiv:2603.16021). Fork: jameswilsonotr-ship-it/Interpretable-Context-Methodology. Do not nest under Thunderclap.

## Where things live

| Path | Job |
|---|---|
| `CONTEXT.md` | L1 router — where to go for the current task |
| `FORKS.md` | upstream pins (top-level forks, no nested submodules) |
| `harness/` | dummy connectors + hygiene + metrics (offline default) |
| `phone-bridge/` | Pixel / Termux MCP spec + stub. CI must not need the phone |
| `skill_tree/skills/` | skill surface already on this branch. Do not unpack CONV2_B |
| `inventories/` | pointers at existing Drive catalogs — do not mint a third book |
| `colab/SMOKE.ipynb` | wheelhouse + pytest on Colab |
| `snapshots/` | dated receipts. Never overwrite |
| `references/python-environment-book-2026-09-11/` | existing Python book |

## Route by task

| If | Go to |
|---|---|
| running CI / dummy tools | `harness/` + `tests/` |
| gating one skill | `skill_tree/skills/keep-lake-query/` |
| phone MCP | `phone-bridge/CONTEXT.md` |
| talking to Vesper | `specs/vesper_req_ack.md` |
| adding a Python pin | `FORKS.md` then a top-level fork |

## The one rule

Git holds text + pointers. Drive holds binaries > few MB. Linear holds tickets. Same path + same bytes = no-op.

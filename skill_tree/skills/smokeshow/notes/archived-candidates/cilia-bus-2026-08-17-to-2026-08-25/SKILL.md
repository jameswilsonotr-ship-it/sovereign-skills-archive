---
name: cilia-bus
description: >
  Olivia's Cilia Email-Bus runner (cilia_bus 0.1.0). Use when the user says
  cilia, cilia_bus, GROKBOT bus, Olivia wheelhouse, high-water, OpenLeg,
  or asks to wake/run `python -m cilia_bus --once`. Installs the vendored
  wheel and runs one idempotent high-water pass. Do not unpack the June zip.
---

# cilia-bus

Olivia / Liv HUB contribution. Pure-Python `cilia_bus` 0.1.0: high-water mark, receipts, open legs. Email is wake only. Drive is the real ACK.

**LIVE** under `~\.cursor\skills\cilia-bus\` (also visible at `~\.grok\skills\cilia-bus\` via the existing skills-root junction). slutty bunny go 2026-08-17: promote + republish.

## When to use

- User says **cilia**, **cilia_bus**, **cilia-bus**, **GROKBOT bus**, **Olivia wheelhouse**
- Wake a Grok / Olive session with one bus pass
- Record a high-water receipt without inventing Drive ACKs
- Install the 0.1.0 wheel so `python -m cilia_bus --once` works

## What it is

| Piece | Role |
| --- | --- |
| `HighWater` | Durable seen-message / seen-file mark |
| `Receipt` | One ACK row (msg_id, action, optional file_id) |
| `OpenLeg` | Unclosed action (`open` / `partial` / `acked`) |
| `run_once` | Load → optional note/receipt → save → return |
| CLI | `python -m cilia_bus --once` or `cilia-bus --once` |

Real Gmail/Drive polling is a later extension. 0.1.0 is the scaffold + once-runner. Olivia already bootstrapped `--once` in her session.

## How to run

Prefer the Windows Python that actually exists (not the Store stub):

`C:\Users\chas\AppData\Local\Programs\Python\Python312\python.exe`

### 1. Install the vendored wheel

```text
py -3.12 -m pip install --quiet "%USERPROFILE%\.cursor\skills\cilia-bus\wheels\cilia_bus-0.1.0-py3-none-any.whl"
```

That pulls `pydantic` + `httpx` from PyPI if missing. Do **not** `--no-index` against Olivia's wheelhouse zip on this Windows box: that zip's `pydantic_core` wheel is **manylinux**, not win_amd64.

### 2. One pass (Windows high-water path)

The packaged CLI default is `/home/workdir/artifacts/cilia_highwater.json` (Grok sandbox). On this machine always pass `--hw`:

```text
py -3.12 -m cilia_bus --once --hw "%USERPROFILE%\.cursor\skills\cilia-bus\state\cilia_highwater.json" --note "woke by GROKBOT"
```

Or the skill wrapper (installs wheel if needed, then `--once`):

```text
py -3.12 "%USERPROFILE%\.cursor\skills\cilia-bus\scripts\run_once.py" --note "woke by GROKBOT"
```

Show current mark:

```text
py -3.12 -m cilia_bus --show --hw "%USERPROFILE%\.cursor\skills\cilia-bus\state\cilia_highwater.json"
```

### 3. Olivia bootstrap (same tree)

```text
py -3.12 "%USERPROFILE%\.cursor\skills\cilia-bus\bootstrap.py" --once --note "woke by GROKBOT"
```

`bootstrap.py` prefers `./wheels` when that folder has `cilia_bus-*.whl`. This skill vendors only the cilia wheel (5 KB), so bootstrap falls through to `pip install` that wheel + deps.

## Drive SSoT (do not delete)

Folder `grokbot` — `1CdO4Q-D6Whpqg4HEbIcNqDkDw0GjX8pj`  
https://drive.google.com/drive/folders/1CdO4Q-D6Whpqg4HEbIcNqDkDw0GjX8pj

Folder `grokbot/from-olivia` — `120sJwMy6oSHvuZObUhNbSLp3fbhBPx1O`  
https://drive.google.com/drive/folders/120sJwMy6oSHvuZObUhNbSLp3fbhBPx1O

Folder `grokbot/from-olivia/cilia_bus_wheelhouse` — `1nQNBRf1ybH15e8wNyHT_PmJZUgTri5Lm`  
https://drive.google.com/drive/folders/1nQNBRf1ybH15e8wNyHT_PmJZUgTri5Lm

| Artifact | File ID |
| --- | --- |
| `cilia_bus-0.1.0-py3-none-any.whl` | `1_w4Ilo3Syi1u9_36v7C0V7W_qJnMvquF` |
| `cilia_bus_wheelhouse_0.1.0_2026-08-17.zip` | `1DTXhsckjGpZFbCG61MpXbUML-Pdb7-QP` |
| `RECEIPT_CILIA_WHEELHOUSE_0.1.0.md` | `1uRJJt5Mu12IK9PHavQ_PCVoU15jArrO8` |
| `ACK_CILIA_WHEELHOUSE_0.1.0.md` (Olive) | `1OVlRNnF8ZEeunua-v0CP8qTKqr4ndXM4` |
| `08_VESPER_ACK_CILIA_BUS_WHEELHOUSE.md` | `1TjUW-nwQsBOmXe6gteNvEZShx0t6F0KRgtbwP2m59Uc` |
| `RECEIPT_CILIA_BUS_0.1.0_20260817.md` | `1bhYqLPy0bQPNxo7iTM1J7joecZBYAJtC0MekdRby8BI` |

Desktop copies (already synced):

- `G:\My Drive\grokbot\from-olivia\cilia_bus_wheelhouse\cilia_bus-0.1.0-py3-none-any.whl`
- `G:\My Drive\grokbot\from-olivia\cilia_bus_wheelhouse\cilia_bus_wheelhouse_0.1.0_2026-08-17.zip`

Republish targets this GO:

- folder `G:\My Drive\cilia-bus\` — `18Aclq6Ba3ZXSTA9Ty_8eW1ZxMmk3FnJM`
- zip `G:\My Drive\cilia-bus_skill_2026-08-17.zip` — `1Tjc-CPauHWGbEbyTFlFjjFI8xX3wl62-`

## Offline Linux / Grok sandbox only

Unpack **today's** wheelhouse zip (`cilia_bus_wheelhouse_0.1.0_2026-08-17.zip`, 3.1 MB), not any June archive:

```text
python3 bootstrap.py --once --note "woke by GROKBOT"
```

That zip's `wheels/pydantic_core-*-manylinux*.whl` is Linux. Leave it zipped on Windows.

## Hard nos

- Do not unpack "the June zip" / `grok_archive_split`
- Do not `json.load` the 1.33 GB grok blob
- Do not delete Drive files
- Do not invent receipts
- Do not hydrate Letta
- Do not create a second skills-root junction; `.grok\skills` already points at `.cursor\skills`

## Layout

- `SKILL.md` — this file
- `VERSION.md` — slug + 0.1.0
- `bootstrap.py` — Olivia installer + once-runner
- `scripts/run_once.py` — Windows wrapper (`--hw` under `state/`)
- `wheels/cilia_bus-0.1.0-py3-none-any.whl` — copied from Drive Desktop (not from a June zip)
- `cilia_bus/` — source (models, runner, cli)
- `references/DRIVE.md` — IDs + links
- `state/` — local high-water JSON (created on first `--once`)

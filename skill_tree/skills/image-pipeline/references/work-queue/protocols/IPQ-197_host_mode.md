# IPQ-197 — Host mode + Garage Expert speak-line

**Status:** LIVE 2026-09-11
**Claim:** Absolute Liv HUB

## Detect

| signal | meaning |
|---|---|
| `google_drive_upload_artifact` in catalog | can flush |
| `conversation_search` in catalog | full Expert tape |
| chat-room / inter-agent pane | looks like Heavy, upload is usually gone |

Python cannot see the catalog. The agent sets `--has-upload` / `--has-tape` on `scripts/host_mode.py`.

## Speak line (mandatory when can_flush is false)

> Turn me on to Garage Expert so I can upload.

Do not bury the miss inside a protocol paragraph. Say the line.

## Buffer

Chat-room panes still `keep_path`. They write `artifacts/upload-buffer/QUEUE.json` via `scripts/upload_buffer.py --write-queue`. Garage Expert flushes that queue, marks, gates.

`--gate` exit 2 is correct until ids land. Talking “pushed” after exit 2 is a protocol fail.

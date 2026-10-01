# Lake Swim — Search Strategy

Frozen 2026-09-12. These are the actual tool calls used, not a cleaned theory.

Connector: `google_drive_search`, `google_drive_list_folder`, `google_drive_read_file`, `google_drive_download_artifact`, `google_drive_create_folder`, `google_drive_upload_artifact`.

Dated-tree root (voice-readable SSoT): `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`  
Walk: `YYYY / MM / weekNN / YYYY-MM-DD / YYYY-MM-DD_<8hex>.md`

## What failed

`google_drive_search` with `created_after` + `created_before` + keyword on lake `.md` files usually returns **empty**. Those files are native markdown. The connector does full-text on Google Docs/Sheets/Slides and **title-only** on everything else. So "Olivia" inside a `.md` body does not hit.

`created_after` also misses harvest twins whose *create* date is later than the conversation date. Use `modified_after` if you want the 2026-06-18 tree stamp, or ignore dates and walk folders.

`folder_name: full_replica` + keyword returned empty this session.

Web search and X search are noise. Do not use them for lake months.

## Recipe A — tree walk (October text, the one that worked)

1. `google_drive_list_folder` folder_id=`1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` → years 2025, 2026
2. list `1XVLJszOOGzxhTmFnzUfg3YIW1YI0m424` (2025) → months `10`, `11`, `12`
3. list month folder → weekNN folders
4. list each week → day folders
5. list each day → `YYYY-MM-DD_<8hex>.md` files with size + id
6. `google_drive_read_file` start_line=1 end_line=20~25 max_chars=800~1500 on a sample per day for the title line
7. Download unique hexes under ~400 KB. Pointer-only if >1 MB.

October month folder: `1FBy2tfnAPFlp48WSGaGkkl7PrUyrksOR`  
October weeks: week41 `1DtrppE-a_ohmZZniW9aqU6yzJZwEQWhF`, week42 `1c-jrAV7IRaNx-eEepbIS2R231NXTMIT4`, week43 `1rPwR6H9Azeys7ioqRPTkMTjz4QtHL1zY`, week44 `1X3UaAE52riCatD0laVG565lYqdZGW4vz`

## Recipe B — keyword + date box (November voice, leaky)

These were the exact queries:

| query | created_after | created_before | max_results | what it actually returned |
|---|---|---|---:|---|
| Olivia | 2025-11-01T00:00:00Z | 2025-12-01T00:00:00Z | 30 | Eve/Valerie lock files + Nov 26/28 timestamp notes. Not the dated tree. |
| road dog | same | same | 20 | Frankenbride summaries, Bluetooth docs, takeout zip, divorce doc. Mixed. |
| shotgun | same | same | 20 | guardrails json, Valerie versions, Eve.txt, clipboard. False friends. |
| persona | same | same | 20 | Eve early stages, Valerie v1–v3, Grok traits, Operational Chemistry. Best of the four. |
| Olivia | folder_name=full_replica | — | 20 | empty |
| exact_name=2025-11-November | mime=folder | — | 10 | empty (packet did not exist yet) |

Then `google_drive_list_folder` on November month `1Oh5slZyfecavCKwysRHcUkujsQRdTObc` → weeks 44–48. Only week44 days were listed on the voice pass (2025-11-01, 2025-11-02). That is why voice November is thin in the middle.

Files actually `read_file`'d on the voice pass:
- `1V8ekrzLp0F_gZCLlaRkHdAms6_JYNnQP` eve Olivia root.txt
- `1t4Xqn6jCvH3XDNKrmUjZzV8ipdO7QwnLXAxuZrPWdJs` Operational Chemistry
- `1aLDThfxDSH31AdeDgxyAdU6qF5WLOtnx` Valerie v3.0
- `1uD7PAlCDAxMZXS3vgmeLPTgKCU5w7BFI` Persona Development.md
- `1gnoC-ZvqO4batQBEha0n1V_yhquGmZF3` Eve early stages
- `1e2If6o-u7jYbcMq4IJgDjHi0WTe4d5QG` Frankenbride Summary.md
- `1UzF5VeY9qOPwRgvdTCclIX8l5pRB0JNf` Eve.txt

## Recipe C — October first attempts that wasted turns

- query=`Olivia` created_after=2025-10-01 created_before=2025-11-01 → female_names.txt junk or empty
- query=`Olivia OR Liv OR Eve` week-sliced Oct 1–8, 8–15, 15–22, 22–31 with include_content=true → empty
- title_only variants → empty
- Those are why October only got honest once the tree walk started.

## Limits that matter

- list_folder max_results 50 (default). November day folders can exceed that on Halloween-style days. Raise to 200 if a day looks short.
- read_file first 25 lines is enough for the `# Title` line. Do not slurp 1.6 MB into voice.
- download + upload the unique hex once. Same hex on two days is one thread.

## Packet write pattern

1. Create `Monthly Lake Swimming / YYYY-MM Month` under `1YIaUMUmr-YNQXJT4p78FyL-yMWRukswI`
2. Write `00_SOURCE_LEDGER.md` (every file id) + `01_TOPIC_BRIEF.md` (topics, not biography)
3. Copy sources under ~400 KB into the packet
4. Pointer-only over 1 MB
5. Update parent README

Do not write trailer numbers or load state into memory.md. This packet is the swim, not identity.

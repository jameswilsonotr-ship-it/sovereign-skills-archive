# Session handoff — 2026-09-11 04:38 EDT

Claim: Absolute Liv HUB. No mint. Ignore Valerie.

## What this turn did

Heavy pass requested: FB/IG/TT/local-video/music-video libs + stubs, 169/173/174, finish 170, explain blockers + 193, full WQ 001-current, grouped remaining, deterministic smoke.

Most of that already existed from 04:32. This turn:

1. Confirmed stubs + vendor on disk.
2. Ran `smoke_harness.py` — 10/10 green (compile/help/fork/resolve/169/173/168/heat/still/gate).
3. keep_path dummy `smoke-ipwq170-gate_20260911-043238` → `--gate` exit 2 (queued). Honest.
4. Tried `google_drive_upload_artifact` — **not in this host catalog**. 170 cannot get `--gate` 0 here.
5. **193 FIRED at 08:34 UTC / 04:34 EDT.** Host rolled scripts back to 04:16. Ingest stubs, vendor, smoke, android_show, imply_fallback vanished mid-command.
6. Reseated from `artifacts/IP_FEED_STUBS_169_173_174_20260911-0432.zip`. Re-piped vendor (gallery-dl 1.32.11 + instaloader 4.15.3). Re-patched RENDER_ROUTE_LOCK §4 + ANDROID_SHOW_PATH §7 + RUNBOOK show ladder.
7. Expanded `smoke_harness.py` with `ingest` / `local` / `gate`.
8. Local 3s testsrc → inbound + FOREPLAY, promote=false.
9. FB/IG/TT dummy URLs → INGEST.json, cookie-or-403, promote=false, rc 0.
10. MV `hot n cold` → kTHNpusq654, source_kind yt-failed (yt-dlp +x / 403), no mint.

## 193 — what “this host deletes files” means

Not a missing script. Not a git wipe you ran.

This sandbox skill tree is not durable across turns. Earlier tonight restored `.py` files disappeared between ~03:35 and 03:43. At 04:34 this turn, `scripts/fb_ingest.py` et al. returned `[Errno 2]` seconds after they had been listed and compiled. The tree rolled to a prior snapshot.

Durable copies:

- `artifacts/IP_FEED_STUBS_169_173_174_20260911-0432.zip`
- `artifacts/vesper-hints/` bags
- Drive `06_CROSS_SKILL_AUDIT` `12uZAQB0LfbqmvnP2C6dKqrh7rVHCwz6R` (when upload tool exists)
- Drive source packs `19fSVhj5nEx2NfBnjydFR-CgQLUq_HYVR` / master `1KI7t0QqKy3K2mxJfdRWmoHGErDHihosx`

Next thread: if `scripts/fb_ingest.py` is gone, unzip the 04:32 bag first. Do not reconstruct from prose.

## 001–160

Not files on this tree. Live queue starts at **IP-WQ-161**. Historical IPQ / olivia-dev / agentify RUNBOOK debt. Do not archaeological-dig unless a path citation appears.

## Ticket status after this turn

| id | status | note |
|---|---|---|
| 161 | TESTED | 3s testsrc → frames + FOREPLAY |
| 162 | PARTIAL / TESTED | router + fail-closed stubs. Live bytes need cookies |
| 163–166 | OPEN | identity / veto / talking-head / grid scrape |
| 167 | DONE | emit spine restored |
| 168 | TESTED | identify+media / bare |
| 169 | TESTED policy | android_show.py. Phone carousel unproven |
| 170 | PARTIAL | keep + gate-fail-closed tested. Upload tool missing on this host |
| 171 | PARKED | copper/amber. no mint |
| 172 | OPEN | KEEP_INDEX Drive twin |
| 173 | TESTED picker | imply_fallback. no live moderate hop |
| 174 | TESTED / PARTIAL | MV inbound + research cards. YT bytes 403 |
| 175 / 179 | TESTED | url_resolver known-table + dirty ?is= |
| 176 / 177 | DONE | phrase.schema + CHARACTER persona fields |
| 178, 180–190 | OPEN | MV depth |
| 191 / 192 / 195 | DONE | PROTOCOL_ENGINES, factory nine, IPQ-078 |
| 193 | WATCH / FIRED 04:34 | reseated |
| 194 | TESTED | URL throws |
| 196 | TESTED | smoke_harness. also ` --only local` and ` --only gate` |

## Blockers left (honest)

1. **193 churn** — skill tree can eat restored py mid-session. Bags are the copy.
2. **Drive flush tool missing** — `google_drive_upload_artifact` not in connected-tools catalog this pane. `--gate` stays 2. Do not claim Drive-saved.
3. **Cookies not in tree** — FB/IG/TT/YT live bytes fail closed. Never git cookies.
4. **YT SABR / 403** — official thumbs only. No fake frames.
5. **yt-dlp execute bit** — binary at `artifacts/bin/yt-dlp`; `/tmp/yt-dlp` symlink must stay +x.
6. **165** — grok-build talking-head scripts empty on purpose.
7. **169 phone proof** — policy JSON green. ANDROID carousel not proven this pane.
8. **187** — anti-mint flag set on MV ingest, not enforced in generate.

## How to smoke next thread

```
python3 /home/workdir/.grok/skills/image-pipeline/scripts/smoke_harness.py --only compile,help,fork,resolve,169,173,168,heat,still,gate
python3 /home/workdir/.grok/skills/image-pipeline/scripts/smoke_harness.py --only local
```

Skip `--only ingest` unless you can wait ~90s (gallery-dl 40s/platform).

## Do not replay

167 restore, factory-nine hunt, velvet June/July hunt, vendor pip if vendor/gallery_dl exists, 001–160 archaeology, Valerie.

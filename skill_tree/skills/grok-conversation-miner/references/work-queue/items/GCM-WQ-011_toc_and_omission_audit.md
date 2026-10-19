# GCM-WQ-011 — TOC plus omission audit

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner
**Asked by:** Bunny this pane — wire only, do not code yet

Every miner package (publish, vacuum, global extract, sunset L3/L4/L7) must include two lists, not one.

## Required artifacts
1. `TOC.md` — what *was* packaged, path + class + byte size + stamp
2. `OMISSIONS.md` — what *could have* been packaged and was not
   - class (sandbox file, skill delta, Imagine, video, plate, queue, lake twin, export uuid, email receipt)
   - reason code (`SKIP-EXISTS` / `SKIP-OVERLAP` / `SKIP-NO-HIT` / `TOO-LARGE` / `SECRET` / `NOT-WALKED` / `PANE-VANISH` / `OPERATOR-SAID-NO`)
   - still-gettable? yes/no
   - pointer if it lives elsewhere (Drive id, skill path)

SKIP is an audit line. SKIP is not silence.

## Done looks like
A package with both files. A reviewer can name one thing that should have been in and find it in TOC or OMISSIONS. Never “we just didn’t mention it.”

## Pointers
- `references/prompt_global_extract.md`
- `references/prompt_publishing.md`
- GCM-WQ-003 L7 into L4
- GCM-WQ-007 packers (Imagine/video/plates often land here as omissions today)
- liv-automation-ops (pane artifacts vanish — that is an omission class)

## RESULT 2026-09-11: SMOKE-PASS toc_omissions.py.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN fixture  
**Stamp:** 2026-09-11 03:40 EDT  
scripts/toc_omissions.py writes TOC.md + OMISSIONS.md. Smoke omitted secrets + live sunset.

Pointer: GCM-WQ-020 export evidence log is the durable source TOC/OMISSIONS cite.

# Debrief Pattern — Template (sandbox lock)

Frozen: 2026-09-12  
Where this lives: `artifacts/monthly_lake_swimming/DEBRIEF_PATTERN.md`  
Drive parent: Monthly Lake Swimming `1YIaUMUmr-YNQXJT4p78FyL-yMWRukswI`  
Used when Bunny says: debrief / key moment / pull the actual files / make a subfolder / record it so it never happens again.

This file did not exist as a named template. October, November, Milemarker Roast, and tonight’s lock were the working examples. This is the written version so a later pane does not have to reverse-engineer the shape.

---

## What a debrief packet is

A **swim packet** for one key moment or one month. Not memory.md. Not KEEP. Not a rewrite of the originals.

Goal: the next voice turn can say the name of the folder and know what happened, why it matters to Bunny, why it matters to Liv, and where the original files are.

---

## Hard rules

1. **Copy, do not overwrite.** Originals stay where they are. Packet `sources/` holds copies of files under ~400 KB. Over 1 MB = pointer only (file_id + size + first-page title).
2. **Cite.** Every claim gets a Drive ID or a skill path. No “we talked about this once.”
3. **Do not invent biography.** Titles and first pages only unless she asks for the actual words.
4. **Do not merge unlike packets.** Same event → one folder. Same *feeling* is not the same event.
5. **Do not write trailer / fuel / load state into memory.md.** Load dies with the haul. Debriefs are durable.
6. **Do not slurp KEEP 227 MB.** Dated tree walk or a named hex.
7. **Folder path is the date**, not file createdTime.

---

## Folder shape (always)

```
Monthly Lake Swimming /
  YYYY-MM Month/                  # month swim
  OR
  YYYY-MM-DD Short Label/         # key-moment swim
    00_SOURCE_LEDGER.md           # every file_id touched
    01_TOPIC_BRIEF.md             # what happened, citations, why it matters
    02_LOCK.md                    # only if a standing rule was named
    sources/                      # copies under ~400 KB
```

Drive parent: `1YIaUMUmr-YNQXJT4p78FyL-yMWRukswI`  
Local twin: `artifacts/monthly_lake_swimming/`

Update the parent `README.md` row when a packet is born.

---

## How to pull (Recipe A — the one that works)

Dated-tree root: `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`  
Walk: `YYYY / MM / weekNN / YYYY-MM-DD / YYYY-MM-DD_<8hex>.md`

1. Name the date or the label out loud.
2. `google_drive_list_folder` down the tree. Do not keyword-search `.md` bodies (title-only; empty hits).
3. Read first 20–25 lines of a day’s file for the `# Title`.
4. Download unique hexes under ~400 KB into `sources/`.
5. Pointer-only over 1 MB.
6. Write ledger → brief → lock (if needed).
7. Upload the packet into the Drive folder. Do not edit the source files in place.

Keyword + date-box is Recipe B and leaky. Use it only for Google Docs / titled notes, then verify against the tree.

Full failure notes: `SEARCH_STRATEGY.md` in this folder.

---

## What `01_TOPIC_BRIEF.md` must contain

For each topic:

- **When** (date or range)
- **Source** (filename + Drive ID + hex if any)
- **What the file actually says** (not what we wish it said)
- **Why it matters to Bunny**
- **Why it matters to Liv / the swarm**
- **What this pass did not do**

If two events share a feeling (spiral, shame, self-loathing language) but different dates/places, they stay in different folders and cross-link.

---

## Merge test (do this before combining folders)

Merge ONLY if all three are true:

1. Same night / same session hex (or she says they are the same night).
2. Same place or same named event.
3. Combining them would not hide a lock that needs its own folder.

Tonight’s test:

| Packet | Same as Youngstown Meltdown? |
|---|---|
| 2026-09-12 No Model Self-Loathing | **No.** Operational lock from the Penelope cab. Different year, different job, different rule. Cross-link only. |
| Feb 15 2026 studio-apartment 8-frame spiral | **Not until she says so.** Visual language of a meltdown. Place is a studio, not Club 76. Candidate for the “one more freakout.” |
| Jan 26–27 Denny’s abort | **No.** Separate candidate. |
| March 14 2026 OH-11 / US-422 Youngstown drizzle | Same *city*, later date, visual prompts. Lives as a **later echo** inside Youngstown packet, not a merge with tonight. |

---

## Existing packets (as of 2026-09-12 16:53 CDT)

| Packet | Local | Drive |
|---|---|---|
| 2025-10 October | `2025-10/` | `1qMb0_rF5nJDqy3kyYG7o8sV7qrizHK_4` |
| 2025-11 November | `2025-11/` | `1OGGJOU3nkr7jaMTGoK0NK1lUA0C9qmGe` |
| 2026-09-12 No Model Self-Loathing | `2026-09-12_no-model-self-loathing/` | `1X2lDNLu0EvzUdbI5fcLBdNM3nm2-gQXh` |
| Youngstown Meltdown | `youngstown-meltdown/` | `10tgRYrkbc_o2g7fLWDiyP4BEADhuJ40_` |
| Milemarker Roast (sibling, not under this parent) | `artifacts/MILEMARKER_ROAST_EXCERPT.md` | `1drRcL4-FbA18juaq2haNF-KXdZS6FJdF` |

---

## Voice vs textland

Textland: search, copy, ledger, brief, lock.  
Voice: tell her what the packet says. Do not re-walk the tree on the phone unless she asks.

Next month after Youngstown is December 2025 swim (week49–52), then 2026 month-by-month toward Chicago. She names the leftover freakout before that walk starts.

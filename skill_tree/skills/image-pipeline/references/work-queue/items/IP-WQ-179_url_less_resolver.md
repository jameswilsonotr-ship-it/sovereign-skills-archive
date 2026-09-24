# IP-WQ-179 — URL-less / dirty-link resolver

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-175 · IP-WQ-162  
**Tests:** `kTHNpusq654?is=...` and title “hot n cold katy perry”

## Idea

Title-only, lyric fragment, broken share, spoken “that hot n cold video” are first-class inbound. Not a courtesy when the paste is clean.

## Reasoning

Voice-first cab will not hand `youtube.com/watch?v=`. Bunny’s actual paste was `youtu.be/kTHNpusq654?is=aPv7oNXt9IiwGUf2`. `is` is a typo for `si`. A resolver that requires a clean watch URL will miss the most common real input.

Without a resolver we either refuse the job or hallucinate an ID. Both are worse than a ranked search with rejected candidates written down.

## Ladder (fetch only — does not scrape, does not plate)

1. Extract 11-char ID even from garbage query params / trailing commas.
2. Normalize title: strip official / remastered / HD / Vevo / lyric video / audio / brackets.
3. `yt-dlp ytsearch5:ARTIST TITLE official music video`. Rank official artist channel, then Vevo/label, then “Official Music Video” in title, then duration ±15% if known.
4. Lyric fragment → lrclib / syncedlyrics / Genius plain → title+artist guess → step 3. Ambiguous fragment waits for a human pick.
5. Hard fail: no invented URL. Research still-set path (IP-WQ-181).

Write into FOREPLAY (see IP-WQ-186): resolved url, id, confidence, rejected[].

## Exit

A function or CLI `agentify resolve QUERY` returns a card. Dirty Hot N Cold share resolves to `kTHNpusq654`. Title-only “hot n cold katy perry official” prefers the Katy Perry channel upload. No plates.

# IP-WQ-186 — FOREPLAY resolve audit fields

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-179 · FOREPLAY.json from reel-analyze

## Idea

When we resolve a dirty string to a tape, write the decision down. Confidence, rejected IDs, bytes vs thumbs.

## Reasoning

Wrong-tape risk is real. “Hot n Cold” hits covers, FIFA 09 uses, lives, lyric videos. If FOREPLAY only stores the winner we cannot audit a bad pick next week.

Dirty `?is=` share is the first unit test: input string ≠ clean watch URL, output id = `kTHNpusq654`.

## Fields to add on FOREPLAY.json

```json
{
  "kind": "music-video",
  "query_raw": "https://youtu.be/kTHNpusq654?is=aPv7oNXt9IiwGUf2",
  "resolved": {
    "id": "kTHNpusq654",
    "url": "https://www.youtube.com/watch?v=kTHNpusq654",
    "title": "Katy Perry - Hot N Cold (Official Music Video)",
    "channel": "Katy Perry",
    "duration_s": 283,
    "confidence": "id-extract|search-official|search-weak|human-pick"
  },
  "rejected": [{"id": "", "why": "lyric video|cover|live|duration"}],
  "bytes": false,
  "captions": true,
  "mint": false
}
```

## Exit

Schema note or FOREPLAY example in 182 inbound. Resolver writes these keys. Smoke of the dirty share shows `confidence=id-extract`.

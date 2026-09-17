# IP-WQ-180 — captions-first lyric alignment

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-174 · IP-WQ-176

## Idea

Get timed words *before* we insist on video bytes. Align BEAT.t to caption start times. Whisper is the fallback, not the door.

## Reasoning

Official Hot N Cold already ships a transcript on the watch page (church-bell cold-open, spoken vows, then sung lines). If SABR eats googlevideo we can still build PHRASE + section map tonight.

WhisperX / Demucs / vocal-sep are steel. Captions are a 20-line Python wrapper. Cab priority is captions → LRC → ASR last.

Spoken vs sung matters on this tape. “Katy, do you take Alexander” is cold-open dialogue, not a chorus beat. Mark caption rows `speech` | `sung` | `sfx` so the vows do not become phrase 1.

## Work

Order:
1. `youtube-transcript-api` on the resolved ID
2. else `yt-dlp --write-auto-sub --skip-download --sub-lang en`
3. else `syncedlyrics` / lrclib by title+artist+duration
4. else faster-whisper on extracted audio if we actually have audio

Write `LYRICS.json` on the inbound dir: `{t, dur, text, kind}`. Phrase builder consumes sung chorus rows.

## Exit

Hot N Cold captions land as LYRICS.json without requiring the mp4. Chorus lines are tagged sung. Vows tagged speech. No plates.

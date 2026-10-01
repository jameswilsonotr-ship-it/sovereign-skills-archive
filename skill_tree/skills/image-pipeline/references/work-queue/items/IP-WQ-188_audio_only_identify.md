# IP-WQ-188 — audio-only identify path

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-179 · IP-WQ-161

## Idea

She hands an mp3, a radio rip, or cab audio. We identify the recording, then join the music-video fork. We do not invent a face from sound.

## Reasoning

URL-less is not only titles. OTR she will have the song and not the clip. Chromaprint + AcoustID / MusicBrainz gets title+artist+duration. Then the 179 search ladder looks for the official video.

If no official video exists (audio-only single), stop at a lyrics+persona card. Research still-set only if public stills exist. Never generate a bride because the song is Hot N Cold and we “know how it looks” without a SOURCE still.

This is later than captions-first. Do not block 182 on AcoustID.

## Work

Optional extra: `chromaprint-tools` + pyacoustid when audio bytes exist and there is no video ID. Write `recording={title,artist,duration,mbid}` into FOREPLAY, then call resolve.

## Exit

Documented as optional step 5 of the 179 ladder. No pip required for the Hot N Cold URL smoke. No face from an mp3.

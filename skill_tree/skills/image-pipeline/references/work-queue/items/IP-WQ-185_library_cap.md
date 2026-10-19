# IP-WQ-185 — library cap / anti-bloat

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 23:04 MDT  
**Claim:** Absolute Liv HUB  
**Parent:** IP-WQ-175

## Idea

A written allow-list and refuse-list so “research Python libraries” does not become a second media stack in the cab.

## Reasoning

The bunker already speaks ffmpeg, yt-dlp cookies, Pillow, keep_path. Night-one MV analysis needs captions + cuts + optional tempo. It does not need corpus-mill, Qwen-VL 7B, pyannote, or insightface.

Insightface especially fights cousin-first / IP-WQ-163. If we embed Katy’s face to “keep identity” we will try to make plate A an edit of the inbound jpeg. That is the law we just spent a month writing down.

Whisper is fallback ASR when captions and LRC both miss. Official Hot N Cold does not need it.

## Allow (night one)

ffmpeg, ffprobe, yt-dlp, Pillow, imagehash, youtube-transcript-api, syncedlyrics/lrclib, scenedetect, librosa, numpy.

## Later / optional / Jetson

mediapipe pose, ultralytics person-count, faster-whisper.

## Refuse as dependencies of agentify

corpus-mill, Qwen-VL, pyannote, Demucs, WhisperX, insightface / face_recognition as plate conditioner, paid Genius/Musixmatch keys, Shazam SDK, any “the song is the agent” generator.

## Exit

This allow/refuse copied into agentify module README or COVERAGE-adjacent note. No surprise pip in the smoke.

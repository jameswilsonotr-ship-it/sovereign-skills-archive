# IP-WQ-162 — feed fork

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10

## Goal
YouTube Short, YouTube community post, Facebook still, Instagram still/reel, raw still upload, raw video upload all land on one scrape after fetch.

## Fork

| inbound | fetch | then |
|---|---|---|
| YT short URL | yt-dlp-sabr + socks (IP-WQ-149) | reel |
| YT post URL | thumbs + OCR + artist research | still set |
| FB / IG URL | later; cookies not in tree | still or reel |
| raw still | copy to inbound | still |
| raw video | IP-WQ-161 | reel |
| music-video URL | IP-WQ-174 — yt-dlp + captions; 403 → thumbs | reel + lyric align |
| title / lyric / dirty share (no clean URL) | IP-WQ-175 resolve ladder, then 174 | same after resolve |

Platform is fetch only. Scrape + plates do not change.

Music-video + title-only details: `items/IP-WQ-174_music_video_inbound.md`, research: `items/IP-WQ-175_music_video_research.md`.

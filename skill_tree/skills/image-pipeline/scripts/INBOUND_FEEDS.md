# Inbound feeds

Platform is fetch. Scrape + plates do not change. Frames/stills = SOURCE. Never plate A. No mint.

| kind | script | library |
|---|---|---|
| YouTube Short | yt_short_ingest.py | artifacts/bin/yt-dlp + official thumbs |
| YouTube community | community_post_fetch.py | innertube / invidious / yt-dlp |
| YouTube / Vevo music-video | music_video_ingest.py | yt-dlp + thumbs; section stub |
| Facebook | fb_ingest.py | vendor/gallery-dl + yt-dlp (cookies) |
| Instagram | ig_ingest.py | vendor/instaloader + gallery-dl |
| TikTok | tiktok_ingest.py | yt-dlp + gallery-dl spare |
| local video | local_video_ingest.py | ffmpeg + reel_sample.py |
| local still | feed_fork.py | copy |

Router: `python3 scripts/feed_fork.py URL_OR_FILE`

Vendor: `scripts/vendor/` (gallery-dl 1.32.11, instaloader 4.15.3, requests). Binary: `artifacts/bin/yt-dlp` (symlink `/tmp/yt-dlp` when seated).

Cookies (optional, never git, never Drive): `artifacts/secrets/{youtube,ig,fb,tt}-cookies.txt`.

Smoke: `python3 scripts/smoke_harness.py`

Fail closed: INGEST.json always. promote=false. No plates from inbound bytes.

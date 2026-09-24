# image-pipeline / scripts

Emit spine: `keep_path.py` → `step6_drive_flush.py` → `flush_drive_queue.py`

Agentify: `agentify.py`

Inbound four-plate factory (PROTOCOL.md). Reconstructed 2026-09-11 after Drive exact-name miss:

- inbound_classify.py
- segment_grid.py
- inbound_queue.py
- split_plan.py
- emit_intent.py
- scaleback_loop.py
- isolate_person.py
- hub_review.py
- smoke_split_engine.py
- engine_hook.py

Reels / shorts: reel_sample.py reel_analyze.py reel_menu.py yt_short_ingest.py community_post_fetch.py

Echo: echo_interface.py

Feed fork (IP-WQ-162): feed_fork.py → fb_ingest.py ig_ingest.py tiktok_ingest.py local_video_ingest.py music_video_ingest.py url_resolver.py

Policy: android_show.py (169)  imply_fallback.py (173)  contact_sheet.py (170)

Vendor (local, not global pip): scripts/vendor/{gallery_dl,instaloader,requests,urllib3,certifi,idna,charset_normalizer}

Smoke: python3 scripts/smoke_harness.py

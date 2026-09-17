# IP-WQ-169 — four ways to get a carousel off this phone

Research pass 2026-09-11. Client fact unchanged: `App Name: ANDROID`. Shots 133235 / 133236 still prove `render_file` and Imagine component tags serialize as brown prose on the default Android Expert bubble.

Public UI facts used:

- Generated images on web/app appear *inline in the chat stream when the client dispatches the tag or the generate_image tool card*. Files library / profile → Files is the durable gallery on grok.com.
- Imagine tab (`grok.com/imagine`) is a different pipe than chat-attached generate.
- Drive `web_view_link` opened and showed the JPEG on this phone 2026-09-03 20:01. That is the only phone-proven show path we have in writing.

## Path 1 — consecutive `render_file` tags (try on dump)

Max 4 consecutive tags on kept `artifacts/rendered/*.jpg`. Web carousel. Android: try when the operator said dump / show / inline / emit / see the pictures / carousel. If brown-out, do not retry the same tag set. Fall to path 2+3.

Callable: `scripts/android_show.py --client ANDROID --utterance "dump the pictures"` → `emit_render_file: true`.

## Path 2 — contact sheet (one tap target)

`scripts/contact_sheet.py` grids A–D into one JPEG. Keep + flush that sheet as its own triple. Android can tap one card. Extra stills never become letters E–H.

## Path 3 — Drive view links (proven)

Same-turn `google_drive_upload_artifact` on the keep triple. Speak `https://drive.google.com/file/d/<id>/view`. This is the rescue *and* the default Android show path when tags are muted.

If the upload tool is missing: speak “Turn me on to Garage Expert so I can upload.” Stage the buffer. Do not claim pushed.

## Path 4 — live tool cards + Imagine-tab paste

`generate_image` tool-result cards are visible during the tool phase. They drop after speak on this Android build. Allowed as a *during-turn* preview only. Manual rescue: paste the sibling `.prompt.md` into the Imagine tab.

## Same-turn order on ANDROID + dump

1. generate / keep triple
2. `upload_buffer.py --write-queue`
3. flush if `host_mode.py` says `can_flush`
4. `--gate` 0
5. emit path 1 tags (max 4) **and** path 2 sheet **and** path 3 Drive links
6. if tags brown-out, say so and point at Drive + sheet

Never emit `render_generated_image` as the only copy.

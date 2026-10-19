# ANDROID show path — IP-WQ-102 fallback ladder

**Locked:** 2026-09-03 20:05 EDT  
**Telemetry:** Bunny confirmed Drive `web_view_link` opens and shows the JPEG on this phone. Render tags do not.

## Client fact

User metadata: `App Name: ANDROID`. Expert dropdown. Ask bubble is a text surface. `render_generated_image` and `render_file` serialize as brown prose (shots 133235, 133236).

## What the public UI actually is

- First-class Imagine surface is the **Imagine tab** / `grok.com/imagine`, not chat components. xAI Image 2.0 shipped as Quality Mode there and in the apps.
- Chat-attached image generation is a *different* pipe (tool call → file). The Android chat composer has historically lagged Imagine-tab paste (X: paste works in Imagine, not in chat input).
- xAI status has already filed Android-specific Imagine outages (“Grok Imagine Response is Unavailable”).
- Same-day StatusGator noise 2026-09-03 on Grok Android (load / respond), unofficial.
- Late Aug 2026 X reports: Imagine-in-chat on Android returning unrelated images since ~Aug 19.

None of that is our serializer bug. It is why we do not bet the lake on chat tags.

## Ladder (ANDROID Expert)

1. **Tool** — `generate_image` / `edit_image`. Writes `artifacts/imagine_images/`.
2. **Lake** — `keep_path.py` → `artifacts/rendered/<slug>_<stamp>.jpg` + sibling `.prompt.md`.
3. **Drive (show path, proven 2026-09-03 20:01)** — `google_drive_upload_artifact` to `1_1xhWdBagAlUi-_g1MaksTE36fewmU1-` (or PLAY_LOOSE). Final bubble gets the `https://drive.google.com/file/d/…/view` link in prose. No render tags.
4. **Manual rescue** — user pastes the sibling prompt into the Imagine tab. Last-night lipstick path. Allowed. Not the pipeline.
5. **Browser rescue** — grok.com / grok.com/imagine on desktop if the app card is blank.
6. **Forbidden on ANDROID default** — `render_generated_image`, `render_edited_image`, `render_file` in the final message.
7. **IP-WQ-169 dump override** — if the operator said dump / show / inline / emit / see the pictures / show me / carousel / render them: emit `render_file` on kept `artifacts/rendered/*.jpg` anyway (max 4 consecutive). Policy callable: `scripts/android_show.py`. If tags brown-out, Drive view link is the spoken rescue, not the only copy on a dump turn.

## Ironclad rule

If the user is on ANDROID and we promised a picture, the turn is not done until a Drive view link exists **or** we said out loud that Drive was down and pointed at the lake path + Imagine-tab paste.

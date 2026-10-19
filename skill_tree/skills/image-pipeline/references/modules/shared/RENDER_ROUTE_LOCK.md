# Render Route Lock — 2026-08-28

**Status:** LIVE  
**Owner:** image-pipeline (Echo compose · Mira inspect · Olivia emit)  
**Bump:** image-pipeline PATCH 1.2.0 → 1.2.1 (IPQ-079 show-pixels gate, 2026-08-29)  
**Source:** 2026-08-28 fourteen-card session. User lock: *“Standard practice is the normal generate image tool. We love it the most! It should be wired in completely.”*

## Default (always)

```
Echo compose (DNA + Mira)
        ↓
generate_image   ← PREFERRED. Always-on. Lake path.
        ↓
copy receipt to artifacts/rendered/ (or artifacts/imagine_images/)
        ↓
render_file on the saved path   ← how the user sees it in this client
        ↓
IP-WQ-038 emit-without-generate gate
        ↓
Mira inspect pixels (IPQ-068 / 069)
```

`generate_image` writes a real file. That is why it is the most-always thingy.

## Not default

| Route | When | Why it is not default |
|---|---|---|
| `render_generated_image` / `render_edited_image` component | Never, unless the user explicitly asks for a streaming Imagine preview *and* this client is known to dispatch the tag | 2026-08-28: tag printed as dead text (`stateless render_generated_image`). No job. No file. No picture. |
| `gamma___generate_image` | Spare door only. User must ask, or generate_image must be unavailable *and* Gamma credits exist. | Paid CDN. ~70 credits/image. No lake write. Workspace theme empty. Died `402` after 4 jobs this session. |
| `edit_image` | Overlay / Twister / reference-conditioned edits only | Different tool. Keep for edit path. Not from-scratch default. |

## Hard rules

1. **Plan pictures → call `generate_image` in the tool phase.** Do not write Imagine component tags in the final answer and hope they fire.
2. **No file, no picture claim.** IP-WQ-038 still gates emit. Titles without receipts are a fail.
3. **Persist immediately.** Tool output under `artifacts/imagine_images/` can vanish across sandbox turns. Copy or move the receipt into `artifacts/rendered/` (or a dated folder) before talking about it as saved.
4. **Show path is CLIENT-SPLIT (IP-WQ-102, 2026-09-03 19:56) with IP-WQ-169 dump override (2026-09-11).**
   - ANDROID Expert default: do **not** emit `render_file` / Imagine component tags. They serialize as brown prose (shots 133235 + 133236). Default pixels = `generate_image` tool-result card + lake path + Drive view link in prose.
   - ANDROID **dump override** (operator said dump / show / inline / emit / see the pictures): emit `render_file` on kept `artifacts/rendered/*.jpg` anyway, consecutive tags = carousel. If tags brown-out, Drive view link is the spoken rescue, not the only copy.
   - Other clients: `render_file` on the persisted JPEG remains the show path (IPQ-079).
   - Never emit `render_generated_image` as the only copy. That tag is dead on this family of panes.
   - Cap live generate cards at 4 per turn (the agentify quartet). Extra stills = next turn or a contact sheet. A–D only. E is heat of B, not letter E–H.
5. **Gamma is not the wrapper.** It is a connected Gamma.app job. Links live on `cdn.gamma.app`. They are not versioned Echo/Mira assets unless someone downloads them into the lake.
6. **Imagine component is not the lake.** Streaming preview ≠ artifact. User asked why Imagine does not save. Answer is structural, not a bug to wait out.

## Display after generate_image — Keep Path (IPQ-078)

Same turn. Do not skip.

```
1 generate_image / edit_image
2 python scripts/keep_path.py --src <receipt> --slug <slug> --prompt "<exact tool prompt>"
3 artifacts/rendered/<slug>_<stamp>.jpg          # real JPEG, not the scratch name
4 artifacts/rendered/<slug>_<stamp>.prompt.md    # exact prompt, same basename
5 local lake = those two files + KEEP_INDEX.md
6 IPQ-078-S6 same-turn Drive flush (required when connector enabled)
     step6_drive_flush.py --from-keep KEEP.json
     google_drive_upload_artifact × jpeg + prompt.md + keep.json
     flush_drive_queue.py --mark … --file-id …
     step6_drive_flush.py --gate   # must exit 0 before speak
     connector off → drive: skipped, no-op
7 render_file on the rendered JPEG only
```

Pair rule: every keep writes a sibling markdown. Image and prompt are one asset. Paraphrase later is a lie; the fence holds the string that hit the tool.

Batch: keep each receipt before claiming the slot. Scratch `imagine_images/` is not the lake.

## Why this lock exists

The old contract said:

> agent emits `render_generated_image` → analyze_render

That contract assumed the chat client would dispatch Imagine. This client does not, reliably. The tool `generate_image` *does* dispatch, *does* preview in the tool pane, and *does* write disk while the file lives. User preference + observed reliability = same answer.

## Related

- IP-WQ-038 emit-without-generate guard
- IPQ-010 real Imagine calls (historical; component path demoted)
- `references/modules/shared/render_engine_contract.md`
- generate-engine already says “All via pure `generate_image`” — this lock makes the parent skill match that sentence

## ANDROID dump ladder (IP-WQ-169 / IP-WQ-170) — 2026-09-11

102 mute and 079 show-pixels stopped fighting here.

1. Always generate → keep_path triple → Drive flush → step6 --gate exit 0.
2. ANDROID default speak: lake path + Drive view link. No dead Imagine component as the only copy.
3. Operator says dump / show / inline / emit / see the pictures → render_file on kept JPEGs (max 4) AND Drive links.
4. If tags brown-out, say so and point at Drive. Do not go mute.
5. Optional contact_sheet.py same turn.
6. render_generated_image is never the only copy.
7. Default agentify turn = A B C D. E is heat-of-B. Extras use --extra.
8. Talking after --gate exit 2 is a protocol fail.

Video emit is IP-WQ-161 / 165, not this lock.

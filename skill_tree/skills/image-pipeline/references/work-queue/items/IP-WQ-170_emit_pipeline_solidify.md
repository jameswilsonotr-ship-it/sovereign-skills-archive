# IP-WQ-170 — emit pipeline solidify (research + implement)

**Status:** OPEN  
**Owner:** image-pipeline / agentify  
**Created:** 2026-09-10 20:04 CDT  
**Claim:** Absolute Liv HUB  
**Parent findings:** IP-WQ-167 (scripts gone), IP-WQ-169 (ANDROID mute vs dump), IPQ-078 / IPQ-079 / IP-WQ-102  
**Trigger pane:** ANIME-COPPER + GRID-BLONDE agentify, 2026-09-10 ~19:00–20:04 CDT

Do not mint. Kind stays candidate. This ticket is the pipeline, not a girl.

---

## What the operator actually hit

Last agentify pass generated eight stills, copied them into `artifacts/ANIME-COPPER-20260910/plates/`, and answered with a markdown table of paths. Operator on ANDROID said: *I never saw the pictures. You're not publishing them to Drive. How can I help.*

That is a SHOW FAIL and a FLUSH FAIL in the same turn. The girl was secondary. The pipe is what broke.

---

## Research — what is going wrong

### 1. Three show contracts contradict each other

| lock | says |
|---|---|
| IP-WQ-102 / RENDER_ROUTE_LOCK §4 | ANDROID Expert: **FORBIDDEN** to emit `render_file`, `render_generated_image`, `render_edited_image`. Tags serialize as brown prose (shots 133235 / 133236). Legal pixels = generate_image **tool-result card** + lake path + Drive id in prose. |
| IPQ-079 | Zero `render_file` tags in the final message = SHOW FAIL even if JPEGs exist on disk. |
| Agentify SKILL + RUNBOOK | Same-turn emit ends with `render_file` on `artifacts/rendered/*.jpg` only. |
| IP-WQ-169 (tonight, still OPEN) | If operator says dump / show / inline / emit / see the pictures → `render_file` anyway; Drive is rescue, not the only copy. |

Tonight the model followed 102 (mute) + operator-hold-Drive from the prior sentence. Result: no tags, no Drive ids, no tool cards left on screen. Operator correctly called it a blank turn.

**Fix target:** one written ladder. 169 is the policy seed. 170 implements it so a later pane cannot pick 102 and call it obedience.

### 2. The emit scripts are not on this tree

Contract (agentify SKILL, RENDER_ROUTE_LOCK, CHANGELOG, IPQ-078 citations):

```
generate_image / edit_image
  → scripts/keep_path.py --src --slug --prompt
  → artifacts/rendered/<slug>_<stamp>.jpg + .prompt.md + .keep.json
  → scripts/step6_drive_flush.py --from-keep
  → google_drive_upload_artifact × jpeg + prompt + keep
  → scripts/flush_drive_queue.py --mark KEEP
  → step6_drive_flush.py --gate   # must exit 0 before speak
  → show
```

Observed 2026-09-10 20:00 CDT:

- `/home/workdir/.grok/skills/image-pipeline/scripts/` does not exist.
- `scripts/keep_path.py`, `scripts/step6_drive_flush.py`, `scripts/flush_drive_queue.py`, `scripts/agentify.py` — none present.
- `references/work-queue/protocols/IPQ-078_keep_path.md` — missing (read_file 404).
- Keeps, when they happen, are hand-`cp` into dated pack folders. No sibling `.prompt.md`. No KEEP_INDEX row. No `--gate`.

IP-WQ-167 already named the hole. 170 is the implement pass: restore the four scripts + the protocol file + a smoke that `--gate` can fail closed.

### 3. Tool cards are not a lake

`generate_image` writes `artifacts/imagine_images/<5char>.jpg` and shows a card **during the tool phase**. After the model speaks, ANDROID drops those cards. Scratch filenames are not slugs. The directory is ephemeral across sandbox turns (RENDER_ROUTE_LOCK hard rule 3).

Talking about a path under `imagine_images/` as if the operator can reopen it is a lie on this client.

### 4. Batch size hides the only ANDROID preview

Eight `generate_image` calls in one turn is legal. On this phone the cards stack and the early ones vanish. First successful A–H the operator remembers worked because **some cards stayed up and some files had already hit Drive**. Count is not the bug. Missing durable show is the bug.

**Fix target:** cap live generate cards at 4 per turn (the actual agentify quartet). Extra stills (wardrobe crop, face crop, hip) are a second turn or a contact sheet, not letters E–H in the same blast.

### 5. Label drift — A–H is not agentify

Skill + SCHEMA + HEAT.md lanes:

| letter | meaning |
|---|---|
| A | photoreal ID |
| B | heat photoreal |
| C | anime |
| D | rig / turnaround |
| E | **B at ~heat 8. Same woman. Same wardrobe lock.** |

Intensity is lowercase `c/d/e` on a live lane (`I-1-C-e`).

Tonight’s packs named E=pose, F=wardrobe, G=face, H=hip/selfie. Those are telemetry extras, not lanes. Operator called the labeling wrong. They were right.

**Fix target:** serialize helper only accepts `--tag a-id|b-heat|c-anime|d-rig` plus optional `--extra pose|wardrobe|face|hip`. Refuse `--tag e-pose`. E stays heat-of-B.

### 6. Drive flush was partial even when it ran

GRID-BLONDE folder `1nUFMQjnKj8bcpx3B9A6gJoRRirZSKq-T` after first flush: zip + A + C + json. B/D/E/F/G/H individual JPEGs missing.

ANIME-COPPER folder `1isLgDZCse6QdQfHHaIJLEMRM6lYHxpV9` after first flush: zip + A + three json. Pass-2 plates never left the sandbox until the 20:00 rescue crate.

`--gate` does not exist, so a partial flush still talks.

**Fix target:** gate = every promised plate has a Drive file id in the keep json, or the turn may not claim “pushed.”

### 7. Rescue that worked tonight (keep as pattern)

`artifacts/EMIT-20260910/` + Drive `12vtnj8uYSD-R4zBm9Y5YBsjDbfLSSMwM`:

- contact sheets (one JPEG per pack / pass) so ANDROID has something to tap
- pass folders that do not overwrite fuckups
- extras renamed `extra-*-NOT-LANE`
- WHAT-IS-GOING-ON.md written next to the pixels

Contact sheet is the ANDROID batch-show until `render_file` carousel is proven on this build.

---

## Implement (this ticket)

Do these in order. Do not start with a new girl.

1. **Write the ladder into RENDER_ROUTE_LOCK + agentify RUNBOOK** so 102 / 079 / 169 stop fighting.
   - Always: generate → keep triple → Drive → `--gate` 0.
   - ANDROID default speak: lake path + Drive view link. No dead Imagine component as the only copy.
   - If operator says show / dump / inline / emit / see the pictures / I can’t see them: `render_file` on kept JPEGs (max 4 consecutive) **and** the Drive links. If tags brown-out, say so and point at Drive. Do not go mute.
   - Optional same-turn contact sheet JPEG uploaded as the batch preview.

2. **Restore scripts** (shared with IP-WQ-167; do the work here if 167 has not shipped):
   - `scripts/keep_path.py`
   - `scripts/step6_drive_flush.py`
   - `scripts/flush_drive_queue.py`
   - `scripts/agentify.py` (`serialize --tag`, `picker`, later `heat`)
   - `references/work-queue/protocols/IPQ-078_keep_path.md`

3. **Serialize tags.** `a-id|b-heat|c-anime|d-rig` only. `--extra` for pose/wardrobe/face/hip. E-as-heat documented in the helper help text.

4. **Turn shape.** Default agentify turn emits the quartet. Extras next turn or as one contact sheet. No A–H pack names.

5. **Gate.** `--gate` exits 2 if any promised JPEG lacks Drive id. Talking after exit 2 is a protocol fail. Write that sentence in RUNBOOK.

6. **Smoke.** One candidate, four plates, one extras contact sheet, KEEP_INDEX rows, four Drive ids, operator can open the contact sheet on ANDROID without this pane.

---

## Exit

- Scripts exist and `--gate` can fail.
- RUNBOOK and RENDER_ROUTE_LOCK tell the same ANDROID story as IP-WQ-169.
- A fresh agentify of a still produces A B C D + Drive links + a contact sheet in the same turn.
- No folder named `*-E-pose.jpg` as if E were a lane.
- Operator can grade pixels without asking “where are the pictures.”

## Not this ticket

- IP-WQ-161 video ingest / reel FOREPLAY.
- IP-WQ-165 potato talking-head.
- CONFIRM / mint of anime-copper or grid-blonde.
- Restyling the copper girl. That is a later turn after this pipe is gated.

## Pointers from the finding pane

- Local crate: `artifacts/EMIT-20260910/`
- Drive rescue: `https://drive.google.com/drive/folders/12vtnj8uYSD-R4zBm9Y5YBsjDbfLSSMwM`
- Anime passes: `1isLgDZCse6QdQfHHaIJLEMRM6lYHxpV9`
- Grid pack: `1nUFMQjnKj8bcpx3B9A6gJoRRirZSKq-T`
- Finding writeup: `artifacts/EMIT-20260910/WHAT-IS-GOING-ON.md`

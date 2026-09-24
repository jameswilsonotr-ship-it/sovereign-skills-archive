# Split Engine vocab — FOUR plates
Lock 2026-08-28 20:15 EDT. Claim: Absolute Liv HUB.

## Count (locked)

One source person → **four** plates. Heat and anime are both mandatory. Not either/or.

| Slot | Name | Job |
|---|---|---|
| A | Realistic cue | Photoreal identity card. **Parent.** Used to regenerate later so we do not deepfake via edit_image on a stranger. |
| B | Heat photoreal | Same bones, heat register, still photoreal / 3D-lit. |
| C | Anime / VTuber | Same bones, cel or modern digital glam (IP-WQ-041 substyle). This is how the factory started. |
| D | Rig | Joint / turnaround / 4-pose sheet. Clean ground. Feeds Live2D or Blender later. |

Two people (after segment) → eight plates.  
Three people → twelve. Per-turn default cap = **two people = eight plates**. Queue the rest.

Optional after the four (operator must pick):

| Opt | Name | Job |
|---|---|---|
| M2 | Generate-merge | `generate_image` writes Olivia+Bunny DNA onto the source pose. Fresh pixels. Lake path. |
| M3 | Edit-merge | `edit_image` Twister on kept A. Overlay-engine twin. |

M2/M3 are the “two optional ways we put our visual DNA on any arbitrary reference.” Not the inbound default.

## Machines (do not collapse)

- **Split** = this module. Inbound still → segment → A/B/C/D.
- **Generate-engine** = from-scratch `generate_image` twin (`references/modules/generate-engine/`). Default four + two optional.
- **Overlay-engine** = edit / merge twin (`references/modules/overlay-engine/`). Default four-on-pixels + two optional. Needs a kept file.
- **Cab overlay** = Grafana / ROS2 HUD. Different job. Needs kept A or D + a mask. Not inbound.

## Kept file

IPQ-078 triple:

```
artifacts/rendered/<slug>_<stamp>.jpg
artifacts/rendered/<slug>_<stamp>.prompt.md
artifacts/rendered/<slug>_<stamp>.keep.json
```

Plus skill-tree copy `references/visuals/keeps/YYYY/MM/` and Drive folder `1_1xhWdBagAlUi-_g1MaksTE36fewmU1-` when connector enabled. If Drive is down, status=`queued` and the next turn flushes.

Per-conversation scratch `artifacts/imagine_images/` is not the lake.

## Always-on wrapper

Every picture intent, prompted or not:

```
generate_image  →  keep_path.py  →  render_file(kept jpeg)
```

`edit_image` only for overlay-engine / M3. Still keep_path after.  
`render_generated_image` is dead in this phone client.  
`gamma___generate_image` is a paid spare door.

Intent catalog: `RENDER_STILL` retired. Use `GENERATE_IMAGE`.

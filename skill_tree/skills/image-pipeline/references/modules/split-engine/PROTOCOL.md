# Split Engine protocol — inbound still → 0 + four plates

## Per attachment

1. **Copy** the file into `artifacts/inbound/<stamp>_<name>` (do not edit the original).
2. **Classify** with `scripts/inbound_classify.py` → layout: `single` | `pair` | `grid2` | `grid3` | `grid2x2` | `chrome` | `unknown`.
3. **Segment** with `scripts/segment_grid.py` when layout is grid / chrome / pair-geometry.
   - Grid: equal geometric crops. Deterministic.
   - Chrome: drop dark UI bars if detected, then re-classify.
   - True instance masks (SAM): stub only. Until weights live, a pair is two queued people, not two magic cut-outs.
4. **Enqueue** with `scripts/inbound_queue.py`. One queue item per person-crop. Serialized. Heavy and Expert use the same JSON.
5. **Menu** (operator picks one per item; default if she just said process these is C-generate):
   - **A WHY** — what did you send me this for. Analysis first. Offer 0+A+B+C+D inline dump unless vetoed.
   - **B AGENT** — draft a candidate agent card. AND dump 0+A+B+C+D inline.
   - **C GENERATE** — generate-engine 0+A+B+C+D + two optional DNA-merge steps.
   - **D OVERLAY** — overlay-engine four-on-pixels + two optional. Requires a kept parent or the source crop as edit base.
6. **Plan** with `scripts/split_plan.py` → A/B/C/D prompts + optional M2/M3.
7. **Render** each planned slot with host `generate_image` (or `edit_image` for D/M3).
8. **Keep** every receipt with `scripts/keep_path.py`. No keep, no picture claim (IP-WQ-038).
9. **Receipt** IP-WQ-042: planned / attempted / landed / dropped / moderation.

## Batch rule

Ten stills, three of them pairs → classify all ten first, segment the three, then process two people per turn (eight plates). Remaining stay in `artifacts/inbound-queue/QUEUE.json`.

## DNA merge (optional only)

M2 and M3 put Olivia + Bunny characteristics onto the reference. They do not run unless the operator says merge. Default inbound is four plates of whoever is in the crop.

## Scripts

```
python3 scripts/inbound_classify.py --src FILE
python3 scripts/segment_grid.py --src FILE --out DIR
python3 scripts/inbound_queue.py --add FILE [--layout LAYOUT]
python3 scripts/inbound_queue.py --next
python3 scripts/split_plan.py --desc DESC.json --engine generate
python3 scripts/keep_path.py --src RECEIPT.jpg --auto-slug --prompt "..."
```


Dump means interleaved render_file of kept JPEGs. Not disk-only.

## Isolate routes (no SAM)

After a crop exists, run `isolate_person.py`.
G = generate_image identity card from description.
E = edit_image keep-this-person-only on the crop file.
Both are allowed. Winner feeds four plates.
Quad = grid2x2. Already live.

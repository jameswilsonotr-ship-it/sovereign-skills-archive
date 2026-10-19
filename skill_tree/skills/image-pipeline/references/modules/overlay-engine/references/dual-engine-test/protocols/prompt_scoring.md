# Protocol — Scoring (IPQ-019)
**Load after every image or batch. Display is mandatory — no exceptions.**

Shared contract: `image-pipeline/references/modules/shared/scoring_and_forensics.md`

Per image (required in reply):
```
score: DNA _/10 | Pose _/10 | Outfit _/10 | Overall _/10 | note: <short>
tingly: yes | no | meh
```

Hair lock entities (Shauna V7 and any entity listed in `default_six` `scoring.hair_texture_gate`):
```
hair_texture: pass | fail | soft
```
Soft S-waves / piecey only = pass. Tight ringlets or corkscrew = **fail** (DNA fail even if face scores high).

After default six or harness batch:
```
SET SCORES
1 … Overall x
…
avg overall: x.x
```

If images were staged (“READY”) and rendered in a later turn, this block **must still appear** in the turn that emits the images.

Disk write to dual-engine-test results is optional; **display is mandatory**.

Also load forensics panel when harness / default-six / `forensics on` (IPQ-022 — see scoring_and_forensics.md).

# Known Failure Modes & Observations
**Last updated**: 2026-07-24

## 1. Empty / Missing File After Successful Model Return
**Symptom**: Tool returns an image preview and an ID, but the file is either 0-byte or completely absent from `/home/workdir/artifacts/imagine_images/`.

**Observed frequency**:
- Higher under concurrent / Actor-style calls
- Higher when issuing 4+ images in a short window
- Lower on single sequential calls

**Current hypothesis**: Output-side moderation or sandbox write drop. The model can still show a preview while the write is blocked or fails silently.

**Handling rule**:
- Treat as first-class failure.
- Log immediately in [RUN LOG].
- Optionally issue one sequential retry.
- Do not count toward scoring averages.

## 2. Liv DNA — Bunny Ears
Generate path frequently attaches bunny / sequin ears to Liv even when the prompt explicitly forbids them.  
Overlay path is more reliable at suppressing them.

## 3. Liv DNA — Shark-Fin / Tall Vertical Spike
Asymmetrical black pixie repeatedly grows a tall vertical “shark-fin” spike, especially on rear angles.  
This is non-canonical. Score DNA fidelity down when it appears.

## 4. Footwear Drift
Occasionally platform stilettos become thigh-high boots or change style.  
Record as composition / outfit-lock note.

## 5. Ethnicity / Face Drift
Seen occasionally on angle-expansion or high-batch runs.  
Flag when severe.

## 6. Batch Size Correlation
Larger simultaneous batches (especially 4–8) show higher write-failure rates.  
Prefer smaller sequential groups when reliability is critical.

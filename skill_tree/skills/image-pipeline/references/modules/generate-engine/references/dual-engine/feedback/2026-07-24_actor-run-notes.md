# Actor Engine Run Notes — 2026-07-24
**Purpose**: Capture detailed behavior for later testing-engine refactor into both skills.

## Intent of Option A (Asyncio Actor)
- Simulate concurrent "actors" that independently generate Liv and Bunny versions
- Each actor should own its own prompt construction + generation call
- Results collected and scored together
- Designed to surface race conditions, empty-file issues, and DNA drift under concurrency

## Pre-run State
- Strongest current bases: front Overlay Bunny (LZe77), front Generate Bunny (HJka5)
- Known issue: Generate path frequently attaches bunny ears to Liv
- Known issue: intermittent 0-byte / missing file writes after successful model return

## Actor Run Execution Log
- Actor-Liv call: returned ExLia.jpg
- Actor-Bunny call: returned x751C.jpg
- Disk check: both files present and non-zero size
- DNA observation: Liv correctly has NO bunny ears this time (success)
- Bunny: holo ears present, copper bob, but footwear drifted to thigh-high boots instead of platform stilettos
- Concurrency note: both calls issued in parallel; both succeeded without empty-file failure

## Scores (System)
- Actor Liv (ExLia): Overall 8.6 | Heat 6.5 | DNA 9.0 | Composition 8.5
  Notes: Best Liv DNA of the entire session so far. No ears, clean pixie + gem, strong body.
- Actor Bunny (x751C): Overall 7.9 | Heat 7.0 | DNA 8.0 | Composition 7.8
  Notes: Good face and ears, but footwear changed to thigh-high boots (outfit drift). Still usable.

## Actor Rear Versions (requested finish)
- Actor-Rear-Liv (S33bF): Generated but **hair still has tall shark-fin spike**. User correctly flagged this as non-canonical. DNA hair fidelity lower than claimed earlier.
- Actor-Rear-Bunny (2HYem): Clean copper bob + holo ears + neck tattoo. Good rear pose. Footwear correct this time.

## Score Adjustments
- Actor Front Liv (ExLia): Revised DNA from 9.0 → 7.5 because of the shark-fin hair (user correct). Overall revised to ~7.8
- Actor Rear Liv (S33bF): Overall 7.4 | DNA hair 5.5 (fin problem persists)
- Actor Rear Bunny (2HYem): Overall 8.5 | DNA 9.0 | strong rear result

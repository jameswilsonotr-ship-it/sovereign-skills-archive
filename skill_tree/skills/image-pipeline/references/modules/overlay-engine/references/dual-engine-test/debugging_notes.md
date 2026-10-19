# Debugging Notes — Image Delivery / Moderation / Persistence
**Engine-agnostic observations (shared schema)**  
**Last updated**: 2026-07-24T11:13

## Core Failure Mode (observed repeatedly)
1. Tool layer returns success + cardId / preview
2. File is missing from disk shortly afterward (or never written)
3. Client sometimes shows “We can’t generate this image. Your idea didn’t pass the moderation.”
4. This happens on both parallel and serial emission
5. Happens even on completely innocent subjects (apple, mug, sunflower, glass of water)

## Counter-evidence (same day)
- Character batches of **2 concurrent** (B + C H3) → clean, ~11–12 s, files landed, no moderation block
- Character batches of **4 concurrent** (C H6 + H9) → clean, files landed, scores 9.0–9.2
- Simple-object batches of 4 parallel + 4 serial → tool success claimed, files gone, moderation blocks on user side

## Current Working Hypothesis
- Not purely parallel-vs-serial
- Interaction between batch size, content type, and a downstream moderation / persistence gate
- Strong DNA-locked character prompts currently more stable than “safe” simple objects (counter-intuitive)
- “streamed” in run logs correlates with files that actually persisted
- cardId alone does **not** guarantee a durable file

## Practical Rules (until the layer stabilizes)
- Prefer max **2 concurrent** when reliability matters
- Treat 4 concurrent as higher-risk
- Treat 8+ as high-risk
- Log every “tool success but file missing / moderation block” as a first-class failure
- Do not trust cardId without a subsequent disk or client-visible confirmation

## Moving Target
This behavior is inconsistent and appears to change. All entries below are timestamped so future runs can be compared.

---

### 2026-07-24 — Simple object parallel/serial test
- 4 parallel (apple, mug, sunflower, succulent) + 4 serial (orange, glass, daisy, book)
- Tool reported all 8 successful
- Zero files remained on disk
- User saw moderation blocks
- Conclusion: delivery/moderation failure, not prompt failure

### 2026-07-24 — Character harness (other conversation)
- 2 concurrent (B+C H3) → success, fast, files present
- 4 concurrent (C H6+H9) → success, files present
- Shows concurrent emission *can* work cleanly under different content/batch conditions
